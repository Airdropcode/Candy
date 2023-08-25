import requests
from bs4 import BeautifulSoup
from http.cookies import SimpleCookie
import sys

# Load cookies for multiple accounts
accounts = []
with open('cookies.txt', 'r') as f:
    raw_cookies = f.read().splitlines()
    for raw_cookie in raw_cookies:
        cookie = SimpleCookie()
        cookie.load(raw_cookie)
        cookies = {k: v.value for k, v in cookie.items()}
        accounts.append(cookies)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.coingecko.com/en/coins/aptos',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
}

params = {
    'locale': 'en',
}

candy_url = "https://www.coingecko.com/account/candy"

def get_candy_balance():
    response = requests.get(candy_url, params=params, cookies=cookies, headers=headers)
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            candy_balance = soup.find('div', {'data-target': 'points.balance'}).text
            return candy_balance
        except:
            print("Account login and balance enquiry failed. Check cookies.")
            sys.exit()
    else:
        print("Error, check cookies or connection.")

# Define the data dictionary
data = {
    'authenticity_token': '',
}

# Iterate through accounts and claim candy
for cookies in accounts:
    print(f"Current Candy Balance: {get_candy_balance()}")
    
    response = requests.get(candy_url, params=params, cookies=cookies, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            authenticity_token = soup.find('input', {'name': 'authenticity_token'})['value']
            data['authenticity_token'] = authenticity_token
        except:
            print("Failed to get auth token. Wait till claim time and try again.")
    else:
        print("Error, check cookies or connection.")

    response = requests.post(
        'https://www.coingecko.com/account/candy/daily_check_in',params=params,cookies=cookies, headers=headers, data=data
    )

    if response.status_code == 200:
        print("Success, candy claimed.")
        print(f"New Candy Balance: {get_candy_balance()}")
    else:
        print("Error, claim failed.")
