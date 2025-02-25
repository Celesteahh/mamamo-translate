import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator
from PIL import Image, ImageTk  # For background image handling
import json

# Initialize Translator
translator = Translator()
translation_history = []

# Create GUI window
root = tk.Tk()
root.title ("MAMAMO TRANSLATOR")
root.geometry("700x700")

#Background Image
bg_image = Image.open("Pastel BG.jpg")   
bg_image = bg_image.resize((700, 700))   
bg_photo = ImageTk.PhotoImage(bg_image)  

#Display Background
canvas = tk.Canvas(root, width=700, height=700)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

#Widgets
frame = tk.Frame(root, bg="white", padx=20, pady=20, bd=5, relief="ridge")
frame.place(relx=0.5, rely=0.5, anchor="center") 

#Languages
languages = {
    "English": "en",
    "Cebuano": "ceb",
    "Filipino (Tagalog)": "tl",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW"
}
language_names = list(languages.keys())

# Function Definitions
def translate_text():
    try:
        source_lang = languages[source_lang_combobox.get()]
        target_lang = languages[target_lang_combobox.get()]
        text = input_text.get("1.0", tk.END).strip()

        if not text:
            messagebox.showerror("Error", "Please enter text to translate.")
            return

        translated = translator.translate(text, src=source_lang, dest=target_lang) 
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated.text)

        # Save to history
        translation_history.append({"source": text, "translated": translated.text})
        update_history()
    except Exception as e:
        messagebox.showerror("Error", f"Translation failed: {e}")

def update_history():
    history_listbox.delete(0, tk.END)
    for entry in translation_history:
        history_listbox.insert(tk.END, f"{entry['source']} -> {entry['translated']}")

def save_history():
    with open("translation_history.json", "w") as file:
        json.dump(translation_history, file, indent=4)
    messagebox.showinfo("Success", "Translation history saved!")

def clear_text():
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)

tk.Label(frame, text="Source Language:", bg="white", font=("Arial", 12, "bold")).pack()
source_lang_combobox = ttk.Combobox(frame, values=language_names, state="readonly", font=("Arial", 10))
source_lang_combobox.set("English")  #english default
source_lang_combobox.pack(pady=5)

tk.Label(frame, text="Target Language:", bg="white", font=("Arial", 12, "bold")).pack()
target_lang_combobox = ttk.Combobox(frame, values=language_names, state="readonly", font=("Arial", 10))
target_lang_combobox.set("Filipino (Tagalog)")  # filipino default
target_lang_combobox.pack(pady=5)

tk.Label(frame, text="Enter Text:", bg="white", font=("Arial", 12, "bold")).pack()
input_text = tk.Text(frame, height=3, font=("Arial", 10), bd=2, relief="solid")
input_text.pack(pady=5)

translate_btn = tk.Button(frame, text="Translate", command=translate_text, font=("Arial", 12, "bold"), bg="#CBC3E3", fg="black", bd=3, relief="raised")
translate_btn.pack(pady=5)

clear_btn = tk.Button(frame, text="Clear", command=clear_text, font=("Arial", 12, "bold"), bg="#CF9FFF", fg="black", bd=3, relief="raised")
clear_btn.pack(pady=5)

save_btn = tk.Button(frame, text="Save History", command=save_history, font=("Arial", 12, "bold"), bg="#AA98A9", fg="black", bd=3, relief="raised")
save_btn.pack(pady=5)

tk.Label(frame, text="Translated Text:", bg="white", font=("Arial", 12, "bold")).pack()
output_text = tk.Text(frame, height=3, font=("Arial", 10), bd=2, relief="solid")
output_text.pack(pady=5)

tk.Label(frame, text="Translation History:", bg="white", font=("Arial", 12, "bold")).pack()
history_listbox = tk.Listbox(frame, height=5, font=("Arial", 10), bd=2, relief="solid")
history_listbox.pack(pady=5)

root.mainloop()

