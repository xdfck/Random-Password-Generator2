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

    password = generate_password(length, use_digits, use_letters, use_special)
    if not password:
        messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
        return

    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)
    
    history.append(password)
    save_history(history)
    update_history_table()

def update_history_table():
    for i in tree.get_children():
        tree.delete(i)
    for p in history:
        tree.insert("", tk.END, values=(p,))

# --- Инициализация ---
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("500x400")
root.grid_columnconfigure(1, weight=1)  # Для растягивания интерфейса

# Загрузка истории при старте
history = load_history()

# --- Вкладка "Генерация" ---
frame_gen = ttk.LabelFrame(root, text="Генерация пароля")
frame_gen.pack(fill=tk.X, padx=10, pady=5)

ttk.Label(frame_gen, text="Длина:").grid(row=0, column=0, padx=5, pady=5)
scale_length = ttk.Scale(frame_gen, from_=MIN_LENGTH, to=MAX_LENGTH, orient=tk.HORIZONTAL)
scale_length.set(12)
scale_length.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

var_digits = tk.BooleanVar(value=True)
ttk.Checkbutton(frame_gen, text="Цифры", variable=var_digits).grid(row=1, column=0, sticky="w", padx=10)
var_letters = tk.BooleanVar(value=True)
ttk.Checkbutton(frame_gen, text="Буквы", variable=var_letters).grid(row=1, column=1, sticky="w", padx=10)
var_special = tk.BooleanVar(value=True)
ttk.Checkbutton(frame_gen, text="Спецсимволы", variable=var_special).grid(row=1, column=2, sticky="w", padx=10)

ttk.Button(frame_gen, text="Сгенерировать", command=on_generate).grid(row=2, column=0, columnspan=3, pady=15)

ttk.Label(frame_gen, text="Результат:").grid(row=3, column=0, padx=10)
entry_password = ttk.Entry(frame_gen)
entry_password.grid(row=3, column=1, columnspan=2, sticky="ew", padx=10)

# --- Таблица истории ---
tree = ttk.Treeview(root, columns=("password",), show="headings")
tree.heading("password", text="История паролей")
tree.pack(fill="both", expand=True, padx=10, pady=10)

update_history_table()
root.mainloop()
