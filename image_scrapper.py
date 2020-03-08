import os
import sys
import requests
from bs4 import BeautifulSoup


class ImageScrapper:
    def __init__(self):
        self.timeout = 60
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0"
        }
        self.allowed = ('jpg', 'jpeg')
        self.download_path = os.environ.get('FILE_PATH', './data')

    def parse_url(self, url):
        _, site, *page = (part for part in url.split('/') if part)
        return {'site': site, 'folder': "".join(page).strip()}

    def extract_page(self, url):
        page = requests.get(url, headers=self.headers, timeout=self.timeout)

        if page.status_code != 200:
            raise Exception(f"Page Not Found {page.status_code}")
        return BeautifulSoup(page.text, 'html.parser')

    def extract_images(self, html):
        images = []
        for image in html.findAll('img'):
            src = image.get('src')
            if src.rsplit('.')[-1] in self.allowed:
                image_src = src
                filename = src.split('/')[-1]
                images.append({'link': image_src, 'filename': filename})
        return images

    def download_image(self, fpath, link):
        res = requests.get(link, headers=self.headers, timeout=self.timeout)
        if res.status_code != 200:
            raise Exception(f'Fetch Error, code: {res.status_code}')

        print(f'Downloading {fpath}...')
        if os.path.exists(fpath):
            print('Image already downloaded, skipping...')
            return
        with open(fpath, 'wb') as f:
            response = requests.get(link, allow_redirects=True, stream=True)
            total_size = response.headers.get('content-length')
            if not total_size:
                f.write(response.content)
            else:
                dl = 0
                total_size = int(total_size)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_size)
                    sys.stdout.write('\r[%s%s]' %
                                     ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()
            print('')

    def download_images_from_site(self, url):
        url_data = self.parse_url(url)
        html = self.extract_page(url)
        images = self.extract_images(html)

        base_path = os.path.abspath(os.path.join(
            self.download_path, url_data['site'], url_data['folder'])).rstrip('/')

        if not os.path.exists(base_path):
            os.makedirs(base_path)

        for image in images:
            fpath = f"{base_path}/{image['filename']}"
            self.download_image(fpath, image['link'])
