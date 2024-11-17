from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests
import time

keywords = [
    "coffee", "phone", "keyboard", "shirt", "pant", "laptop", "watch", "headphones", "speaker", "camera",
    "tablet", "charger", "cable", "bag", "wallet", "sneakers", "socks", "hat", "glasses", "jacket",
    "jeans", "mouse", "monitor", "television", "fridge", "microwave", "vacuum", "toaster", "blender", "grill",
    "oven", "stove", "freezer", "dishwasher", "mixer", "airfryer", "fan", "heater", "airpods", "projector",
    "tripod", "backpack", "suitcase", "dress", "boots", "sandals", "scarf", "belt", "tie", "umbrella",
    "perfume", "makeup", "lotion", "shampoo", "conditioner", "soap", "toothbrush", "toothpaste", "razor", "shaver",
    "towel", "blanket", "pillow", "mattress", "bed", "sofa", "chair", "table", "desk", "lamp",
    "mirror", "vase", "clock", "frame", "curtains", "rug", "cushion", "bookshelf", "wardrobe", "dresser",
    "bicycle", "skateboard", "helmet", "scooter", "treadmill", "weights", "dumbbell", "yoga", "meditation", "protein",
    "supplement", "vitamin", "energy", "hydration", "snack", "chocolate", "cookie", "juice", "soda", "tea",
    "water", "wine", "beer", "whiskey", "vodka", "rum", "gin", "cider", "champagne", "pizza",
    "burger", "pasta", "salad", "soup", "sushi", "taco", "sandwich", "steak", "chicken", "seafood",
    "cereal", "bread", "butter", "cheese", "egg", "milk", "yogurt", "fruit", "vegetable", "meat",
    "rice", "pasta", "oil", "sauce", "spice", "salt", "pepper", "sugar", "honey", "jam",
    "chips", "nuts", "candy", "popcorn", "cracker", "biscuit", "flour", "cake", "cookie", "icecream",
    "chocolate", "syrup", "pancake", "waffle", "bacon", "ham", "sausage", "tofu", "pasta", "lasagna",
    "noodle", "wrap", "smoothie", "milkshake", "muffin", "croissant", "donut", "brownie", "pastry", "pudding",
    "tea", "coffee", "juice", "smoothie", "shake", "water", "soda", "milk", "lemonade", "mojito",
    "sweater", "blouse", "shorts", "trousers", "cap", "beanie", "gloves", "jacket", "hoodie", "vest",
    "mask", "gown", "tunic", "robe", "shoes", "boots", "heels", "flats", "loafers", "flipflops"
]




options = webdriver.ChromeOptions()
options.add_argument("--headless=old")
driver = webdriver.Chrome(options=options)


def scroll_page():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  

downloaded_captions = []

if not os.path.exists('downloaded_images'):
    os.makedirs('downloaded_images')
else:
    for folder_name in sorted(os.listdir('downloaded_images')):
        folder_path = os.path.join('downloaded_images', folder_name)
        
        if folder_name.isdigit() and os.path.isdir(folder_path):
            
            captions_file_path = os.path.join(folder_path, "captions.txt")
        
            
            if os.path.exists(captions_file_path):
                
                with open(captions_file_path, 'r', encoding='utf-8') as file:
                    caption = file.read().strip()
                    downloaded_captions.append(caption)
    
    

totalDownloaded = 0

for keyword in keywords:
    print(f"Processing keyword: {keyword}")

    
    driver.get(f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&content_languages[0]=en&country=US&media_type=image_and_meme&q=%22{keyword}%22&search_type=keyword_exact_phrase")

    
    wait = WebDriverWait(driver, 20)
    first_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".x1dr75xp.xh8yej3.x16md763"))
    )

    parent_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".xrvj5dj.xdq2opy.xexx8yu.xbxaen2.x18d9i69.xbbxn1n.xdoe023.xbumo9q.x143o31f.x7sq92a.x1crum5w"))
    )

    
    processed_divs = set()
    currentDownloaded = 0

    
    caption_limit = 25

    while currentDownloaded < caption_limit:
        main_divs = parent_element.find_elements(By.XPATH, "./*[contains(@class, 'xh8yej3')]")

        for main_div in main_divs:
            if main_div in processed_divs:
                continue

            try:
                processed_divs.add(main_div)
                nested_div = WebDriverWait(main_div, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "xh8yej3"))
                )
                if len(nested_div) >= 6:
                    final_div = nested_div[5]
                else:
                    print("Final div doesn't exist")
                    continue

                target_div = WebDriverWait(final_div, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.x6ikm8r.x10wlt62'))
                )

                img_tag = WebDriverWait(target_div, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'img'))
                )

                outer_span = WebDriverWait(target_div, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'span.x8t9es0.xw23nyj.xo1l8bm.x63nzvj.x108nfp6.xq9mrsl.x1h4wwuj.xeuugli'))
                )

                caption_tag = WebDriverWait(outer_span, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'span'))
                )

                img_url = img_tag.get_attribute('src')
                caption = caption_tag.text.strip()

                if not caption:
                    print("Blank caption")
                    continue

                if caption not in downloaded_captions:
                    downloaded_captions.append(caption)
                    currentDownloaded += 1
                    totalDownloaded += 1
                    
                    directory_path = f"downloaded_images/{totalDownloaded}"

                    if not os.path.exists(directory_path):
                        os.makedirs(directory_path)

                    img_data = requests.get(img_url).content
                    img_filename = f"downloaded_images/{totalDownloaded}/img.jpg"
                    with open(img_filename, 'wb') as img_file:
                        img_file.write(img_data)


                    with open(f"downloaded_images/{totalDownloaded}/caption.txt", 'w', encoding='utf-8') as caption_file:
                        caption_file.write(caption)

                    print(f"Downloaded {currentDownloaded}/{caption_limit} images/captions for keyword: {keyword}")

                    
                        

                    if currentDownloaded >= caption_limit:
                        break

            except Exception as e:
                print("Error processing div")

        scroll_page()

driver.quit()
