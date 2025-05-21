class CartPage:

    def __init__(self,page):
        self.page = page
        self.checkout= page.locator('#checkout')


    def shopping_checkout_click(self):
        self.checkout.click()