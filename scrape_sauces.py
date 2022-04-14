from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from datetime import timedelta
import os
import io
import requests
from PIL import Image

opt = Options()

# Un-Comment Below options
# To run Browser on Background 

# opt.add_argument("--headless")
# opt.add_argument("--no-sandbox")
# opt.add_argument("--disable-dev-shm-usage")

# Ad-Blocker Extension 
opt.add_extension("/opt/google/chrome/AdBlock-—-best-ad-blocker.crx")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=opt)

def manga_sauce (sauce):

    web = 'https://nhentai.to/g/'+str(sauce)

    driver.get(web)

    start_time = time.time()


    manga_title = driver.find_element(By.TAG_NAME,"h1").text
    # print(manga_title)

    filename = os.path.join("manga_sauces", str(sauce))
    if not os.path.exists(filename):
        os.makedirs(filename)

    manga_container = driver.find_element(By.CLASS_NAME,"thumb-container").click()
    driver.implicitly_wait(10)
    image = []

    def manga_image():

        manga_image_container = driver.find_element(By.XPATH,".//section[@id='image-container']/a/img")

        manga_image_src = manga_image_container.get_attribute("src")

        try:
            manga_content = requests.get(manga_image_src).content
        except Exception as e:
            print("Error on getting image content",e)
        
        try:
            manga_byte = io.BytesIO(manga_content)
            manga_image = Image.open(manga_byte)
            image.append(manga_image)
        except Exception as e:
            print("Error on Downloading images",e)

    while True:
        manga_image()
        try:
            # next_page = driver.find_element(By.CLASS_NAME,"next").click()
            # next_page = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME,"next"))).click()
            next_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"next"))).click()
        except:
            break

    file = os.path.join(filename,str(sauce) +".pdf")
    with open(file,"wb") as f:
        image[0].save(f,save_all=True,append_images=image[1:])

    end_time = time.time()
    time_taken = round(end_time - start_time,10)
    
    print(f"The Manga {manga_title} sauce {sauce} Download is Completed")
    print(f"The time take to download manga {manga_title} is {timedelta(seconds=time_taken)}")
    print(" ")

    driver.implicitly_wait(10)  

# Download a Single Manga use function 
# To run program for 1 time

# manga_sauce(390044)

# To Downlaod a List of manga use list 
# To add all sauces 
# for loop to download all manga

sauce_list = [289060,246408,236707]

for sauce_number in sauce_list:
    manga_sauce(sauce_number)
driver.quit()