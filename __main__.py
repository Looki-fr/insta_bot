from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from getpass import getpass
import os

class Internet:
    """

        Call the insta method to connect to instagram

        Args:
            username: str : username
            password: str : password
            number_of_followers : int : number of followers that you have
            number_of_follow : int : the number of people that you follow
 
        Attributes:
            driver.Selenium.webdriver.Chrome: the driver that is used to automate Chrome
        """

    def __init__(self, username, password, number_of_followers, number_of_follow):
        self.username = username
        self.password = password
        self.number_of_follow = number_of_follow
        self.number_of_followers = number_of_followers

        self.directory = os.path.dirname(os.path.realpath(__file__))

        self.driver = webdriver.Chrome(f'{self.directory}\\chromedriver.exe')

        time.sleep(1)

        self.insta()

    def insta(self):
        """
        method that will connect the Chrome to instagram and click to the differents pop ups such as 'accept cookies'
        
        """

        self.list_followers_string = []
        self.list_follow_string = []
        self.base_url = 'https://www.instagram.com/'

        self.driver.get(self.base_url)

        
        # wait until the element in parameter appears, with a maximum time of 10 secondes
        element = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div[2]/button[1]'))
        )


        self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/button[1]').click()

        

        # connect again to instagram because I had a bug if I didn't do this
        self.driver.get(f"{self.base_url}accounts/login/")


        # enter the username
        element = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'username'))
        )
        
        self.driver.find_element_by_name('username').send_keys(self.username)

        # enter the password
        element = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'password'))
        )

        self.driver.find_element_by_name('password').send_keys(self.password)


        # click to login button
        self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()

        # click on two pop ups
        element = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button'))
        )

        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()

        element = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div/div[3]/button[2]'))
        )

        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
            
    def list_followers(self):
        """ method that will go to the profile page to get the list of all your followers, and then check if the people that you follow follow you back, and if they don't, unfollow them.
        """

        # go to your profile page
        self.driver.get(f"https://www.instagram.com/{self.username}/")

        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a'))
        )

        # click to 'followers'
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a").click()

        time.sleep(1)

        list_followers = []

        # panel that will be use to scroll down
        followers_panel = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]') 

        # scroll down for every 8 followers that you have to load every followers
        for i in range(round(self.number_of_followers / 8 )):
            self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight + arguments[0].offsetHeight;",followers_panel
                )
            time.sleep(0.5)

        # put every followers 'href' in a list
        list_followers = self.driver.find_elements_by_xpath('//span/a[@href]')

        # put every pseudo of your followers in the self.list_followers_string
        for i in list_followers:
            self.list_followers_string.append(i.get_attribute("title"))

    def unfollow_non_followers(self):
        """ method that will unfollow all the people that don't follow you
        """

        # go to your profile page
        self.driver.get(f"https://www.instagram.com/{self.username}/")

        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a'))
        )

        # click to the button of all the people that you follow
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a').click()

        time.sleep(1)

        # panel that will be use to scroll down
        followers_panel = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]')

        # scroll down for every 8 follow that you have to load every follow
        for i in range(round(self.number_of_follow / 8 )):
            self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight + arguments[0].offsetHeight;",followers_panel
                )
            time.sleep(0.5)
        
        # put every 'href' of the people that you follow in a list
        list_follow = self.driver.find_elements_by_xpath('//span/a[@href]')

        # add their names in the self.list_follow_string list
        for i in list_follow:
            self.list_follow_string.append(i.get_attribute("title"))
        
        list_end = []

        # num will be the number of the person and person will be all the names that are in self.list_follow_string list (list of people that you follow)
        for num, person  in enumerate(self.list_follow_string):
            #if the guy / girl is not in your followers list, so if he/she don't follow you
            if person not in self.list_followers_string:
                
                # click to 'unfollow' button
                # if you got an error here replace div[3] by div[2] before /button[1] so you'll get : f'/html/body/div[5]/div/div/div[2]/ul/div/li[{num+1}]/div/div[2]/button'
                self.driver.find_element_by_xpath(f'/html/body/div[5]/div/div/div[2]/ul/div/li[{num+1}]/div/div[3]/button').click() 

                # confirm your choice while clicking on the confirmation button
                element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div/div[3]/button[1]'))
        )

                self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[3]/button[1]').click()
                time.sleep(20) # it'll be long but you don't want to get ban :)

if __name__ == '__main__':
    username = input("enter your username : ")
    password = getpass("enter your password (its normal if you don't see what you write): ")
    number_of_followers = int(input('Please enter your number of followers : '))
    number_of_follow = int(input('Please enter the number of people that you follow : '))
    browser = Internet(username, password, number_of_followers, number_of_follow) 
    browser.list_followers()
    browser.unfollow_non_followers()
