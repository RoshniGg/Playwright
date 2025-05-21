import time


class LoginPage:

    def __init__(self,page):
        self.page = page
        self.username= page.locator('#user-name')
        self.password=page.locator('#password')
        self.button= page.locator('#login-button')


    def login(self,username: str,password: str):
        self.username.fill(username)
        self.password.fill(password)
        time.sleep(2)
        self.button.click()



