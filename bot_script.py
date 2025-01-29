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
options.add_argument("--headless")  # Exécution sans interface graphique
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugging-port=9222")

# Initialiser le driver sans chemins explicites
driver = webdriver.Chrome(options=options)

# Fonction pour générer un tweet avec hashtags
def generate_tweet_with_hashtags():
    tweet_content = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a witty and sarcastic woman who tweets about relationships."},
            {"role": "user", "content": "Generate a short sarcastic tweet with a seductive tone."}
        ],
        max_tokens=100
    )['choices'][0]['message']['content'].strip()

    hashtags = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Generate relevant hashtags for the following tweet."},
            {"role": "user", "content": tweet_content}
        ],
        max_tokens=30
    )['choices'][0]['message']['content'].strip()

    return f"{tweet_content}\n\n{hashtags}"

# Fonction de connexion à Twitter
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

# Fonction pour publier un tweet
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

# Fonction pour répondre à toutes les mentions
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

