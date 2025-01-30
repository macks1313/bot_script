import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Charger les variables d'environnement
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")

# Déclaration globale du driver Selenium
driver = None

def initialize_driver():
    global driver
    print("Initializing Selenium driver...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")

    try:
        driver = webdriver.Chrome(options=options)
        print("Selenium driver initialized successfully.")
    except Exception as e:
        print(f"Error initializing Selenium driver: {e}")
        exit(1)

def log_with_screenshot(stage_name):
    print(f"Log stage: {stage_name}")
    driver.save_screenshot(f"/tmp/{stage_name}.png")
    print(f"Screenshot saved for stage: {stage_name}")

def test_simple_tweet():
    global driver
    try:
        print("Navigating to Twitter login...")
        driver.get("https://twitter.com/login")
        time.sleep(5)
        log_with_screenshot("login_page")

        print("Entering username...")
        username_field = driver.find_element(By.NAME, "text")
        username_field.send_keys(TWITTER_USERNAME)
        username_field.send_keys(Keys.RETURN)
        time.sleep(3)
        log_with_screenshot("after_username")

        print("Entering password...")
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(TWITTER_PASSWORD)
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)
        log_with_screenshot("after_password")

        # Vérification de l'URL après la connexion
        current_url = driver.current_url
        print(f"Current URL after login: {current_url}")

        if "home" not in current_url:
            print("Login failed or verification required.")
            log_with_screenshot("login_failed")
            return

        print("Login successful! Navigating to home page...")
        driver.get("https://twitter.com/home")
        time.sleep(5)
        log_with_screenshot("home_page")

        print("Attempting to post a tweet...")
        tweet_box = driver.find_element(By.XPATH, '//div[@data-testid="tweetTextarea_0"]')
        tweet_box.send_keys("Manual test tweet from Selenium!")
        time.sleep(2)
        log_with_screenshot("tweet_box_filled")

        print("Clicking tweet button...")
        tweet_button = driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]')
        tweet_button.click()
        print("Test tweet posted successfully!")
        log_with_screenshot("tweet_posted")
        time.sleep(5)

    except Exception as e:
        print(f"Error in simple tweet test: {e}")
        log_with_screenshot("error_occurred")
    finally:
        print("Shutting down Selenium driver...")
        driver.quit()

# Initialiser le driver et exécuter le test
initialize_driver()
test_simple_tweet()

# Garder le processus actif
print("Entering idle loop to keep the process alive...")
while True:
    time.sleep(600)

