import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Charger les variables d'environnement
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")

# Configurer Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugging-port=9222")

# Initialiser le driver Selenium
try:
    driver = webdriver.Chrome(options=options)
    print("Selenium driver initialized successfully.")
except Exception as e:
    print(f"Error initializing Selenium driver: {e}")
    exit(1)

def test_twitter_login_and_tweet():
    try:
        print("Navigating to Twitter login page...")
        driver.get("https://twitter.com/login")
        time.sleep(5)

        print("Entering username...")
        username_field = driver.find_element(By.NAME, "text")
        username_field.send_keys(TWITTER_USERNAME)
        username_field.send_keys(Keys.RETURN)
        time.sleep(3)

        print("Entering password...")
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(TWITTER_PASSWORD)
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)

        print("Login successful! Navigating to home page...")
        driver.get("https://twitter.com/home")
        time.sleep(5)

        print("Attempting to post a test tweet...")
        tweet_box = driver.find_element(By.XPATH, '//div[@data-testid="tweetTextarea_0"]')
        tweet_box.send_keys("This is a test tweet from Selenium!")
        time.sleep(2)

        tweet_button = driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]')
        tweet_button.click()
        print("Test tweet posted successfully!")
        time.sleep(5)

    except Exception as e:
        print(f"Error during test: {e}")
    finally:
        print("Shutting down Selenium driver...")
        driver.quit()

# Exécuter le test
test_twitter_login_and_tweet()

# Garder le processus actif
print("Entering idle loop to keep the process alive...")
while True:
    time.sleep(600)  # Garder la boucle active en attendant 10 minutes à chaque itération
