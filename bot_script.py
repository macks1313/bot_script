import os
import time
import random
import openai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Charger les variables d'environnement
print("Loading environment variables...")
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Vérification des variables d'environnement
if not TWITTER_USERNAME:
    print("Error: Missing TWITTER_USERNAME environment variable.")
    exit(1)
if not TWITTER_PASSWORD:
    print("Error: Missing TWITTER_PASSWORD environment variable.")
    exit(1)
if not OPENAI_API_KEY:
    print("Error: Missing OPENAI_API_KEY environment variable.")
    exit(1)

# Configurer l'API OpenAI
print("Initializing OpenAI API...")
openai.api_key = OPENAI_API_KEY

# Configurer Selenium
print("Configuring Selenium...")
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

# Fonction pour générer un tweet avec hashtags
def generate_tweet_with_hashtags():
    print("Generating tweet content...")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a witty and sarcastic woman who tweets about relationships."},
                {"role": "user", "content": "Generate a short sarcastic tweet with a seductive tone."}
            ],
            max_tokens=100
        )
        tweet_content = response.choices[0].message["content"].strip()

        print("Generating hashtags...")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Generate relevant hashtags for the following tweet."},
                {"role": "user", "content": tweet_content}
            ],
            max_tokens=30
        )
        hashtags = response.choices[0].message["content"].strip()
        return f"{tweet_content}\n\n{hashtags}"
    except Exception as e:
        print(f"Error generating tweet or hashtags: {e}")
        return ""

# Fonction de connexion à Twitter
def login_to_twitter():
    print("Logging in to Twitter...")
    try:
        driver.get("https://twitter.com/login")
        time.sleep(5)

        username_field = driver.find_element(By.NAME, "text")
        username_field.send_keys(TWITTER_USERNAME)
        username_field.send_keys(Keys.RETURN)
        time.sleep(3)

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(TWITTER_PASSWORD)
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)
        print("Successfully logged in to Twitter.")
    except Exception as e:
        print(f"Error during Twitter login: {e}")
        exit(1)

# Fonction pour publier un tweet
def post_tweet():
    print("Posting tweet...")
    tweet_content = generate_tweet_with_hashtags()
    if not tweet_content:
        print("No tweet content generated.")
        return

    try:
        print("Navigating to Twitter home...")
        driver.get("https://twitter.com/home")
        time.sleep(5)

        print("Finding tweet box...")
        tweet_box = driver.find_element(By.XPATH, '//div[@data-testid="tweetTextarea_0"]')
        tweet_box.send_keys(tweet_content)
        time.sleep(2)

        print("Clicking the tweet button...")
        tweet_button = driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]')
        tweet_button.click()
        print(f"Tweet posted successfully: {tweet_content}")
        time.sleep(3)
    except Exception as e:
        print(f"Error posting tweet: {e}")

# Fonction principale
def run_bot():
    print("Starting bot execution...")

    # Connexion à Twitter
    login_to_twitter()

    # Publier immédiatement un premier tweet
    print("Posting initial tweet...")
    post_tweet()

    # Entrer dans une boucle pour publier régulièrement des tweets
    while True:
        print("Running tweet cycle...")
        post_tweet()

        # Attendre entre 90 et 120 minutes avant la prochaine exécution
        wait_time = random.randint(5400, 7200)
        print(f"Waiting {wait_time / 60:.2f} minutes before next tweet...")
        time.sleep(wait_time)

# Exécuter le bot
try:
    run_bot()
finally:
    print("Shutting down Selenium driver...")
    driver.quit()
