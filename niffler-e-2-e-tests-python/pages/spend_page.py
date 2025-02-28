import time

from selene import browser, have, be, command

from models.spend import SpendResponseModel
from pages.base_page import BasePage


class SpendPage(BasePage):
    def __init__(self):
        self.category_name = lambda name_category: browser.element(f'//span[.="{name_category}"]')
        self.delete_button = browser.element('#delete')
        self.delete_button_approve = browser.all('//button[.="Delete"]')
        self.new_spending = browser.element('//a[.="New spending"]')
        self.title_new_spending = browser.element('.MuiTypography-root.MuiTypography-h5.css-w1t7b3')
        self.add_amount = browser.element('#amount')
        self.add_category = browser.element('#category')
        self.add_description = browser.element('#description')
        self.save_button = browser.element('#save')
        self.helper_text = browser.element('.input__helper-text')
        self.currency = browser.element('#currency')
        self.value_currency = lambda currency_val: browser.element(f'//span[.="{currency_val}"]')
        self.calendar = browser.element("[name='date']")
        self.value_date = lambda value_date: browser.element(f'//span[.="{value_date}"]')
        self.no_spend_header = browser.element('//p[.="There are no spendings"]')
        self.menu_spendings = browser.element('[id="spendings"]')

    def create_spend(self, title, amount, name_category, description=""):
        self.new_spending.click()
        self.title_new_spending.should(have.text(title))
        self.add_amount.set_value(amount)
        self.add_category.set_value(name_category)
        self.add_description.set_value(description)
        self.save_button.click()
        self.category_name(name_category).should(be.visible).should(be.clickable)

    def create_spend_different_currency(self, title, amount, currency_val, name_category, description=""):
        self.new_spending.click()
        self.title_new_spending.should(have.text(title))
        self.add_amount.set_value(amount)
        self.currency.click()
        self.value_currency(currency_val).click()
        self.add_category.set_value(name_category)
        self.add_description.set_value(description)
        self.save_button.click()
        time.sleep(2)
        self.category_name(name_category).should(be.visible).should(be.clickable)

    def create_spend_specific_date_on_calendar(self, title, amount, name_category, date, value_date, description=""):
        self.new_spending.click()
        self.title_new_spending.should(have.text(title))
        self.add_amount.set_value(amount)
        self.add_category.set_value(name_category)
        self.calendar.perform(command.js.set_value(date))
        self.add_description.set_value(description)
        self.save_button.click()
        time.sleep(2)
        self.value_date(date).should(be.visible).should(have.text(value_date))
        self.category_name(name_category).should(be.visible).should(be.clickable)

    def create_invalid_spand(self, title, amount, name_category, description, text):
        self.new_spending.click()
        self.title_new_spending.should(have.text(title))
        self.add_amount.set_value(amount)
        self.add_category.set_value(name_category)
        self.add_description.set_value(description)
        self.save_button.click()
        self.helper_text.should(be.visible).should(have.text(text))

    def delete_spend(self, name_category):
        self.category_name(name_category).should(be.visible).click()
        time.sleep(0.5)
        self.delete_button.click()
        time.sleep(0.5)
        self.delete_button_approve.second.click()

    def verify_spend_delete(self, name_category, title_text):
        # Проверяем наличие траты
        self.category_name(name_category).should(be.visible).click()
        # Удаляем трату
        self.delete_button.click()
        self.delete_button_approve.second.click()
        # Проверяем, что траты больше нет
        self.category_name(name_category).should(be.hidden)
        # Проверяем сообщение о пустом списке трат
        self.no_spend_header.should(be.visible).should(have.text(title_text))

    def verify_spend_update(self, spends_update):
        body = SpendResponseModel(**spends_update.json())
        browser.driver.refresh()
        self.menu_spendings.should(have.text(str(body.amount)))
        self.menu_spendings.should(have.text(body.description))

    def verify_description_create(self, descriptions: list):
        for desc in descriptions:
            browser.element(f'//span[.="{desc}"]').should(be.visible).should(have.text(desc))


app_spend_page = SpendPage()
