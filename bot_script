import os
import time
import random
import openai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Charger les variables d'environnement
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurer l'API OpenAI
openai.api_key = OPENAI_API_KEY

# Configurer Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)

# Fonction pour générer un tweet avec hashtags populaires
def generate_tweet_with_hashtags():
    # Génération du tweet principal
    tweet_content = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a sarcastic, witty, and flirtatious woman who tweets about dating and relationships."},
            {"role": "user", "content": "Generate a short, sarcastic tweet about relationships, with a confident and seductive tone."}
        ],
        max_tokens=100
    )['choices'][0]['message']['content'].strip()

    # Génération des hashtags populaires
    hashtags = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert social media manager. Your task is to generate popular hashtags based on the tweet content."},
            {"role": "user", "content": f"Generate 3 to 5 popular and relevant hashtags for the tweet: '{tweet_content}'"}
        ],
        max_tokens=30
    )['choices'][0]['message']['content'].strip()

    # Ajouter les hashtags au tweet
    full_tweet = f"{tweet_content}\n\n{hashtags}"
    return full_tweet

# Se connecter à Twitter
def login_to_twitter():
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

# Publier un tweet
def post_tweet():
    tweet_content = generate_tweet_with_hashtags()
    driver.get("https://twitter.com/home")
    time.sleep(5)

    try:
        tweet_box = driver.find_element(By.XPATH, '//div[@data-testid="tweetTextarea_0"]')
        tweet_box.send_keys(tweet_content)
        time.sleep(2)

        tweet_button = driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]')
        tweet_button.click()
        print(f"Tweet posted: {tweet_content}")
        time.sleep(3)
    except Exception as e:
        print(f"Error posting tweet: {e}")

# Répondre à toutes les mentions
def reply_to_all_mentions():
    driver.get("https://twitter.com/notifications/mentions")
    time.sleep(5)

    mentions = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
    for mention in mentions:
        try:
            reply_button = mention.find_element(By.XPATH, './/div[@data-testid="reply"]')
            reply_button.click()
            time.sleep(2)

            reply_box = driver.find_element(By.XPATH, '//div[@data-testid="tweetTextarea_0"]')
            reply_content = generate_tweet_with_hashtags()
            reply_box.send_keys(reply_content)
            driver.find_element(By.XPATH, '//div[@data-testid="tweetButton"]').click()
            print(f"Replied to mention with: {reply_content}")
            time.sleep(3)
        except Exception as e:
            print(f"Error replying to mention: {e}")

# Fonction principale
def run_bot():
    login_to_twitter()

    while True:
        post_tweet()
        reply_to_all_mentions()

        # Attendre entre 90 et 120 minutes avant la prochaine exécution
        wait_time = random.randint(5400, 7200)
        print(f"Waiting {wait_time / 60:.2f} minutes before next execution...")
        time.sleep(wait_time)

# Exécuter le bot
try:
    run_bot()
finally:
    driver.quit()
