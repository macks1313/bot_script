def test_twitter_login_and_tweet():
    try:
        print("Navigating to Twitter login page...")
        driver.get("https://twitter.com/login")
        time.sleep(5)

        print("Entering username...")
        username_field = driver.find_element(By.NAME, "text")
        if username_field:
            print("Username field found.")
        username_field.send_keys(TWITTER_USERNAME)
        username_field.send_keys(Keys.RETURN)
        time.sleep(3)

        print("Entering password...")
        password_field = driver.find_element(By.NAME, "password")
        if password_field:
            print("Password field found.")
        password_field.send_keys(TWITTER_PASSWORD)
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)

        # Vérification de l'URL actuelle
        current_url = driver.current_url
        print(f"Current URL after login: {current_url}")

        driver.save_screenshot("/tmp/twitter_login_debug.png")
        print("Screenshot saved.")

        if "home" not in current_url:
            print("Login failed or additional verification required.")
            return

        print("Successfully logged in. Navigating to home page...")
        driver.get("https://twitter.com/home")
        time.sleep(5)

        print("Finding tweet box...")
        tweet_box = driver.find_element(By.XPATH, '//div[@data-testid="tweetTextarea_0"]')
        if tweet_box:
            print("Tweet box found.")
        tweet_box.send_keys("This is a test tweet from Selenium.")
        time.sleep(2)

        print("Clicking tweet button...")
        tweet_button = driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]')
        if tweet_button:
            print("Tweet button found.")
        tweet_button.click()
        print("Tweet posted successfully!")

    except Exception as e:
        print(f"Error during test: {e}")
    finally:
        print("Shutting down Selenium driver...")
        driver.quit()
