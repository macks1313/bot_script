def test_simple_tweet():
    try:
        print("Navigating to Twitter login...")
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

        driver.get("https://twitter.com/home")
        time.sleep(5)

        tweet_box = driver.find_element(By.XPATH, '//div[@data-testid="tweetTextarea_0"]')
        tweet_box.send_keys("Manual test tweet from Selenium!")
        time.sleep(2)

        tweet_button = driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]')
        tweet_button.click()
        print("Manual test tweet posted successfully!")
        time.sleep(5)

    except Exception as e:
        print(f"Error in simple tweet test: {e}")
    finally:
        driver.quit()

# Exécuter le test
test_simple_tweet()

