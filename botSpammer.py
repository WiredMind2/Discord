# Ecrit ton programme ici ;-)
from selenium import webdriver
from time import sleep


class BotSpammer:
    def __init__(self):
        self.driver = webdriver.Firefox(
            executable_path=("C:/Program Files/geckodriver/geckodriver.exe")
        )
        self.driver.implicitly_wait(15)

        self.xPth = lambda e: self.driver.find_element_by_xpath(e)

    def create_bot(self):
        self.driver.get("https://discord.com/")

        self.xPth("/html/body/div/div/div/div[1]/div[2]/div/div[2]/button").click()
        sleep(0.5)
        self.xPth("/html/body/div/div/div/div[1]/div[2]/div/div[2]/form/input").send_keys(self.get_username())
        sleep(0.5)
        self.xPth("/html/body/div/div/div/div[1]/div[2]/div/div[2]/form/button").click()

        sleep(2)
        self.xPth('//*[@id="react-select-2-input"]').send_keys("24")
        sleep(0.5)
        self.xPth('//*[@id="react-select-3-input"]').send_keys("décembre")
        sleep(0.5)
        self.xPth('//*[@id="react-select-4-input"]').send_keys("2004")

        sleep(1)
        self.xPth('/html/body/div/div[6]/div[2]/div/div/div[2]/div/div/div/form/div[4]/div/button').click()

    def get_username(self):
        return "Megacraft97421"

bot = BotSpammer()
bot.create_bot()
input("Stop?")