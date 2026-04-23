import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

HISTORY_FILE = "history.json"
MIN_LENGTH, MAX_LENGTH = 6, 32

def initialize_history_file():
    """Создаёт файл history.json с пустым списком, если его нет."""
    if not os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
        except OSError as e:
            messagebox.showerror("Ошибка", f"Не удалось создать файл истории: {e}")
            return False
    return True

def load_history():
    """Загружает историю из файла. Возвращает пустой список при ошибках."""
    if not initialize_history_file():
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                raise json.JSONDecodeError("Данные не являются списком", "", 0)
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл истории не найден. Будет создан новый.")
        return []
    except json.JSONDecodeError as e:
        messagebox.showerror("Ошибка", f"Файл истории повреждён: {e}. Будет создан новый.")
        return []
    except OSError as e:
        messagebox.showerror("Ошибка", f"Ошибка чтения файла: {e}")
        return []

def save_history(history):
    """Сохраняет историю в файл с обработкой ошибок."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except OSError as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")

def generate_password(length, use_digits, use_letters, use_special):
    chars = ""
    if use_digits: chars += string.digits
    if use_letters: chars += string.ascii_letters
    if use_special: chars += string.punctuation
    if not chars:
        return None
    return ''.join(random.choices(chars, k=length))

def on_generate():
    try:
        length = int(scale_length.get())
        if length < MIN_LENGTH or length > MAX_LENGTH:
            raise ValueError(f"Длина должна быть от {MIN_LENGTH} до {MAX_LENGTH}")
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))
        return

    use_digits = var_digits.get()
    use_letters = var_letters.get()
    use_special = var_special.get()

 
