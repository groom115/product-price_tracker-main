#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import requests
import smtplib
import time

prices_list = []



#url links for checking
#url="https://www.amazon.in/Realme-Storage-Additional-Exchange-Offers/dp/B092QJLQMX/ref=sr_1_3?dchild=1&keywords=realme&qid=1626576992&sr=8-3"
#URL="https://www.flipkart.com/try-solid-men-polo-neck-white-black-t-shirt/p/itmce6503bba6f4c?pid=TSHF8UEUQPUSH9HF&lid=LSTTSHF8UEUQPUSH9HFSXT9IB&marketplace=FLIPKART&store=clo%2Fash%2Fank%2Fedy&srno=b_1_1&otracker=hp_omu_Deals%2Bof%2Bthe%2BDay_1_4.dealCard.OMU_K35T3HSIJGOH_3&otracker1=hp_omu_SECTIONED_manualRanking_neo%2Fmerchandising_Deals%2Bof%2Bthe%2BDay_NA_dealCard_cc_1_NA_view-all_3&fm=neo%2Fmerchandising&iid=716621ac-e71e-496c-8322-58fd7920af79.TSHF8UEUQPUSH9HF.SEARCH&ppt=hp&ppn=homepage&ssid=lbcc0owqw00000001626797158505"

#HEADERS for amazon AND headers from flipkart
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15"}
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36' }
sender_email="abhishekshyam_ug@ece.nits.ac.in"
sender_password="*********"
receiver_email="shyamabhishek115@gmail.com"



# checking while the last element added is smaller that previous last element, if so that means price decreses and it return true
def price_decrease_check(price_list):
    if prices_list[-1] < prices_list[-2]:
        return True
    else:
        return False


# checkin for flipkartdef flipkart_check_price():

def flipkart_check_price(url):
    '''Function called when there is a price check to be made '''
    
    #Loads the HTML ans stores in page
    page = requests.get(URL, headers=headers)
    
    #Enables use to parse the HTMl through html parser
    soup = BeautifulSoup(page.content, 'html.parser')
    
    #Gets the title of the product by looking for <span> tag in the HTML code with the classname "_35KyD6"
    title = soup.find("span", {"class": "B_NuCI"}).get_text()
    
    #Gets the price of the product by looking for <div> tag in the HTML code with the classname "_35KyD6"
    # [1:] is used to truncate the '₹' symbol and replace method to eradicate any commas if present
    price = float(soup.find("div", {"class":"_30jeq3 _16Jk6d"}).get_text()[1:].replace(',',''))
    prices = float(prices.replace(",", "").replace("₹", ""))
    prices_list.append(prices)
    print(title)
    print(price) 




# return price of the product with title
def amazon_check_price(url):
    
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    
   # soup = BeautifulSoup(page.content, 'lxml')
    #sauce = urllib.request.urlopen(url).read()
    #soup = BeautifulSoup(sauce, "html.parser")

    title = soup.find(id='productTitle').get_text().strip()
    prices = soup.find(id="priceblock_ourprice").get_text()
    prices = float(prices.replace(",", "").replace("₹", ""))
    prices_list.append(prices)
    print(title)
    print(prices)
    return prices

#login to ur email and sending to another user
def send_email(mailtext):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender_email, sender_password)
    s.sendmail(sender_email, receiver_email, mailtext)
    s.quit()



#proccesing 
count = 1
while True:
    print("website:")
    st=input()
    url=input()
    if st == "amazon":
        current_price = amazon_check_price(url)
    else:
        current_price = flipkart_check_price(url)
    
    if count > 1:
        flag = price_decrease_check(prices_list)
        if flag:
            print("cheaper, notifying!.....")
            decrease = prices_list[-1] - prices_list[-2]
            message = f"The price has decrease please check the item. The price decrease by {decrease} rupees."
            mailtext='Subject:'+message+'\n\n'+url
            send_email(mailtext) #ADD THE OTHER AGRUMENTS sender_email, sender_password, receiver_email
        else:
            print("still, too expensive")
    
    time.sleep(36000)
    count += 1
