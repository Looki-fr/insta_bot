from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import time
from getpass import getpass
import os
import random

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

    def __init__(self, username, password, number_of_followers=0, number_of_follow=0):
        self.username = username
        self.password = password
        self.number_of_follow = number_of_follow
        self.number_of_followers = number_of_followers
        self.t1 = 0
        self.number_scroll = 0
        self.lang = 'fr'

        self.directory = os.path.dirname(os.path.realpath(__file__))

        self.driver = webdriver.Chrome(f'{self.directory}\\chromedriver.exe')

        time.sleep(1)

        self.insta()

    def insta(self):
        """
        method that will connect the Chrome to instagram and click to the differents pop ups such as 'accept cookies'
        
        """
        self.tags_before = [
            "spicymemes",
            "memes",
            "funny",
            "originalmeme",
            "weirdmemes",
            "meme",
            "dank",
            "funnyvideos",
            "funnymemes",
            "funnymeme",
            "funnyshit"
        ]

        self.tags_after = []
        for i in self.tags_before:
            self.tags_after.append(i)

        self.banned_tag = [
            "https://www.instagram.com/explore/tags/beauty/",
            "https://www.instagram.com/explore/tags/fashion/",
            "https://www.instagram.com/explore/tags/nsfw/",
            "https://www.instagram.com/explore/tags/luxury/",
            "https://www.instagram.com/explore/tags/pretty/",
            "https://www.instagram.com/explore/tags/fashionblogger/",
            "https://www.instagram.com/explore/tags/nasty/",
            "https://www.instagram.com/explore/tags/nastyfreak/",
            "https://www.instagram.com/explore/tags/fit/",
            "https://www.instagram.com/explore/tags/girlsexy/",
            "https://www.instagram.com/explore/tags/beautifulgirls/",
            "https://www.instagram.com/explore/tags/yummy/",
            "https://www.instagram.com/explore/tags/photogirl/",
            "https://www.instagram.com/explore/tags/sexy/",
            "https://www.instagram.com/explore/tags/-18/"
        ]

        self.list_followers_string = []
        self.list_follow_string = []
        self.base_url = 'https://www.instagram.com/'

        self.driver.get(self.base_url)

        try:
            #will accept the cookies if we need to
            # wait until the element in parameter appears, with a maximum time of 10 secondes
            element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div[2]/button[1]'))
            )


            self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/button[1]').click()
        except:
            pass
     

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

        # scroll down for every 5 followers that you have to load every followers
        for i in range(round(self.number_of_followers / 5 )):
            self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight + arguments[0].offsetHeight;",followers_panel
                )
            time.sleep(0.2)

        # put every followers 'href' in a list
        list_followers = self.driver.find_elements_by_xpath('//span/a[@href]')

        # put every pseudo of your followers in the self.list_followers_string
        for i in list_followers:
            self.list_followers_string.append(i.get_attribute("title"))

    def unfollow_non_followers(self):
        """ method that will unfollow all the people that don't follow you
        """

        self.list_followers()

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
        for i in range(round(self.number_of_follow / 5 )):
            self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight + arguments[0].offsetHeight;",followers_panel
                )
            time.sleep(0.2)
        
        # put every 'href' of the people that you follow in a list
        list_follow = self.driver.find_elements_by_xpath('//span/a[@href]')  

        # add their names in the self.list_follow_string list
        for i in list_follow:
            self.list_follow_string.append(i.get_attribute("title"))
        
        list_end = []

        # num will be the number of the person and person will be all the names that are in self.list_follow_string list (list of people that you follow)
        for num, person  in enumerate(self.list_follow_string):
            #if the guy / girl is not in your followers list, so if he/she don't follow you
            if person not in self.list_followers_string and not person in self.white_list:
                # click to 'unfollow' button
                # if you got an error here replace div[3] by div[2] before /button[1] so you'll get : f'/html/body/div[5]/div/div/div[2]/ul/div/li[{num+1}]/div/div[2]/button'
                self.driver.find_element_by_xpath(f'/html/body/div[5]/div/div/div[2]/ul/div/li[{num+1}]/div/div[2]/button').click() 
                
                # confirm your choice while clicking on the confirmation button
                element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div/div[3]/button[1]')) 
        )

                self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[3]/button[1]').click()
                time.sleep(5)

    def follow_back(self):
        self.driver.get(f"https://www.instagram.com/{self.username}/")

        #click to the little hearth (to our news fill)

        element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[4]/a')) 
        )

        
        self.driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[4]/a').click()

        #click to the arrow, where we'll see all the people that want to follow us

        element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[4]/div/div[2]/div[2]/div/div/div/div/div[1]/div[3]/div/div')) 
        )

        self.driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[4]/div/div[2]/div[2]/div/div/div/div/div[1]/div[3]/div/div').click()
       
        followers_panel = self.driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[4]/div/div[2]/div[2]/div')

        # scroll down
        for i in range(10):
            self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight + arguments[0].offsetHeight;",followers_panel
                )
            time.sleep(0.2)
        #get all the confirms button
        buttons = self.driver.find_elements_by_xpath("//*[contains(text(), 'Confirmer')]") #replace Confirmer (Confirm in english) by the text that have the confirm button in your language
        num = 0
        finish = False

        for button in buttons:
            while not finish:
                try:
                    button.click()
                    time.sleep(1)
                    self.driver.find_element_by_xpath(f'/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[4]/div/div[2]/div[2]/div/div/div[1]/div/div[{num+1}]/div[3]/div/button').click()
                    finish = True
                    time.sleep(1)

                except:
                    num +=1

            finish = False
            num +=1

    def random_pic(self):
        """ function that choose a random picture that we did'nt like yet
        """
        if self.number_scroll > 0:
            row = random.randint(7,12)
        else:
            row = random.randint(1,6)
        column = random.randint(1,3)
        if tuple((row, column)) in self.picture:
            while tuple((row, column)) in self.picture:
                row = random.randint(1,4)
                column = random.randint(1,3)
        self.row = row
        self.column = column
        self.picture.append((row, column))

    def find_picture(self):
        banned = False
        self.random_pic()
        seconde = random.randint(7,15)
        try:
            self.driver.find_element_by_xpath(f'//*[@id="react-root"]/section/main/article/div[2]/div/div[{self.row}]/div[{self.column}]/a/div').click()
            time.sleep(seconde)
            tag = self.driver.find_elements_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span/a')
            try:
                for i in tag:
                    if i.get_attribute('href') in self.banned_tag:
                        banned = True
                if not banned:
                    self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[1]/button').click()
                    if random.randint(1,2) > 1:
                        self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()
            finally:
                time.sleep(5)
                self.driver.find_element_by_xpath('/html/body/div[5]/div[3]/button').click()
        except:
            pass

    def like_picture(self, tag):
        self.picture = []

        self.driver.get(f'{self.base_url}explore/tags/{tag}/?hl={self.lang}')

        time.sleep(5)

        t2 = time.time()

        while t2 < self.t1:
            time.sleep(2)
            if len(self.picture) > 4:
                actions = ActionChains(self.driver)
                actions.send_keys(Keys.SPACE).perform()
                ctions = ActionChains(self.driver)
                actions.send_keys(Keys.SPACE).perform()

                time.sleep(2)
            
                actions = ActionChains(self.driver)
                actions.send_keys(Keys.SPACE).perform()
                ctions = ActionChains(self.driver)
                actions.send_keys(Keys.SPACE).perform()

                time.sleep(2)
            
                actions = ActionChains(self.driver)
                actions.send_keys(Keys.SPACE).perform()
                ctions = ActionChains(self.driver)
                actions.send_keys(Keys.SPACE).perform()

                time.sleep(2)
            
                actions = ActionChains(self.driver)
                actions.send_keys(Keys.SPACE).perform()
                ctions = ActionChains(self.driver)
                actions.send_keys(Keys.SPACE).perform()

                time.sleep(2)

                self.number_scroll += 1
                self.picture = []
            self.find_picture()
            t2 = time.time()

    def random_likes_follow(self):
        self.t1 = time.time() + random.randint(165,323) #t1 + between 3 and 5 minutes its not round numbers because i want it unpredictable

        choice_tag = random.randint(0,len(self.tags_after)-1)
        choice = self.tags_after[choice_tag]
        del self.tags_after[choice_tag] # so you'll not go twice to the same tag

        self.like_picture(choice)

    def long_time_running(self):  
        time_init = time.time()

        number_iteration = random.randint(1,2)
        print(number_iteration)

        for i in range(number_iteration):
            self.random_likes_follow()
            time.sleep(5)

        self.driver.get('https://www.google.com') #we leave instagram
        self.number_scroll = 0

        while time.time() < time_init + random.randint(1100, 1400):# between 18 and 23 minutes
            time.sleep(1) #so it will not be laggy 
        
        self.insta()

        number_iteration = random.randint(1,2)

        for i in range(number_iteration):
            self.random_likes_follow()
            time.sleep(1)

        self.driver.get('https://www.google.com') #we leave instagram
    

if __name__ == '__main__':
    sentence="""
    Please read the readme.md file before :)

    1 : just connect to your instagram account
    2 : to unfollow all the people that don't follow you
    3 : like pictures and follow people during around 4 minutes of a random tag
    4 : let the bot do the same as the number '3' but more ! during between around 4 and 8 minutes, 2 times, separated by around 20 minutes of wait
    5 : will do the same as number '3' but you'll enter a specific tag
    6 : the bot will follow all the people that recently followed you

    your input : """
    
    choice = input(sentence)

    if choice == '1' or choice == '3' or choice == '4' or choice == '6':
        username = input("enter your username : ")
        password = getpass("enter your password (its normal if you don't see what you write): ")
        number_of_follow = 0
        number_of_followers = 0
        browser = Internet(username, password, number_of_followers, number_of_follow) 
    if choice == '2':
        username = input("enter your username : ")
        password = getpass("enter your password (its normal if you don't see what you write): ")
        number_of_followers = int(input('Please enter your number of followers : '))
        number_of_follow = int(input('Please enter the number of people that you follow : '))
        browser = Internet(username, password, number_of_followers, number_of_follow)
        browser.unfollow_non_followers() 
    if choice == '3':
        browser.random_likes_follow()
    if choice == '4':
        browser.long_time_running()
    if choice == '5':
        tag = input("Enter the tag pls, without the '#' : ")
        username = input("enter your username : ")
        password = getpass("enter your password (its normal if you don't see what you write): ")
        number_of_follow = 0
        number_of_followers = 0
        browser = Internet(username, password, number_of_followers, number_of_follow)
        browser.t1 = time.time() + random.randint(165,323) #t1 + between 3 and 5 minutes its not round numbers because i want it unpredictable 
        browser.like_picture(tag)
    if choice == '6':
        browser.follow_back()
    if choice not in ['1','2','3','4','5','6']:
        print("wrong choice pls try again :D")