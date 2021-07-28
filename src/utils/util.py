import requests, csv, datetime, os
from time import sleep
from requests.api import request
from models.currency import *
ROOT_PATH = os.getcwd()

# Method to create, doing a request and save the content in a html file
def create_html():
    # Prevents the site from identifying that it is a crawler
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}

    url = 'https://br.investing.com/currencies/single-currency-crosses'
    resp = requests.get(url, headers=header)

    with open('url_content.html', 'w', encoding='utf-8') as file:
        file.write(resp.text)

# Function just to pass line
def pass_line(file, count):
    for i in range(count):
        file.readline()

# Scrap the page and return a list content all the currency
def scrap_page():
    save_data = []
    date = datetime.datetime.now().strftime('%d-%m-%Y')

    with open('url_content.html', 'r', encoding='utf-8', newline='') as file:
        for line in file:
            if line.find('<td class="bold left noWrap elp plusIconTd">') != -1:
                # Get a pair of currency to do another scrap specific
                splited = line.split('<td class="bold left noWrap elp plusIconTd">')
                
                for i in range(1, 201):
                    currency = splited[i][(splited[i].find('href="') + len('href="')) : (splited[i].find('title') - 2)]
                    url = f'https://br.investing.com{currency}'
                    data = scrap_specific_currency(url, date)
                    object = Currency(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])
  
                    # Save the data
                    save_data.append([data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]])

                break
                

    save_data.insert(0, ['base', 'currency_pair', 'sell_price', 'buy_price', 'min_day', 'max_day', 'open_market_value', 'last_closing', 'date'])

    with open(f'currency_prices_{date}.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(save_data)


def scrap_specific_currency(url, date):
    # Prevents the site from identifying that it is a crawler
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}

    resp = requests.get(str(url), headers=header)

    currency_information = []

    for line in resp.iter_lines():
        line = str(line, encoding='utf-8')

        if line.find('<h1 class="float_lang_base_1 relativeAttr" dir="ltr">') != -1:
            currency_pair = line[(line.find('>') + len('>')) : (line.find('-') + len('-')) - 2]
            print(currency_pair)
            base = line[(line.find('-') + 2) : (line.rfind('</h1>'))]
            print(base)
            currency_information.append(base.strip())
            currency_information.append(currency_pair)

        if line.find('<div class="first inlineblock"><span class="float_lang_base_1">') != -1:
            # Split line to recover fields
            splitted_line = line.split('</span></div>')
            
            # Taking each respective field
            last_closing = splitted_line[0][(splitted_line[0].find('bold">')) + len('bold">') : ]
            buy = splitted_line[1][(splitted_line[1].find('bold">')) + len('bold">') : ]
            var_diary = splitted_line[2][(splitted_line[2].find('bold">')) + len('bold">') : ]
            open = splitted_line[3][(splitted_line[3].find('bold">')) + len('bold">') : ]
            sell = splitted_line[4][(splitted_line[4].find('bold">')) + len('bold">') : ]
            
            # Remove comma
            last_closing = last_closing.replace(',', '.')
            buy = buy.replace(',', '.')
            var_diary = var_diary.replace(',', '.').replace(' ', '')
            open = open.replace(',', '.')
            sell = sell.replace(',', '.')

            var_diary = var_diary.split('-')

            currency_information.append(sell)
            currency_information.append(buy)
            currency_information.append(var_diary[0])
            currency_information.append(var_diary[1])
            currency_information.append(open)
            currency_information.append(last_closing)
            currency_information.append(date)
            
            break


    return currency_information

def read_last_register():

    try:
        with open('last_register.txt', 'r', encoding='utf-8') as file:
            last_register = file.read()
        
        return last_register
    except EnvironmentError:
        with open('last_register.txt', 'w', encoding='utf-8') as file:
            now = datetime.datetime.now()
            today = now.day
            file.write(str(today))

        return now

def write_new_register():
    with open('last_register.txt', 'w', encoding='utf-8', newline='') as file:
        now = datetime.datetime.now()
        today = now.day
        file.write(str(today))
