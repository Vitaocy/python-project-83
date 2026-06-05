import requests
from bs4 import BeautifulSoup


def parse_data(url):
    response = requests.get(url, timeout=5)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    h1_tag = soup.find('h1')
    title_tag = soup.find('title')
    meta_description = soup.find('meta', attrs={'name': 'description'})

    return {
        'code': response.status_code,
        'h1': h1_tag.get_text(strip=True) if h1_tag else '',
        'title': title_tag.get_text(strip=True) if title_tag else '',
        'description': meta_description.get('content', '') if meta_description else '',
    }