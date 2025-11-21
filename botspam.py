import telebot
import schedule
import time
import random
import threading

# ← DÁN TOKEN BOT MỚI VÀO ĐÂY
TOKEN = "8339189762:AAG5thO3Rx4-0h-pyMRP1y2mWO4_dO9aMCY"
bot = telebot.TeleBot(TOKEN)

# ← DÁN HÀNG NGHÌN ID NHÓM VÀO ĐÂY (mỗi dòng 1 ID)
GROUP_IDS = [
    -1002335996897,  # ← Kiểm tiền ko vốn UT-AT (đã gửi thành công)
    # Thêm nhóm khác ở đây...
]

# 6 nội dung tin nhắn luân phiên để tránh bị report spam giống nhau
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
    random.shuffle(GROUP_IDS)  # trộn thứ tự nhóm mỗi lần gửi
    for group_id in GROUP_IDS:
        try:
            msg = random.choice(MESSAGES)
            bot.send_message(group_id, msg)
            sent += 1
            print(f"Sent → {group_id}")
            time.sleep(random.randint(9, 20))  # delay 9–20 giây mỗi tin
        except Exception as e:
            if "blocked" in str(e) or "kicked" in str(e) or "chat not found" in str(e):
                print(f"Bot bị kick/ban khỏi nhóm {group_id}")
            else:
                print(f"Lỗi {group_id}: {e}")
            time.sleep(5)
    print(f"HOÀN THÀNH 1 VÒNG – ĐÃ GỬI {sent}/{len(GROUP_IDS)} NHÓM – {time.strftime('%H:%M %d/%m')}")

# GỬI MỖI 30 PHÚT 1 LẦN – 48 LẦN/NGÀY
schedule.every(30).minutes.do(spam_job)

# Chạy nền
def run_schedule():
    spam_job()  # gửi luôn lần đầu khi khởi động
    while True:
        schedule.run_pending()
        time.sleep(30)

threading.Thread(target=run_schedule, daemon=True).start()

# Giữ Render sống + test
@bot.message_handler(commands=['start', 'test'])
def test(m):
    bot.reply_to(m, "Bot spam đang chạy 30 phút/lần – cực mạnh!")

print("BOT SPAM 30 PHÚT 1 LẦN ĐÃ KHỞI ĐỘNG!")
bot.infinity_polling()