import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin


def find_pdf_links(endpoint_base_url, start_num, end_num, output_csv):
    # List to store all PDF URLs
    pdf_urls = []

    # Iterate through the range of numbers
    for num in range(start_num, end_num + 1):
        endpoint_url = urljoin(endpoint_base_url, str(num) + '/')

        try:
            response = requests.get(endpoint_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
            else:
                print(f"Failed to fetch HTML content from {endpoint_url}. Status code: {response.status_code}")
                continue
        except requests.exceptions.RequestException as e:
            print(f"Error fetching HTML content from {endpoint_url}: {str(e)}")
            continue

        # Find all links on the page
        for link in soup.find_all('a', href=True):
            href = link['href'].strip()
            if href.lower().endswith('.pdf'):
                pdf_url = urljoin(endpoint_url, href)
                pdf_urls.append(pdf_url)

    # Write the PDF URLs to CSV
    if pdf_urls:
        try:
            with open(output_csv, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['PDF URL'])
                for url in pdf_urls:
                    writer.writerow([url])
            print(f"Successfully wrote {len(pdf_urls)} PDF URLs to {output_csv}")
        except IOError:
            print(f"Error writing to {output_csv}")


# Example usage:
if __name__ == "__main__":
    endpoint_base_url = 'http://www.rcmbase.kz/en/karzav/karzav_card/'
    start_num = 1
    end_num = 560
    output_csv = 'pdf_urls.csv'

    find_pdf_links(endpoint_base_url, start_num, end_num, output_csv)
