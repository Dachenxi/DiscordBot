import json
from pathlib import Path

# Lokasi folder settings
settings_folder = Path('settings')
def setup_settings():
    # Cek url.json
    url_file = settings_folder / 'url.json'
    if not url_file.is_file():
        print("'url.json' tidak ditemukan. Membuat baru.")
        webhook_url = input("Masukkan WEBHOOK_URL: ")
        with open(url_file, 'w') as f:
            json.dump({"WEBHOOK_URL": webhook_url}, f, indent=4)
    else:
        print("'url.json' sudah ada.")

    # Cek bot.json
    bot_file = settings_folder / 'bot.json'
    if not bot_file.is_file():
        print("'bot.json' tidak ditemukan. Membuat baru.")
        token = input("Masukkan TOKEN: ")
        prefix = input("Masukkan prefix: ")
        with open(bot_file, 'w') as f:
            json.dump({"TOKEN": token, "prefix": prefix}, f, indent=4)
    else:
        print("'bot.json' sudah ada.")

    print("Selesai.")