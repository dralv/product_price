import requests
from bs4 import BeautifulSoup
import smtplib
import os
def get_page():
    URL = "https://www.amazon.com/Genuine-Instant-Pot-Tempered-Glass/dp/B07215ZYFQ/ref=pd_bxgy_d_sccl_1/131-4920813-0990240?pd_rd_w=VkESd&content-id=amzn1.sym.7a852ee0-0a6d-4799-a94f-16897e369d05&pf_rd_p=7a852ee0-0a6d-4799-a94f-16897e369d05&pf_rd_r=JHMTYTG0ZF2WN1XXNJ4W&pd_rd_wg=x5ij0&pd_rd_r=ff68428d-71af-4537-8a23-f3a5d551881d&pd_rd_i=B07215ZYFQ&psc=1"
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
        "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url=URL,headers=headers)

    return response.text

def get_price(data):
    soup = BeautifulSoup(data,'html.parser')
    whole_price = soup.select_one(selector=".a-price-whole").getText()
    price_fraction = soup.select_one(selector=".a-price-fraction").getText()
    price =  f"{whole_price}{price_fraction}"
    return float(price)

def email_sender(price):
    MY_EMAIL = os.environ['MY_EMAIL']
    MY_PASSWORD = os.environ['MY_PASS   WORD']
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs="testsendemail@yahook.com",
                            msg=f"Subject:Low Price Alert\n\nThe product is costing less then 100. The current price is: ${price}")

def main():
    data = get_page()
    price = get_price(data)
    if price < 100:
        email_sender(price)
