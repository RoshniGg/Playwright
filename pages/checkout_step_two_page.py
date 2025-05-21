class CheckoutStepTwoPage:

    def __init__(self,page):
        self.page = page
        self.finish_button=page.locator(".btn_action.cart_button")

    def click_finish(self):
        self.finish_button.click()
