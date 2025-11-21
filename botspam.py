import telebot
import schedule
import time
import random
import threading
import os
from flask import Flask, request

# TOKEN bot spam
TOKEN = "8339189762:AAG5thO3Rx4-0h-pyMRP1y2mWO4_dO9aMCY"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Danh sách nhóm
GROUP_IDS = [
    -1002335996897,
    # Thêm nhóm khác ở đây...
]

# 6 nội dung quảng cáo
MESSAGES = [
    "🎁 Bot mới: nhận mã quà tặng ngẫu nhiên từ 20K đến 200K mỗi ngày!\n@codenetwinbycvk_bot",
    "✨ Muốn nhận gift random 20K–200K? Vào thử bot này ngay 👉 @codenetwinbycvk_bot",
    "🔥 Bot đang phát mã quà ngẫu nhiên giá trị 20K–200K, thử vận may liền tay!\n@codenetwinbycvk_bot",
    "💥 Làm vài thao tác nhẹ là có mã quà random từ 20K đến 200K!\n@codenetwinbycvk_bot",
    "🚀 Nhận quà hoàn toàn miễn phí, random giá trị 20K–200K mỗi lần!\n@codenetwinbycvk_bot",
    "🎉 Bot này phát quà ngẫu nhiên siêu vui, trị giá từ 20K đến 200K!\n@codenetwinbycvk_bot",
]


def spam_job():
    sent = 0
    random.shuffle(GROUP_IDS)
    for group_id in GROUP_IDS:
        try:
            msg = random.choice(MESSAGES)
            bot.send_message(group_id, msg)
            sent += 1
            print(f"Sent → {group_id}")
            time.sleep(random.randint(9, 20))
        except Exception as e:
            print(f"Lỗi nhóm {group_id}: {e}")
            time.sleep(5)
    print(f"HOÀN THÀNH – Gửi {sent}/{len(GROUP_IDS)} nhóm – {time.strftime('%H:%M %d/%m')}")

# Gửi mỗi 1 phút để test (sau đổi lại 30)
schedule.every(1).minutes.do(spam_job)

def run_schedule():
    spam_job()  # gửi luôn lần đầu
    while True:
        schedule.run_pending()
        time.sleep(30)

threading.Thread(target=run_schedule, daemon=True).start()

# ==================== WEBHOOK CHO RENDER ====================
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.get_json())
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "Bot spam NETWIN đang chạy mượt mà!", 200

if __name__ == "__main__":
    bot.remove_webhook()
    time.sleep(2)
    url = os.environ.get("RENDER_EXTERNAL_URL")
    bot.set_webhook(url=f"{url}/{TOKEN}")
    print(f"Webhook set: {url}/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
