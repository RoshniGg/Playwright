class CheckoutCompletePage:

    def __init__(self,page):
        self.page = page
        self.title= page.locator('.title')


    def get_title(self):
        return self.title