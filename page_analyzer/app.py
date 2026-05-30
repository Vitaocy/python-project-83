import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for, flash, redirect, get_flashed_messages
from url_repository import UrlRepository
from validators import url as url_validate
import requests


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
repo = UrlRepository(app.config['DATABASE_URL'])


def validate(url):
    errors = {}
    name = url.get("name", "")
    if not name:
        errors["name"] = "Can't be blank"
    elif len(name) > 255:
        errors["name"] = "URL must be shorter than 255 characters"
    elif not url_validate(name):
        errors["name"] = "Invalid URL"

    return errors


@app.route('/')
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

    errors = validate(url)
    if errors:
        return render_template('index.html', url=url, errors=errors), 422

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
        response = requests.get(url['name'], timeout=5)
        response.raise_for_status()
        repo.add_check(id, response.status_code)
        flash('Страница успешно проверена', 'success')
        
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        
    return redirect(url_for('urls_show', id=id))
