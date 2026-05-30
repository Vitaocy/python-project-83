import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for, flash, redirect, get_flashed_messages
from url_repository import UrlRepository
from validators import url as url_validate
import requests
from bs4 import BeautifulSoup


load_dotenv()
app = Flask(__name__)  # NOSONAR
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # NOSONAR
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

        code = response.status_code
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        h1_tag = soup.find('h1')
        h1 = h1_tag.get_text(strip=True) if h1_tag else ''

        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else ''
        
        meta_description = soup.find('meta', attrs={'name': 'description'})
        description = meta_description.get('content', '') if meta_description else ''
        
        check_data = {
            'url_id': id,
            'code': code,
            'h1': h1,
            'title': title,
            'description': description
        }

        repo.add_check(check_data)
        flash('Страница успешно проверена', 'success')
        
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        
    return redirect(url_for('urls_show', id=id))
