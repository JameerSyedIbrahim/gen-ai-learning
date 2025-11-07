import pyautogui
import webbrowser
import time

# Step 1: Open WhatsApp Web
webbrowser.open("https://web.whatsapp.com")
print("Opening WhatsApp Web...")
time.sleep(10)  # wait for it to load (adjust if needed)

# Step 2: Click the search bar (you found this position manually)
search_x, search_y = 203, 242  # <-- your coordinates
pyautogui.moveTo(search_x, search_y, duration=0.5)
pyautogui.click()
time.sleep(1)

# Step 3: Type the group name
group_name = "SE - AI-B3 - 2"  # <-- change this to your group name
pyautogui.typewrite(group_name)
time.sleep(2)

# Step 4: Press Enter to open the group
pyautogui.press('enter')
time.sleep(3)

# Step 5: Type and send your message
message = "One week Completed - PyautoGui"
pyautogui.typewrite(message)
pyautogui.press('enter')

print("✅ Message sent successfully!")

