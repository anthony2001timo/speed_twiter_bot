from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PROMISED_DOWN = 150
PROMISED_UP = 10
CHROME_DRIVER_PATH = "YOUR_CHROME_DRIVER_PATH"
TWITTER_EMAIL = "YOUR_TWITTER_EMAIL"
TWITTER_PASSWORD = "YOUR_TWITTER_PASSWORD"

class InternetSpeedTwitterBot:
    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        
        # Espera que el botón de inicio esté disponible y haz clic
        go_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".start-button a"))
        )
        go_button.click()

        # Espera a que termine la prueba de velocidad (60 segundos aprox)
        time.sleep(60)

        # Obtiene las velocidades de bajada y subida
        self.down = self.driver.find_element(
            By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div[2]/span'
        ).text
        self.up = self.driver.find_element(
            By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span'
        ).text

    def tweet_at_provider(self):
        self.driver.get("https://twitter.com/login")

        # Espera a que los campos de email y contraseña estén disponibles
        email = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        email.send_keys(TWITTER_EMAIL)
        email.send_keys(Keys.ENTER)

        time.sleep(2)  # Espera breve para evitar problemas de carga

        password = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password.send_keys(TWITTER_PASSWORD)
        password.send_keys(Keys.ENTER)

        # Componer y enviar el tweet
        tweet_compose = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[aria-label='Tweet text']")
            )
        )
        tweet = f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?"
        tweet_compose.send_keys(tweet)

        tweet_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="tweetButton"]'))
        )
        tweet_button.click()

        time.sleep(2)
        self.driver.quit()

# Ejecuta el bot
bot = InternetSpeedTwitterBot(CHROME_DRIVER_PATH)
bot.get_internet_speed()
bot.tweet_at_provider()
