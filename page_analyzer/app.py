import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for, flash, redirect, get_flashed_messages
from page_analyzer.url_repository import UrlRepository
from page_analyzer.validators import validate_url
from page_analyzer.parser import parse_data
import requests
from page_analyzer.url_normalizer import normalize_url


load_dotenv()
app = Flask(__name__)  # NOSONAR
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # NOSONAR
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
repo = UrlRepository(app.config['DATABASE_URL'])


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def urls_get():
    urls = repo.get_content()
    return render_template('urls.html', urls=urls)


@app.get('/urls/<id>')
def urls_show(id):
    messages = get_flashed_messages(with_categories=True)
    url = repo.find(id)
    checks = repo.get_checks(id) 
    return render_template('urls_show.html', url=url, checks=checks, messages=messages)


@app.post('/urls')
def urls_post():
    url_data = request.form.get('url')
    url = {'name': url_data}

    errors = validate_url(url)
    if errors:
        return render_template('index.html', url=url, errors=errors), 422

    normalized_url = normalize_url(url_data)

    existing_url = repo.find_by_name(normalized_url)

    if existing_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for('urls_show', id=existing_url['id']))

    url = {'name': normalized_url}
    repo.save(url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('urls_show', id=url['id']))


@app.post('/urls/<id>/checks')
def urls_checks(id):
    url = repo.find(id)
    
    if url is None:
        flash('URL not found', 'danger')
        return redirect(url_for('urls_show', id=id))
    
    try:
        page_data = parse_data(url['name'])

        check_data = {
            'url_id': id,
            **page_data
        }

        repo.add_check(check_data)
        flash('Страница успешно проверена', 'success')
        
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        
    return redirect(url_for('urls_show', id=id))
