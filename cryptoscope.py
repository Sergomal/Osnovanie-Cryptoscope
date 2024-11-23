import pprint
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests
import json


def update_cryptocurrency_label(event):
    code = cryptocurrency_combobox.get()
    name = cryptocurrency_id_name_dict[code]
    cryptocurrency_label.config(text=name)


def update_currency_label(event):
    code = currency_combobox.get()
    name = currency_id_name_dict[code]
    currency_label.config(text=name)


def exchange():
    currency_code = currency_combobox.get()
    cryptocurrency_code = cryptocurrency_combobox.get()
    name_cryptocurrency = cryptocurrency_id_name_dict[cryptocurrency_code]
    name_currency = currency_id_name_dict[currency_code]
    price = 0.0

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={cryptocurrency_code}&vs_currencies={currency_code}"

    headers = {
        "accept": "application/json",
        "x-cg-api-key": "CG-fdBbEAD3nQxkDWGKkb2gbyjD",

    }

    if currency_code and cryptocurrency_code:

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            for crypto_id in data:
                name_cryptocurrency = crypt_id_name[crypto_id]
                for p in data[crypto_id].values():
                    price = p

            rate_label.config(text=f"Курс: {price} {name_currency} за 1 {name_cryptocurrency}")

        except Exception as e:
            mb.showerror("Error", str(e))


def crypto_lists():
    global crypt_id_name, count
    url = "https://api.coingecko.com/api/v3/coins/list"

    headers = {
        "accept": "application/json",
        "x-cg-api-key": "CG-fdB222bEAD3nQxkDWGKkb2gbyjD"

    }

    response = requests.get(url, headers=headers)
    data = response.json()

    for crypta in data:
        crypt_id_name.update({crypta['id']: crypta['name']})


crypt_id_name = {}

cryptocurrency_id_name_dict = {
    'bitcoin': 'Bitcoin',
    'ethereum': 'Ethereum',
    'solana': 'Solana',
    'the-open-network': 'Toncoin',
    'near': 'NEAR Protocol',
    'sui': 'Sui',
    'optimism': 'Optimism',
    'helium': 'Helium',
    'bittensor': 'Bittensor',
    'celo': 'Celo'
}

currency_id_name_dict = {
    'RUB': 'Российский рубль',
    'USD': 'Американский доллар',
    'EUR': 'Евро',
    'AED': 'Дирхам ОАЭ',
    'CAD': 'Канадский доллар',
    'CHF': 'Швейцарский франк',
    'CNY': 'Китайский юань',
    'GBP': 'Британский фунт стерлингов',
    'JPY': 'Японская йена'

}

window = Tk()
window.title("CryptoScope 0.2")
window.geometry("360x460")
window.configure(background='gray')
window.configure(highlightbackground='gray')

crypto_lists()

Label(text="Введите код криптовалюты").pack(padx=10, pady=10)

cryptocurrency_combobox = ttk.Combobox(values=list(cryptocurrency_id_name_dict))
cryptocurrency_combobox.current(0)
cryptocurrency_combobox.pack(padx=10, pady=10)
cryptocurrency_combobox.bind("<<ComboboxSelected>>", update_cryptocurrency_label)
cryptocurrency_combobox.current(0)


cryptocurrency_label = ttk.Label()
cryptocurrency_label.pack(padx=10, pady=10)
update_cryptocurrency_label(list(cryptocurrency_id_name_dict)[0])

Label(text="Валюта платежа").pack(padx=10, pady=10)

currency_combobox = ttk.Combobox(values=list(currency_id_name_dict))
currency_combobox.current(0)
currency_combobox.pack(padx=10, pady=10)
currency_combobox.bind("<<ComboboxSelected>>", update_currency_label)

currency_label = ttk.Label()
currency_label.pack(padx=10, pady=10)
update_currency_label(list(currency_id_name_dict)[0])

Button(text="Получить курс обмена", command=exchange).pack(padx=10, pady=10)


rate_label = ttk.Label(text="Выберите код криптовалюты и валюту платежа,\nчтобы узнать курс обмена")
rate_label.pack(padx=10, pady=10)

window.mainloop()
