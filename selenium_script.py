from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import pymongo
from datetime import datetime
import requests

# Function to configure the WebDriver
def configure_driver(proxy=None):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless Chrome
    chrome_options.add_argument("--disable-gpu")  # Disable GPU
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')
    service = Service('/path/to/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to login to Twitter and fetch trending topics
def fetch_trending_topics(driver, username, password):
    driver.get('https://twitter.com/login')
    
    # Log in to Twitter
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "session[username_or_email]"))).send_keys(username)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "session[password]"))).send_keys(password + Keys.RETURN)
    
    # Wait for the home page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text()="What’s happening"]')))
    
    # Fetch the trending topics
    trending_elements = driver.find_elements(By.XPATH, '//section//span[text()="Trending now"]/following-sibling::div//span')
    trending_topics = [element.text for element in trending_elements[:5]]
    
    return trending_topics

# Function to get a new IP address from ProxyMesh
def get_new_proxy():
    proxy_api_url = "http://proxymesh.com/api/proxies"
    response = requests.get(proxy_api_url, auth=('your_proxymesh_username', 'your_proxymesh_password'))
    proxies = response.json()
    return proxies['data'][0]['proxy']

# Function to store data in MongoDB
def store_in_mongodb(trending_topics, ip_address):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["twitter_trends"]
    collection = db["trends"]
    
    data = {
        "trend1": trending_topics[0],
        "trend2": trending_topics[1],
        "trend3": trending_topics[2],
        "trend4": trending_topics[3],
        "trend5": trending_topics[4],
        "date_time": datetime.now(),
        "ip_address": ip_address
    }
    
    collection.insert_one(data)
    return data

# Main script
def main():
    # Twitter credentials
    username = "your_twitter_username"
    password = "your_twitter_password"
    
    # Get a new proxy
    proxy = get_new_proxy()
    
    # Configure the WebDriver
    driver = configure_driver(proxy)
    
    try:
        # Fetch trending topics
        trending_topics = fetch_trending_topics(driver, username, password)
        
        # Store the data in MongoDB
        data = store_in_mongodb(trending_topics, proxy)
        
        return data
    finally:
        driver.quit()

if __name__ == "__main__":
    result = main()
    print(result)
