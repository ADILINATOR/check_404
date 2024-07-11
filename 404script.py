import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from test import get_pdf_url_from_iframe,check_pdf_link
import csv
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


# Example usage:
if __name__ == "__main__":
    base_url = "http://www.rcmbase.kz/en/karzav/karzav_card/"
    links_csv = "broken_links.csv"

    # Open the CSV file in append mode before the loop
    try:
        with open(links_csv, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            for i in range(144, 146):
                page_url = f"{base_url}{i}/"
                pdf_links = find_pdf_links_on_page(page_url)

                if pdf_links:
                    print(f"Found {len(pdf_links)} PDF links for {page_url}:")
                    for link in pdf_links:
                        pdf_url1 = get_pdf_url_from_iframe(link)
                        if pdf_url1 and check_pdf_link(pdf_url1):
                            try:
                                # Write each PDF link to the CSV file
                                writer.writerow([link])
                            except IOError as e:
                                print(f"Error writing to CSV: {e}")
                else:
                    print(f"No PDF links found for {page_url}.")

    except IOError as e:
        print(f"Error opening CSV file: {e}")
