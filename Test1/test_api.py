
import sys
import unittest
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By

from random import choice


logger = logging.getLogger()
logger.level = logging.INFO

stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


class CheckOneProduct(unittest.TestCase):


    def setUp(self):

        logger.info('Settind driver..')
        
        options = webdriver.ChromeOptions()
        options.page_load_strategy='eager'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(
            options=options
    )


    def test_check_one_product(self):

        logger.info('Access url..')
        self.driver.get("https://www.saucedemo.com/")

        logger.info('Authorization..')
        self.driver.find_element(By.XPATH, '//input[@data-test="username"]') \
            .send_keys("standard_user")

        self.driver.find_element(By.XPATH, '//input[@data-test="password"]') \
            .send_keys("secret_sauce")

        self.driver.find_element(By.XPATH, '//input[@data-test="login-button"]') \
            .click()
        
        logger.info('Choose product..')
        labels = self.driver.find_elements(By.XPATH, '//div[@data-test="inventory-item-name"]')
        prices = self.driver.find_elements(By.XPATH, '//button[text()="Add to cart"]')

        items = dict((label.text, price_btn) for label, price_btn in zip(labels, prices))

        product_name = choice(list(items.keys()))

        logger.info(f'Chosen product: "{product_name}"..')
        items[product_name].click()

        assert self.driver.find_element(By.XPATH, '//span[@data-test="shopping-cart-badge"]'), "Cart flag is not visiable"
        logger.info('Go to the cart..')

        self.driver.find_element(By.XPATH, '//a[@data-test="shopping-cart-link"]').click()
        items = self.driver.find_elements(By.XPATH, '//div[@data-test="inventory-item-name"]')

        assert product_name in [item.text for item in items], "Chosen product is not in the cart"
        logger.info('Product actualy is in the cart..')

        logger.info('Confirm the order..')
        self.driver.find_element(By.XPATH, "//button[@data-test='checkout']").click()

        logger.info('Filing form fields..')
        self.driver.find_element(By.XPATH, "//input[@data-test='firstName']").send_keys("Bushmen")
        self.driver.find_element(By.XPATH, '//input[@data-test="lastName"]').send_keys("Heavyside")
        self.driver.find_element(By.XPATH, '//input[@data-test="postalCode"]').send_keys("253748")

        logger.info('Continue..')
        self.driver.find_element(By.XPATH, "//input[@data-test='continue']").click()

        logger.info('Finish..')
        self.driver.find_element(By.XPATH, "//button[@data-test='finish']").click()

        assert self.driver.find_element(By.XPATH, '//div[@data-test="complete-text"]'), "Can`t locate complete text.."
        logger.info('Complete..')

        logger.info('Back to products..')
        self.driver.find_element(By.XPATH, "//button[@data-test='back-to-products']").click()


    def tearDown(self):
        self.driver.close()



if __name__ == "__main__":
    unittest.main()