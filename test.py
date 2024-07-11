import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from io import BytesIO
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError

def get_pdf_url_from_iframe(page_url):
    try:
        response = requests.get(page_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        iframe = soup.find('iframe')
        if iframe and 'src' in iframe.attrs:
            pdf_url = urljoin(page_url, iframe['src'])
            return pdf_url
        else:
            print(f"No iframe found in {page_url}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"RequestException while fetching {page_url}: {e}")
        return None

def check_pdf_link(url):
    try:
        response = requests.get(url)
        print(f"URL: {url}")
        print(f"Status Code: {response.status_code}")

        response.raise_for_status()

        if response.headers.get('Content-Type') != 'application/pdf':
            print("Not a PDF file.")
            return True

        with BytesIO(response.content) as file:
            try:
                pdf_reader = PdfReader(file)
                print(f"Number of Pages: {len(pdf_reader.pages)}")
                return len(pdf_reader.pages) == 0
            except PdfReadError as e:
                print(f"PdfReadError: {e}")
                return True
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return True

