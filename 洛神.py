import os
import tempfile
import time
import pyautogui
import pygame
import speech_recognition as sr
from gtts import gTTS

def mouse(x, y):
    # 移動滑鼠到螢幕座標 (0, 0)
    if x == 1:
        x_move = 48
    else:
        x_move = 48 + (x - 1) * 96
    if y == 1:
        y_move = 45
    else:
        y_move = 45 + (y - 1) * 130
    pyautogui.moveTo(x_move, y_move)
    # 在滑鼠移動後進行雙擊操作
    pyautogui.doubleClick()

# 初始化pygame
pygame.mixer.init()

# 創建語音識別器
recognizer = sr.Recognizer()

# 語音輸入
with sr.Microphone() as source:
    print("請說話...")
    recognizer.adjust_for_ambient_noise(source)  # 自動調整麥克風噪音
    audio = recognizer.listen(source, timeout=20)  # 設置5秒的語音輸入超時

# 語音識別
try:
    coordinate = []
    text = recognizer.recognize_google(audio, language='zh-TW')
    if text:
        print("你說的話是：" + text)
        # 在此處列印轉換的文本
        print("轉換的文本是：" + text)
        # 檢查文本中是否同時包含"洛神"和"在嘛"
        if "洛神" in text and ("在嘛" in text or "在嗎" in text):
            message = "洛神已經準備就緒，隨時為您服務"
            print(message)

            # 創建臨時文件夾
            temp_dir = tempfile.mkdtemp()

            # 使用gTTS將消息轉換為語音並保存到臨時文件夾
            temp_file = os.path.join(temp_dir, "output.mp3")
            tts = gTTS(text=message, lang='zh-TW')
            tts.save(temp_file)

            # 播放語音文件
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()

            # 等待音訊播放完成
            while pygame.mixer.music.get_busy():
                time.sleep(5)  # 延遲1秒，確保語音有足夠的時間播放

            # 刪除臨時文件
            os.remove(temp_file)
            os.rmdir(temp_dir)
        elif "開啟檔案" in text:
            for i in text:
                if i in "0123456789":
                    coordinate.append(i)
                    if len(coordinate) > 2:
                        c_test = coordinate[0] + coordinate[1]
                        del coordinate[0:2]
                        coordinate.insert(0, c_test)
            mouse(int(coordinate[0]), int(coordinate[1]))
        else:
            print("無法識別語音")

except sr.UnknownValueError:
    print("無法識別語音")
except sr.RequestError as e:
    print(f"無法發送識別請求: {e}")
except Exception as e:
    print(f"發生未知錯誤: {e}")
