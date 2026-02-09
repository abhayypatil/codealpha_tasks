import re
import nltk
import datetime
import webbrowser as wb
import tkinter as tk
from tkinter import messagebox, Canvas, Frame, Scrollbar
from PIL import Image, ImageTk
import asyncio
from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from bs4 import BeautifulSoup
import requests
import keyboard

# NLTK Setup
nltk.download('punkt', quiet=True)
from nltk.tokenize import word_tokenize

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

def preprocess_input(user_input):
    user_input = user_input.lower()
    tokens = word_tokenize(user_input)
    return tokens, user_input

def open_websites(raw_text):
    raw_text = raw_text.lower().strip()
    if "open" not in raw_text:
        return False
    command = raw_text.replace("open", "").strip()
    site_names = [site.strip().replace(" ", "") for site in command.split("and") if site.strip()]
    if not site_names:
        return False
    for site in site_names:
        url = f"https://www.{site}.com"
        wb.open(url)
    return True


def GoogleSearch(topic):
    search(topic)
    return True


def YoutubeSearch(topic):
    url = f"https://www.youtube.com/results?search_query={topic}"
    wb.open(url)
    return True


def PlayYoutube(query):
    playonyt(query)
    return True


def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all("a", {'jsname': 'UWckNb'})
            return [link.get('href') for link in links]

        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)
            return response.text if response.status_code == 200 else None

        html = search_google(app)
        if html:
            links = extract_links(html)
            if links:
                webopen(links[0])
        return True


def CloseApp(app):
    try:
        close(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        return False


def system(command):
    if command in ["mute", "unmute"]:
        keyboard.press_and_release("volume mute")
    elif command in ["volume up", "increase volume"]:
        keyboard.press_and_release("volume up")
    elif command in ["volume down", "decrease volume"]:
        keyboard.press_and_release("volume down")
    return True


async def TranslateAndExecute(commands: list[str]):
    funcs = []
    for command in commands:
        if command.startswith("open "):
            funcs.append(asyncio.to_thread(OpenApp, command[5:]))

        elif command.startswith("close "):
            funcs.append(asyncio.to_thread(CloseApp, command[6:]))

        elif command.startswith("play "):
            funcs.append(asyncio.to_thread(PlayYoutube, command[5:]))

        elif command.startswith("google search "):
            funcs.append(asyncio.to_thread(GoogleSearch, command[14:]))

        elif command.startswith("youtube search "):
            funcs.append(asyncio.to_thread(YoutubeSearch, command[15:]))

        elif command.startswith("system "):
            funcs.append(asyncio.to_thread(system, command[7:]))

    await asyncio.gather(*funcs)
    return True
def generate_response(user_input):
    tokens, raw_text = preprocess_input(user_input)

    if re.search(r"\b(hii|hiii|hiiii|hello|hlo|hloo|hey|namaste)\b", raw_text):
        return "Hello! How can I assist you today?"

    elif re.search(r"\b(time|what's the time|current time)\b", raw_text):
        return f"The current time is {datetime.datetime.now().strftime('%H:%M')}."

    elif re.search(r"\b(date|today's date|what day)\b", raw_text):
        return f"Today's date is {datetime.datetime.now().strftime('%d-%m-%Y')}."

    elif re.search(r"\b(who are you|your name|what is your name)\b", raw_text):
        return "My Name is Alpha, I'm your chatAlpha assistant!"

    elif any(word in tokens for word in ["thanks", "thank", "thankyou", "thanku"]):
        return "You're welcome! Sir."

    elif any(word in tokens for word in ["weather", "temperature", "rain", "sunny"]):
        return "I'm not connected to weather APIs yet, but it looks like a great day!"

    elif "open youtube" in raw_text:
        wb.open("https://www.youtube.com")
        return "Opening YouTube..."

    elif "open" in raw_text and "and" in raw_text:
        if open_websites(raw_text):
            return "Opening requested websites..."
        else:
            return "Sorry, I couldn't open the sites."

    elif any(raw_text.startswith(cmd) for cmd in
             ["open ", "close ", "play ", "google search ", "youtube search ", "system "]):
        asyncio.run(TranslateAndExecute([raw_text]))
        return "Searching and executing....."

    elif any(word in tokens for word in ["bye", "goodbye", "see you", "exit", "quit", "time to sleep"]):
        return "Goodbye! Talk to you later."

    else:
        return "I'm sorry, I didn't understand that...."
def load_history():
    try:
        with open("chat_history.txt", "r", encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError:
        return []


def save_message(message, sender):
    timestamp = datetime.datetime.now().strftime('%H:%M')
    with open("chat_history.txt", "a", encoding="utf-8") as file:
        file.write(f"{sender}|{timestamp}|{message}\n")


def clear_chat():
    confirm = messagebox.askyesno("Clear Chat", "can i clear the chat history?")
    if confirm:
        for widget in chat_frame.winfo_children():
            widget.destroy()
        open("chat_history.txt", "w").close()
        Alpha_greeting()


def add_message(msg, sender, timestamp=None):
    if not timestamp:
        timestamp = datetime.datetime.now().strftime('%H:%M')

    bg_color = "#2a2d31" if sender == "Alpha" else "#3a3f44"
    fg_color = "#e0e0e0"
    avatar_img = b_avatar if sender == "Alpha" else u_avatar

    outer = tk.Frame(chat_frame, bg=chat_frame["bg"])
    outer.pack(fill="x", padx=10, pady=5)

    if sender == "Alpha":
        bubble_frame = tk.Frame(outer, bg=chat_frame["bg"])
        bubble_frame.grid(column=0, row=0, sticky="w")

        avatar = tk.Label(bubble_frame, image=avatar_img, bg=chat_frame["bg"])
        avatar.grid(row=0, column=0, sticky="w")

        text_label = tk.Label(
            bubble_frame,
            text=f"{msg}\n🕒 {timestamp}",
            font=("Calibri", 12),
            bg=bg_color,
            fg=fg_color,
            wraplength=450,
            justify="left",
            padx=10,
            pady=6
        )
        text_label.grid(row=0, column=1, padx=5, sticky="w")

    else:
        bubble_frame = tk.Frame(outer, bg=chat_frame["bg"])
        bubble_frame.grid(column=1, row=0, sticky="e")

        text_label = tk.Label(
            bubble_frame,
            text=f"{msg}\n🕒 {timestamp}",
            font=("Calibri", 12),
            bg=bg_color,
            fg=fg_color,
            wraplength=450,
            justify="left",
            padx=10,
            pady=6
        )
        text_label.grid(row=0, column=0, padx=5, sticky="e")

        avatar = tk.Label(bubble_frame, image=avatar_img, bg=chat_frame["bg"])
        avatar.grid(row=0, column=1, sticky="e")

    canvas.update_idletasks()
    canvas.yview_moveto(1)


def Alpha_greeting():
    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        greet = "Good Morning Sir!"
    elif 12 <= hour < 16:
        greet = "Good Afternoon Sir!"
    elif 16 <= hour < 24:
        greet = "Good Evening Sir!"
    else:
        greet = "Hello Sir!"
    add_message(greet + "\nHow may I help you? (Type 'bye' to exit)", "Alpha")
    save_message(greet + "\nHow may I help you? (Type 'bye' to exit)", "Alpha")


def send_message(event=None):
    user_msg = user_entry.get().strip()
    if user_msg == "":
        return
    timestamp = datetime.datetime.now().strftime('%H:%M')
    add_message(user_msg, "user", timestamp)
    save_message(user_msg, "user")
    user_entry.delete(0, tk.END)

    Alpha_msg = generate_response(user_msg)
    add_message(Alpha_msg, "Alpha")
    save_message(Alpha_msg, "Alpha")
    
root = tk.Tk()
root.title("💬 Alpha ChatAlpha")
root.geometry("500x700")
root.resizable(False, False)
bg_color, chat_bg, entry_bg = "#1c1c1c", "#1e1e1e", "#2a2a2a"
text_fg, btn_fg= "white", "white"
root.configure(bg=bg_color)
user_img = Image.open("user.png").resize((40, 40))
Alpha_img = Image.open("Alpha.png").resize((40, 40))
u_avatar = ImageTk.PhotoImage(user_img)
b_avatar = ImageTk.PhotoImage(Alpha_img)
canvas = Canvas(root, bg=chat_bg, highlightthickness=0)
chat_scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
chat_frame = Frame(canvas, bg=chat_bg)
chat_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=chat_frame, anchor="nw")
canvas.configure(yscrollcommand=chat_scrollbar.set)
canvas.pack(side="top", fill="both", expand=True, padx=(10, 0), pady=(10, 0))
chat_scrollbar.pack(side="right", fill="y")
input_frame = tk.Frame(root, bg=bg_color)
input_frame.pack(padx=10, pady=10, fill=tk.X)
user_entry = tk.Entry(input_frame, font=("Calibri", 13), bg=entry_bg, fg=text_fg, insertbackground="white")
user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=6)
user_entry.bind("<Return>", send_message)
send_button = tk.Button(input_frame, text="Send", command=send_message, bg="#4CAF50", fg=btn_fg,font=("Calibri", 12, "bold"))
send_button.pack(side=tk.LEFT)
clear_button = tk.Button(input_frame, text="Clear", command=clear_chat, bg="#E53935", fg=btn_fg, font=("Calibri", 12, "bold"))
clear_button.pack(side=tk.LEFT, padx=(10, 0))
for line in load_history():
    if "|" in line:
        parts = line.strip().split("|")
        if len(parts) == 3:
            sender, timestamp, message = parts
            if sender in ["user", "Alpha"]:
                add_message(message.strip(), sender, timestamp)

if not load_history():
    Alpha_greeting()

user_entry.focus()
root.mainloop()
