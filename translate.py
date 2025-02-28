import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator
from PIL import Image, ImageTk

import requests  # For API calls

# Initialize Translator
translator = Translator()

# Dictionary of supported languages
languages = {
    "English": "en", "Cebuano": "ceb", "Filipino (Tagalog)": "tl",
    "Spanish": "es", "French": "fr", "German": "de", 
    "Japanese": "ja", "Korean": "ko", "Chinese (Simplified)": "zh-CN"
}
language_names = list(languages.keys())

# Function to translate text
def translate_text():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("Error", "Please enter text to translate.")
        return

    source_lang = languages.get(source_lang_combobox.get(), "en")
    target_lang = languages.get(target_lang_combobox.get(), "tl")

    try:
        translated = translator.translate(text, src=source_lang, dest=target_lang)
        output_text.config(state="normal")  # Enable editing output box
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated.text)
        output_text.config(state="disabled")  # Disable editing output box
    except Exception as e:
        messagebox.showerror("Error", f"Translation failed: {e}")

# Function to get dictionary definition
def get_definition():
    word = input_text.get("1.0", tk.END).strip()
    if not word:
        messagebox.showerror("Error", "Please enter a word to search.")
        return

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    try:
        response = requests.get(url, timeout=5)  # Timeout after 5 seconds
        response.raise_for_status()  # Raise error if request fails

        data = response.json()
        if isinstance(data, list) and "meanings" in data[0]:
            definitions = [f"- {d['definition']}" for d in data[0]['meanings'][0]['definitions']]
            meaning_text = "\n".join(definitions[:3])  # Show up to 3 definitions
        else:
            meaning_text = "Definition not found."

        output_text.config(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Definitions:\n{meaning_text}")
        output_text.config(state="disabled")

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch definition:\n{e}")

# Function to clear input & output text
def clear_text():
    input_text.delete("1.0", tk.END)
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.config(state="disabled")

# GUI Setup
root = tk.Tk()
root.title("Language Translator & Dictionary")
root.geometry("700x600")
root.configure(bg="#f5f5f5")  # Set background color

# Frame for UI elements
frame = tk.Frame(root, bg="white", padx=20, pady=20, bd=5, relief="ridge")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Language Selection
tk.Label(frame, text="Source Language:", bg="white", font=("Arial", 12, "bold")).pack()
source_lang_combobox = ttk.Combobox(frame, values=language_names, state="readonly")
source_lang_combobox.set("English")
source_lang_combobox.pack(pady=5)

tk.Label(frame, text="Target Language:", bg="white", font=("Arial", 12, "bold")).pack()
target_lang_combobox = ttk.Combobox(frame, values=language_names, state="readonly")
target_lang_combobox.set("Filipino (Tagalog)")
target_lang_combobox.pack(pady=5)

# Text Input
tk.Label(frame, text="Enter Text/Word:", bg="white", font=("Arial", 12, "bold")).pack()
input_text = tk.Text(frame, height=3, font=("Arial", 10))
input_text.pack(pady=5)

# Buttons
button_frame = tk.Frame(frame, bg="white")
button_frame.pack(pady=5)

translate_btn = tk.Button(button_frame, text="Translate", command=translate_text, font=("Arial", 12, "bold"), bg="#6fa3ef", fg="white", padx=10, pady=5)
translate_btn.grid(row=0, column=0, padx=5, pady=5)

dictionary_btn = tk.Button(button_frame, text="Get Definition", command=get_definition, font=("Arial", 12, "bold"), bg="#ffb3b3", fg="black", padx=10, pady=5)
dictionary_btn.grid(row=0, column=1, padx=5, pady=5)

clear_btn = tk.Button(button_frame, text="Clear", command=clear_text, font=("Arial", 12, "bold"), bg="#b0c4de", fg="black", padx=10, pady=5)
clear_btn.grid(row=0, column=2, padx=5, pady=5)

# Output Box
tk.Label(frame, text="Output:", bg="white", font=("Arial", 12, "bold")).pack()
output_text = tk.Text(frame, height=4, font=("Arial", 10))
output_text.pack(pady=5)
output_text.config(state="disabled")  # Initially disable output box

root.mainloop()
