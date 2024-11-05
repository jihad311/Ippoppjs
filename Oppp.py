import telebot
import random
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup

API_TOKEN = '7257366939:AAGVDtHfWO-Ikoi3iYx0Mvqk7UGBNqtZchs'
bot = telebot.TeleBot(API_TOKEN)


def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    checksum = 0
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10

def complete_card_number(partial_card_number, length=16):
    card_number = [int(digit) for digit in partial_card_number if digit.isdigit()]
    while len(card_number) < (length - 1):
        card_number.append(random.randint(0, 9))
    check_digit = luhn_checksum(int("".join(map(str, card_number))) * 10)
    if check_digit != 0:
        check_digit = 10 - check_digit
    card_number.append(check_digit)
    return ''.join(map(str, card_number))

def generate_expiry_date(provided_date=None):
    if provided_date:
        return provided_date
    current_year = datetime.now().year
    year = random.randint(current_year, current_year + 5)
    month = random.randint(1, 12)
    return f"{month:02}|{year % 100:02}"

def generate_cvv(length=3):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def generate_cards(input_data, count=10):
    parts = input_data.split("|")
    partial_card = parts[0] if parts[0] else ""
    expiry_date = f"{parts[1]}|{parts[2]}" if len(parts) > 2 and parts[1] and parts[2] else generate_expiry_date()
    
    cards = []
    for _ in range(count):
        card_number = complete_card_number(partial_card)
        cvv = generate_cvv()
        cards.append(f"{card_number}|{expiry_date}|{cvv}")
    
    bin_display = partial_card[:6] if len(partial_card) >= 6 else partial_card
    result_text = f"𝗕𝗜𝗡 ⇾ {bin_display}\n\n" + "\n".join(cards)
    return result_text

def generate_combo_file(bin_code, count):
    cards = []
    for _ in range(count):
        card_number = complete_card_number(bin_code)
        expiry_date = generate_expiry_date()
        cvv = generate_cvv()
        cards.append(f"{card_number}|{expiry_date}|{cvv}")
    
    filename = f"{bin_code}_combo.txt"
    with open(filename, "w") as file:
        file.write("\n".join(cards))
    return filename

# دالة لجلب معلومات BIN
def fetch_bin_info(bin_code):
    url = f'https://bincheck.io/ar/details/{bin_code}'
    cookies = {
	    '_ga': 'GA1.1.1995228761.1730140163',
	    '_clck': '1qjaf5r%7C2%7Cfql%7C0%7C1762',
	    '__gads': 'ID=114ce0fa404e3366:T=1730140164:RT=1730742450:S=ALNI_MYShGpntgkdMwi5VZH4Toh8u6-vRQ',
	    '__gpi': 'UID=00000f1a932575ae:T=1730140164:RT=1730742450:S=ALNI_MaJa8rRPl_mhIDilAAdukUr8glMCw',
	    '__eoi': 'ID=9d86f1d61e40357e:T=1730140164:RT=1730742450:S=AA-Afja0IuW9t0DEpU-ixF2XrsXP',
	    'cfzs_google-analytics_v4': '%7B%22OFGW_pageviewCounter%22%3A%7B%22v%22%3A%222%22%7D%7D',
	    '_ga_CGDE2TMKTW': 'GS1.1.1730737586.4.1.1730742467.42.0.0',
	    'FCNEC': '%5B%5B%22AKsRol_Yx6cG5IjL7CcZmAIfZAh0KB4Ia7JLlhUFaNPKgLr-BXhhmuaburLJj519ns5LPCFZXbUrCMXZfzHrrjTIWkQYX82FttcCW5gAaN7ep_-ABf_tKqKdkKfFa70RUR0bdYfMMZAu3DJkq9gEGYPahAEb5ewxzQ%3D%3D%22%5D%2Cnull%2C%5B%5B2%2C%22%5Bnull%2C%5Bnull%2C1%2C%5B1730140171%2C782429000%5D%5D%5D%22%5D%5D%5D',
	    'cfz_google-analytics_v4': '%7B%22OFGW_engagementDuration%22%3A%7B%22v%22%3A%220%22%2C%22e%22%3A1762278697865%7D%2C%22OFGW_engagementStart%22%3A%7B%22v%22%3A1730742707527%2C%22e%22%3A1762278707675%7D%2C%22OFGW_counter%22%3A%7B%22v%22%3A%2235%22%2C%22e%22%3A1762278697865%7D%2C%22OFGW_session_counter%22%3A%7B%22v%22%3A%222%22%2C%22e%22%3A1762278697865%7D%2C%22OFGW_ga4%22%3A%7B%22v%22%3A%22f5057373-c62d-4a31-86e7-9168701d376b%22%2C%22e%22%3A1762278697865%7D%2C%22OFGW__z_ga_audiences%22%3A%7B%22v%22%3A%22f5057373-c62d-4a31-86e7-9168701d376b%22%2C%22e%22%3A1762268505579%7D%2C%22OFGW_let%22%3A%7B%22v%22%3A%221730742697865%22%2C%22e%22%3A1762278697865%7D%2C%22OFGW_ga4sid%22%3A%7B%22v%22%3A%22687786491%22%2C%22e%22%3A1730744497865%7D%7D',
	    'XSRF-TOKEN': 'eyJpdiI6InlvVDhGTFBkbCtFN2dxT0JBSFIzcnc9PSIsInZhbHVlIjoiN3NJdStaMUk3TUNEYTZQdm1rSHB0QlVaUWtOODRxSVlpenkzc3V1SWZSa0J1WUU1dnRsdlVJa0ZEbTR5c0lsb0xDSVdwWlYvRmdXTkdqdE5SdXlFekt6RldlMWtLZ1RkMWNqT2RPOVBWWVdRbDFBdCtwb1FlRXhvaDNKL3Jrbk4iLCJtYWMiOiI5YWY0MmU1MTIyODAyNzAzOTJiNWNiMWJiMzdmOTEzYzk5ZTdhNzVkODQ0OTk0ZWFiMWJjZWY5MGRhN2I5ZGZkIn0%3D',
	    'bincheck_session': 'eyJpdiI6InVsRWxGbDdkZXBkc3B0SWNaMk1Nd1E9PSIsInZhbHVlIjoibXJ0OXZqTW5DQURTb3VZaFgzcG1RV2d4UTBGK2ZWU3ByZWhVVzNRcmZmbWVZZGYwMEtxcUord2V5cjFJeXJsUFcrRWJNakt3YzNLTXMzWnJHQTgyU2x3azVuOGtNeWQwYXkwemd5T0EvQk5abW16d0R2TFY3dHNEZHluamJvUDgiLCJtYWMiOiI5OTE5NTAwYmNiOTk2NzM3OWQ5MDE5MzcxNmRlNDNjMWI1MTI5MDY1NzE0YzNmMTFiZTg3ZjIwNjM2YzgxYzYxIn0%3D',
	}
    headers = {
	    'authority': 'bincheck.io',
	    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	    'accept-language': 'ar-AE,ar;q=0.9,en-US;q=0.8,en;q=0.7',
	    'referer': 'https://bincheck.io/ar/bin-checker',
	    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
	    'sec-ch-ua-mobile': '?1',
	    'sec-ch-ua-platform': '"Android"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'navigate',
	    'sec-fetch-site': 'same-origin',
	    'upgrade-insecure-requests': '1',
	    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
	}

    response = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    info = {}
    for row in soup.select("table tr"):
        columns = row.find_all("td")
        if len(columns) == 2:
            label = columns[0].get_text(strip=True)
            value = columns[1].get_text(strip=True)
            info[label] = value
    
    if not info:
        return "لم يتم العثور على معلومات للـ BIN المحدد."
    
    result_text = f"معلومات BIN: {bin_code}\n\n"
    for key, value in info.items():
        result_text += f"{key}: {value}\n"
    return result_text

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton("🔗 My Account", url="https://t.me/@l31l3")
    markup.add(btn)
    bot.send_message(message.chat.id, "Welcome! You can use the .gen command to generate fake credit cards.\n"
                                      "Example: .gen 763486\n"
                                      "You can also use the .st command to create a combo file.\n"
                                      "Example: .st 863484 (100)\n"
                                      "Use .bin command to get BIN information.\n"
                                      "Example: .bin 549186", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.startswith(".gen"))
def generate_cards_command(message):
    try:
        input_data = message.text.split(" ", 1)[1]
        generated_cards = generate_cards(input_data)
        bot.send_message(message.chat.id, f"Cards generated successfully:\n\n{generated_cards}")
    except Exception as e:
        bot.send_message(message.chat.id, "An error occurred. Please make sure the input is correct.")

@bot.message_handler(func=lambda message: message.text.startswith(".st"))
def generate_combo_command(message):
    try:
        content = message.text.split(" ")
        bin_code = content[1]
        count = int(content[2].strip("()")) if len(content) > 2 else 10  
        
        filename = generate_combo_file(bin_code, count)
        with open(filename, "rb") as file:
            bot.send_document(message.chat.id, file)
        
        os.remove(filename)
    except Exception as e:
        bot.send_message(message.chat.id, "حدث خطأ. تأكد من إدخال البيانات بالشكل الصحيح. مثال: .st 863484 (100)")

@bot.message_handler(func=lambda message: message.text.startswith(".bin"))
def bin_info_command(message):
    try:
        bin_code = message.text.split(" ", 1)[1]
        bin_info = fetch_bin_info(bin_code)
        bot.send_message(message.chat.id, bin_info)
    except Exception as e:
        bot.send_message(message.chat.id, "حدث خطأ. تأكد من إدخال BIN بالشكل الصحيح. مثال: .bin 549186")

bot.polling()
