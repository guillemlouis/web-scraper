import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import smtplib

# url of the site to scrape
url = 'https://www.santafixie.fr/acheter-velo-pignon-fixe/velo-fixie-santafixie-raval-matte-black-30.html#'

# library to generate User-Agent for each browser
ua = UserAgent()

# minimum price to check
minimum_price = int(450)

# email information
email_address_sender = 'email@gmail.com'
email_password_sender = 'password'
email_address_receiver = 'email@gmail.com'


# function that compare the price of a product to a given price
def compare_price():
    # gets the full HTTP response
    response = requests.get(url, ua.safari)

    # gets the HTML page
    html = BeautifulSoup(response.text, 'html.parser')

    # finds the title of the product and its price
    title = html.find('div', class_='product-name').h1.getText()
    price = int(html.find('span', class_='price').getText()[0:3])

    # if the price of the product is bellow the minimum price, it sends an email
    if price < minimum_price:
        print('sending email...')
        send_email(title, price)


# function that sends the email
def send_email(title, price):
    # sets up the gmail connection
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email_address_sender, email_password_sender)

    # creates the message
    subject = "Price dropped"
    body = 'Check the ' + title + 'price! \n' + url + '\n' + "It's only " + str(price) + " now!"
    message = f"Subject: {subject}\n\n{body}"

    # sends the email
    server.sendmail(
        email_address_sender,
        email_address_receiver,
        message.encode('utf-8')
    )

    print('email has been sent')

    # closes the connection
    server.quit()


compare_price()
