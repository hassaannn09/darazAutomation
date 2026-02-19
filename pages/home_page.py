from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    SEARCH_BOX = (By.NAME, "q")  # Search input
    SEARCH_BUTTON = (By.CLASS_NAME, "search-box__button--1oH7")
    POPUP_CLOSE = (By.CLASS_NAME, "ic-close")  # If any modal appears

    def close_popup_if_present(self):
        try:
            self.wait_and_click(self.POPUP_CLOSE)
        except:
            pass

    def search_product(self, product):
        self.close_popup_if_present()
        self.wait_and_send_keys(self.SEARCH_BOX, product)
        self.wait_and_click(self.SEARCH_BUTTON)
