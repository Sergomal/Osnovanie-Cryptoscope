import pprint
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox as mb
import requests
import json
from io import BytesIO


def update_cryptocurrency_label(event):
    code = cryptocurrency_combobox.get()
    name = cryptocurrency_id_name_dict[code]
    cryptocurrency_label.config(text=name)
    set_image(code)


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
    global crypt_id_name
    url = "https://api.coingecko.com/api/v3/coins/list"

    headers = {
        "accept": "application/json",
        "x-cg-api-key": "CG-fdB222bEAD3nQxkDWGKkb2gbyjD"

    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        for crypta in data:
            crypt_id_name.update({crypta['id']: crypta['name']})
    except Exception as e:
        mb.showerror("Error", str(e))


def load_image(code):
    img_url = ""

    try:

        url = "https://api.coingecko.com/api/v3/asset_platforms"
        headers = {
            "accept": "application/json",
            "x-cg-api-key": "CG-fdB222bEAD3nQxkDWGKkb2gbyjD"

        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        for asset in data:
            if asset['id'] == code:
                img_urls = asset['image']
                img_url = img_urls['small']
                break

        print(img_url)
        response = requests.get(img_url)
        image_data = BytesIO(response.content)
        img = Image.open(image_data)
        img.thumbnail((400, 400), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


def set_image(code):
    img = load_image(code)
    if img:
        cryptocurrency_label.config(image=img)
        cryptocurrency_label.image = img


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
window.title("CryptoScope 0.3")
window.geometry("424x424")
window.configure(background='gray')

crypto_lists()

Label(text="Введите код криптовалюты", font=("Arial", 12)).grid(row=0, column=0, padx=4, pady=4, sticky=NSEW)
Label(text="Валюта платежа", font=("Arial", 12)).grid(row=0, column=1, padx=4, pady=4, sticky=NSEW)

cryptocurrency_combobox = ttk.Combobox(values=list(cryptocurrency_id_name_dict), font=("Arial", 12))
cryptocurrency_combobox.current(0)
cryptocurrency_combobox.grid(row=1, column=0, padx=4, pady=4, sticky=NSEW)
cryptocurrency_combobox.bind("<<ComboboxSelected>>", update_cryptocurrency_label)
cryptocurrency_combobox.current(0)


currency_combobox = ttk.Combobox(values=list(currency_id_name_dict), font=("Arial", 12))
currency_combobox.current(0)
currency_combobox.grid(row=1, column=1, padx=4, pady=4, sticky=NSEW)
currency_combobox.bind("<<ComboboxSelected>>", update_currency_label)

cryptocurrency_label = ttk.Label(font=("Arial", 12))
cryptocurrency_label.grid(row=2, column=0, padx=4, pady=4, sticky=NSEW)
update_cryptocurrency_label(list(cryptocurrency_id_name_dict)[0])


currency_label = ttk.Label(font=("Arial", 12))
currency_label.grid(row=2, column=1, padx=4, pady=4, sticky=NSEW)
update_currency_label(list(currency_id_name_dict)[0])

Button(text="Получить курс обмена", font=("Arial", 12), command=exchange).grid(row=3, column=0, columnspan=2, padx=4,
                                                                               pady=4, sticky=NSEW)

rate_label = ttk.Label(text="Выберите код криптовалюты и валюту платежа,\nчтобы узнать курс обмена", font=("Arial", 12))
rate_label.grid(row=4, column=0, columnspan=2, padx=4, pady=4, sticky=NSEW)

window.mainloop()
