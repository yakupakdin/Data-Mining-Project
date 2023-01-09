# region Libraries/Modules

import bs4
import requests
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
import os
import time

# endregion

# region Functions


def scroll_down_and_up(web_driver, scroll_time):

    SCROLL_PAUSE_TIME = scroll_time

    # Get scroll height
    last_height = web_driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = web_driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Scroll up to top once it's done
    web_driver.execute_script("window.scrollTo(0, 0);")


def download_image(url, dir_name, num):
    file_name = str(num) + '.jpg'
    response = requests.get(url)
    # status code 200 means OK status for HTTP response
    if response.status_code == 200:
        # os.path.join(dir_name, file_name) -> output string => dir_name/num.jpg, wb = write binary
        with open(os.path.join(dir_name, file_name), 'wb') as file:
            # write the image data to the file
            file.write(response.content)


def create_a_directory(path):
    """Creating a directory if it doesn't exist

    :param str path: path of the directory in string format
    :return: None
    """

    # Creating a directory to save images
    if not os.path.isdir(path):
        os.makedirs(path)


# endregion

search_URL = "kmsdgnkadfgınk"
path_to_folder_to_create = r"C:\Users\YakupAkdin\PycharmProjects\VeriMadenciligi1\dataset\kemence"
create_a_directory(path_to_folder_to_create)


# region Opera WebDriver Path for Selenium to use

chromeDriverPath = "C:\\Users\\YakupAkdin\\PycharmProjects\\chromedriver.exe"

# endregion
options = webdriver.ChromeOptions()
options.add_experimental_option('w3c', True)

# Creating an instance of Service class
webdriver_service = service.Service(chromeDriverPath)

# Starting the service
webdriver_service.start()


driver = webdriver.Remote(webdriver_service.service_url, options=options)

# The browser will open up and close itself (you're gonna need a sleep() method to see it properly)
driver.get(search_URL)

# To start the script
a = input('Waiting for user input to start...')


# Invoking the scroll_down_and_up() function
scroll_down_and_up(driver, 2)

# Sending all of the HTML code into this variable named called "page_html"
page_html = driver.page_source

# Parsing the HTML code
pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')

# Finding all "div" tags with class attribute below in given HTML code
containers = pageSoup.find_all('div', {'class': 'isv-r PNCib MSM1fd BUooTd'})

# Printing how many containers we have found so far with beautifulsoup
len_containers = len(containers)
print(f"Found {len_containers} image containers")


# Google Görseller'deki resim kaplarına tıklamak
downloaded_images = 0
# her 25 öğede bir resim olmayan bir container olduğu için onu atlayacağız.
for i in range(1, len_containers + 1):
    if i % 25 == 0:
        continue

    xPath = f"""//*[@id="islrg"]/div[1]/div[{i}]"""

    # region Waiting for high resolution images to load

    # küçük resmin selector özelliği ile src değerini çekiyoruz.
    previewImageXpath = f"""//*[@id="islrg"]/div[1]/div[{i}]/a[1]/div[1]/img"""
    try:
        previewImageElement = driver.find_element(by=By.XPATH, value=previewImageXpath)
        previewImageURL = previewImageElement.get_attribute("src")
    except selenium.common.exceptions.NoSuchElementException:
        print("No preview image found!")
        continue

    # Clicking on the image container
    driver.find_element(by=By.XPATH, value=xPath).click()
    download_status = False
    # Starting a while True loop to wait until the URL inside the large image view is different from the preview one
    timeStarted = time.time()
    while True:
        imageElement = driver.find_element(
            by=By.XPATH,
            value=f""" //*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img""")
        imageURL = imageElement.get_attribute("src")

        # print('waiting for the full resolution image')
        if imageURL != previewImageURL:

            download_status = True
            break

        else:
            # Making a timeout if the full res image can't be loaded
            currentTime = time.time()

            if (currentTime - timeStarted) > 10:
                print("Timeout!")
                break

    # Downloading the image
    try:
        if download_status:
            downloaded_images += 1
            download_image(imageURL, path_to_folder_to_create, downloaded_images)
            print(f"Downloaded element {downloaded_images} out of {len_containers} <----> URL: {imageURL}")

    except:
        print(f"Couldn't download element {i} out of {len_containers}.")

    # endregion

# endregion





print("Bitti")
print(f"Downloaded {downloaded_images} out of {len_containers} images!")
driver.quit()
webdriver_service.stop()
