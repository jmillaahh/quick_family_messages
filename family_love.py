import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import datetime
import pytz
import time

USER = os.getenv('personal_email')
PASSWORD = os.getenv('shhh_keep_it_a_secret')

tz = pytz.timezone('Asia/Manila')
TODAY_WEEKDAY = datetime.datetime.now(tz=tz).weekday()

errors = {
    'login_email': "FAILURE: Unable to locate and input email credentials in email field.",
    'login_password': "FAILURE: Unable to locate and input password credentials in email field.",
    'login_attempt': "FAILURE: Unable to LOGIN.",
    'search_name': "FAILURE: Unable to locate search box on logged in Messenger page.",
    'select_contact': "FAILURE: Unable to select desired contact.",
    'select_message_box': "FAILURE: Unable to find the message box.",
    'send_message': "FAILURE: Unable to send message.",
}
nicknames = {
    os.getenv('DAD_FB'): 'pops',
    os.getenv('MOM_FB'): 'momsie',
    os.getenv('OLDEST_FB'): 'niks',
    os.getenv('SECOND_FB'): 'maxie',
    os.getenv('WEIRDO_FB'): 'loser',
    os.getenv('BRO_FB'): 'kiddo',
}
recipients = [name for name in nicknames.keys()]


def login(email, password):
    try:
        email_field = wait.until(EC.element_to_be_clickable((By.XPATH, f"//input[@name='email']")))
        email_field.send_keys(email)
    except:
        print(errors['login_email'])
        return
    try:
        password_field = wait.until(EC.element_to_be_clickable((By.XPATH, f"//input[@name='pass']")))
        password_field.send_keys(password)
        try:
            password_field.send_keys(Keys.ENTER)
        except:
            print(errors['login_attempt'])
            return
    except:
        print(errors['login_password'])
        return


def locate_contact(name):
    try:
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, r"//input[@class='_58al _7tpc']")))
        search_box.click()
        search_box.send_keys(name)
    except:
        print(errors['search_name'])
        return

    try:
        first_result = wait.until(EC.element_to_be_clickable((By.XPATH, fr"//div[text()='{name}'][1]")))
        first_result.click()
        time.sleep(5)
    except:
        print(errors['select_contact'])
        return


def send_message(message):
    xpath = fr"//div[@class='_1mf _1mj']"
    try:
        message_box = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        message_box.click()
    except:
        print(errors['select_message_box'])
        return

    try:
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)
        time.sleep(3)
    except:
        print(errors['send_message'])
        return


def personalize_message(name, day):
    daily_messages = {
        0: f"hiya {name}, hope you had a restful weekend and that u have a great weekend and an even greater week ahead!",
        1: f"start of the week is always slow but know that i miss ya and love ya {name}",
        2: f"hump day today!! you've made it this far {name}, keep at it :)",
        3: f"woohoooo one more day til the end of the work week {name}!! finish strong!!",
        4: f"yay {name}!!! u made it to the end of the week wooooo",
        5: f"have a great saturday {name}!",
        6: f"enjoy and rest up today {name} -- love u and miss u"
    }
    return daily_messages[day]


# DRIVER CODE
# ============================
if __name__ == "__main__":
    print(f'Script started @ {datetime.dateime.now().strftime("%H:%M:%S")}')        # Record start time

    # Start-up window
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 30)
    driver.get('https://www.messenger.com/')

    # Login
    login(USER, PASSWORD)

    for member in recipients:
        locate_contact(member)
        personal = nicknames[member]
        todays_message = personalize_message(personal, TODAY_WEEKDAY)
        send_message(todays_message)

    print(f'Script finished @ {datetime.dateime.now().strftime("%H:%M:%S")}')       # Record end time