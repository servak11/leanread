"""
English Learning Tool
---------------------
A Tkinter-based application for learning foreign words and pronunciation by reading articles and selecting words to learn

Features:
- Open and save text files (R-8, R-9, R-10).
- Display file path in a label.
- Text-to-speech conversion with gTTS and playback via pygame (R-11, R-12).
- Vocabulary dictionary with translations using deep-translator (R-20, R-21).
- Status bar for user feedback (R-50 to R-53).
- Vertical scrollbar for text area (R-101).
- Word/phrase cleanup before adding to dictionary (R-61, R-62).
---------------------
TKinter App to learn english words and word pronouncation using short texts

# text
R-1. On the left side an edit control where I can display text of an article
R-101. The edit control shall have vertical scroll bar
R-2. I can open a text file or just paste a text.

# words to learn
R-4. On the right side I have a table of words I did not know or wanted to learn.
R-5. I can select a word in the edit control and press Add button, this will add the word into the table of words to learn
R-6. In the list table I wanted to learn the left column shall contain the words I added, and the right column shall contain the translation to german language
R-61. Before a single word was added, it shall be stripped from whitespace and punktuation.
R-62. If a phrase was selected, it shall be stripped from starting and ending punktuation.
R-63. The converted words shall be stored in the subdirectory wordsmp3


# status bar
R-50. Need status bar between the button bar and progress bar.
R-51. If the same word is selected and Add button clicked the status bar displays "already in the Dictionary"
R-52. The table of words to learn shall be in groupbox  saying "Dictionary to learn"
R-53. All button actions shall end with a corresponding status message displayed in the status bar.

# text file management
R-8. When I open file the file name with path appears in the label above the Open button
R-9. Add "Save" button which saves the file to either the file which was open or to a file "text.txt" if nothing was selected before
R-10. At program start the last file selected or saved shall be reopened.
R-81. When the "Save" button pressed, the current dictionary of words shall be saved to a file with the same name as the opened file with extension json
R-82. If no file was saved/selected, then the dictionary is saved to text.json
R-83. The dictionary is saved in json format.
R-84. If a new text file is opened and the dictionary json with the same exists, the dictionary is loaded from the file to the table of words to learn

# play text
R-11. The conversion to text lasts a while, so a progress bar shall be displayed to the right of the buttons panel showing conversion in progress
R-12. Stop button shall stop reading a long text.
R-13. Move TKinter GUI setup in own function

# word to play conversion
R-3. I can press play button and the app shall convert text to speech using gTTS, save it to output.mp3 and then play it using pygame sound output
R-20. As soon as word adds to the table of words to learn, the app starts a process to convert the (name of the word) to mp3 file called (name of the word).mp3, so that for each word we have its audio representation in the mp3 file named the same as the word itself
R-21. If I click on a word entry (showing "the content of the word entry") in the table of words I wanted to learn, the app plays the related mp3 file using pygame sound output
"""


import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from gtts import gTTS
import pygame
from deep_translator import GoogleTranslator
import re, os, threading, string, json


pygame.mixer.init()

current_file = None
lastfile_cfg = "lastfile.txt"

WORDS_DIR = "wordsmp3"
os.makedirs(WORDS_DIR, exist_ok=True)


def set_status(msg: str):
    """Update the status bar with a message."""
    status_label.config(text=msg)

def load_last_file():
    """Load the last opened or saved file at program start (R-10)."""
    global current_file
    if os.path.exists(lastfile_cfg):
        with open(lastfile_cfg, "r", encoding="utf-8") as f:
            path = f.read().strip()
        if path and os.path.exists(path):
            current_file = path
            with open(path, "r", encoding="utf-8") as f:
                text_area.insert(tk.END, f.read())
            file_label.config(text=f"Opened: {path}")
            set_status("Last file loaded")
            # R-84: Load dictionary JSON if exists
            dict_path = os.path.splitext(path)[0] + ".json"
            if os.path.exists(dict_path):
                load_dictionary(dict_path)

def save_last_file(path: str):
    """Save the path of the last opened or saved file to config."""
    with open(lastfile_cfg, "w", encoding="utf-8") as f:
        f.write(path)

def open_file():
    """Open a text file and display its content in the text area (R-8, R-84)."""
    global current_file
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        current_file = file_path
        with open(file_path, "r", encoding="utf-8") as f:
            text_content = f.read()
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, text_content)
        file_label.config(text=f"Opened: {file_path}")
        save_last_file(file_path)
        set_status("File opened successfully")
        # R-84: Load dictionary JSON if exists
        dict_path = os.path.splitext(file_path)[0] + ".json"
        if os.path.exists(dict_path):
            load_dictionary(dict_path)

def save_file():
    """Save the text area content and dictionary to files (R-9, R-81 to R-83)."""
    global current_file
    if current_file:
        path = current_file
    else:
        path = "text.txt"
        current_file = path
    # Save text
    with open(path, "w", encoding="utf-8") as f:
        f.write(text_area.get("1.0", tk.END))
    file_label.config(text=f"Saved: {path}")
    save_last_file(path)
    set_status("File saved successfully")
    # Save dictionary JSON
    dict_path = os.path.splitext(path)[0] + ".json"
    save_dictionary(dict_path)

def save_dictionary(dict_path: str):
    """Save dictionary table to JSON file (R-81 to R-83)."""
    data = []
    for item in word_table.get_children():
        word, translation = word_table.item(item, "values")
        data.append({"word": word, "translation": translation})
    with open(dict_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    set_status(f"Dictionary saved to {dict_path}")

def load_dictionary(dict_path: str):
    """Load dictionary from JSON file into the table (R-84)."""
    try:
        with open(dict_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        word_table.delete(*word_table.get_children())
        for entry in data:
            word_table.insert("", tk.END, values=(entry["word"], entry["translation"]))
        set_status(f"Dictionary loaded from {dict_path}")
    except Exception as e:
        set_status(f"Failed to load dictionary: {e}")

def play_text():
    """Convert text area content to speech and play it."""
    content = text_area.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Warning", "No text to play!")
        set_status("No text to play")
        return

    def worker():
        progress.start()
        set_status("Converting text to speech...")
        try:
            tts = gTTS(content, lang="en")
            tts.save("output.mp3")
            pygame.mixer.music.load("output.mp3")
            pygame.mixer.music.play()
            set_status("Playing text")
        finally:
            progress.stop()

    threading.Thread(target=worker, daemon=True).start()

def stop_playback():
    """Stop playback of audio."""
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        set_status("Playback stopped")

def clean_selection(text: str) -> str:
    """
    Clean selected text before adding to dictionary.
    - Single word: strip whitespace and remove all punctuation.
    - Phrase: strip whitespace and punctuation only at start/end.
    """
    text = text.strip()
    if " " in text:  # phrase
        text = text.strip(string.punctuation + " ")
    else:  # single word
        text = "".join(ch for ch in text if ch not in string.punctuation)
    return text

def add_word():
    """Add selected word/phrase to dictionary with translation and audio (R-20, R-61, R-62, R-63)."""
    try:
        selected_text = text_area.selection_get()
    except tk.TclError:
        messagebox.showwarning("Warning", "Select a word first!")
        set_status("No word selected")
        return

    cleaned = clean_selection(selected_text)
    if not cleaned:
        set_status("Selection empty after cleanup")
        return

    # Check duplicates
    for item in word_table.get_children():
        if word_table.item(item, "values")[0] == cleaned:
            set_status("already in the Dictionary")
            return

    translation = GoogleTranslator(source="en", target="de").translate(cleaned)
    word_table.insert("", tk.END, values=(cleaned, translation))

    safe_word = re.sub(r'\W+', '_', cleaned)
    filename = os.path.join(WORDS_DIR, f"{safe_word}.mp3")
    tts = gTTS(cleaned, lang="en")
    tts.save(filename)
    set_status(f"Word '{cleaned}' added to dictionary")

def play_word(event):
    """Play audio file for the selected word in the dictionary (R-21, R-63)."""
    selected_item = word_table.selection()
    if selected_item:
        word = word_table.item(selected_item, "values")[0]
        safe_word = re.sub(r'\W+', '_', word)
        filename = os.path.join(WORDS_DIR, f"{safe_word}.mp3")
        if os.path.exists(filename):
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            set_status(f"Playing word '{word}'")
        else:
            set_status(f"No audio file found for {word}")


def create_gui(root):
    """
    Create and layout the Tkinter GUI.

    Includes:
    - File label above text area (R-8).
    - Text area with vertical scrollbar (R-101).
    - Buttons for Open, Save, Play, Stop, Add Word (R-9, R-11, R-12).
    - Status bar for feedback messages (R-50 to R-53).
    - Progress bar below status bar (R-11).
    - Dictionary table inside a groupbox titled 'Dictionary to learn' (R-52).
    """
    global text_area, file_label, progress, word_table, status_label

    root.title("English Learning Tool")

    # Left and right frames
    left_frame = tk.Frame(root)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    right_frame = tk.Frame(root)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # File label (R-8)
    file_label = tk.Label(left_frame, text="No file opened")
    file_label.pack()

    # Text area with vertical scrollbar (R-101)
    text_frame = tk.Frame(left_frame)
    text_frame.pack(fill=tk.BOTH, expand=True)

    text_area = tk.Text(text_frame, wrap="word")
    text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scroll_y = tk.Scrollbar(text_frame, orient="vertical", command=text_area.yview)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    text_area.configure(yscrollcommand=scroll_y.set)

    # Buttons (R-9, R-11, R-12)
    btn_frame = tk.Frame(left_frame)
    btn_frame.pack(fill=tk.X)

    tk.Button(btn_frame, text="Open File", command=open_file).pack(side=tk.LEFT)
    tk.Button(btn_frame, text="Save", command=save_file).pack(side=tk.LEFT)
    tk.Button(btn_frame, text="Play Text", command=play_text).pack(side=tk.LEFT)
    tk.Button(btn_frame, text="Stop", command=stop_playback).pack(side=tk.LEFT)
    tk.Button(btn_frame, text="Add Word", command=add_word).pack(side=tk.LEFT)

    # Status bar (R-50 to R-53)
    status_label = tk.Label(left_frame, text="Ready", anchor="w", relief="sunken")
    status_label.pack(fill=tk.X)

    # Progress bar (R-11)
    progress = ttk.Progressbar(left_frame, mode="indeterminate", length=100)
    progress.pack(fill=tk.X, padx=5, pady=2)

    # Dictionary groupbox (R-52)
    dict_frame = tk.LabelFrame(right_frame, text="Dictionary to learn")
    dict_frame.pack(fill=tk.BOTH, expand=True)

    columns = ("Word", "Translation")
    word_table = ttk.Treeview(dict_frame, columns=columns, show="headings")
    word_table.heading("Word", text="Word")
    word_table.heading("Translation", text="Translation")
    word_table.pack(fill=tk.BOTH, expand=True)

    # Bind click to play word (R-21)
    word_table.bind("<ButtonRelease-1>", play_word)


# --- Main ---
if __name__ == "__main__":
    root = tk.Tk()
    create_gui(root)
    load_last_file()
    root.mainloop()
