import os
from image_scrapper import ImageScrapper
from selenium_scrapping import FirefoxScrapper

urls = [

]

scrapper = ImageScrapper()
print("############### Downloading ######################")
for url in urls:
    scrapper.download_images_from_site(url)

print("############### Finished ######################")


# firefox = FirefoxScrapper()
# firefox.scrappe(url)
