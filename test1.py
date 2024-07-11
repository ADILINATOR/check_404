import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def find_pdf_links_on_page(url):
    pdf_links = []

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href'].strip()
            if href.lower().endswith('.pdf'):
                pdf_url = urljoin(url, href)
                pdf_links.append(pdf_url)

        return pdf_links

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []


