import requests
import os
import time
from bs4 import BeautifulSoup

url = "https://www.msijanakpuri.com/faculty/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"Failed to fetch the page. Status code: {response.status_code}")
    exit()

soup = BeautifulSoup(response.content, "html.parser")

output_directory = "images"  
os.makedirs(output_directory, exist_ok=True)

faculty_wrappers = soup.find_all("div", class_="msi-team-item-wrapper")

counter = 1

for wrapper in faculty_wrappers:
    faculty_items = wrapper.find_all("div", class_="msi-team-item")
    
    for item in faculty_items:
        image_element = item.select_one(".msi-team-item-image img[src]")
        if image_element is None:
            continue  # Skip faculty item without an image

        image_url = image_element["src"]
        faculty_name = item.find("div", class_="msi-team-item-title").text.strip()

        image_response = requests.get(image_url, headers=headers)

        if image_response.status_code == 200:
            filename = os.path.join(output_directory, f"{counter}_{faculty_name}.jpg")
            with open(filename, "wb") as f:
                f.write(image_response.content)
            print(f"Downloaded image for faculty: {faculty_name}")
            counter += 1
        else:
            print(f"Failed to download image for faculty: {faculty_name}")

        time.sleep(1)
