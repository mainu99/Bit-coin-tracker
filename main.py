import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()
# global variables
api_key = os.getenv('API_KEY')
bot_token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

threshold = 30000
time_interval = 5 * 60  # in seconds


#get bit coin price
def get_price():
    pass
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }

    # make a request to the coinmarketcap api
    response = requests.get(url, headers=headers)
    response_json = response.json()
    # extract the bitcoin price from the json data
    btc_price = response_json['data'][0]
    return btc_price['quote']['USD']['price']


# send_message through telegram
def send_msg(chat_id, msg):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}"
    requests.get(url)


def main():
    price_list = []
    while True:
        price = get_price()
        price_list.append(price)
        if price < threshold:
            send_msg(chat_id=chat_id, msg=f'BTC Price Drop Alert: {price}')
        if len(price_list) >= 6:
            send_msg(chat_id=chat_id, msg=price_list)
            price_list = []
        time.sleep(time_interval)


if __name__ == '__main__':
    main()
