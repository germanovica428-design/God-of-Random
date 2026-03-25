import customtkinter as ctk
import secrets
import string
import gc
import ctypes
from tkinter import messagebox

try:
    import pyperclip
    PYPERCLIP_READY = True
except ImportError:
    PYPERCLIP_READY = False

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class OrionProjectApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("God of Random v1.8.6")
        self.geometry("500x420")
        self.resizable(False, False)
        self.focus_set()
        self.bind("<Button-1>", lambda e: self.focus_set())
        self.bind("<FocusIn>", lambda e: self.focus_set())

        self.сложность = "Мужик"
        self.скрыто = True
        self.таймер_id = None

        self.menu_frame = ctk.CTkFrame(self, height=40, fg_color="transparent")
        self.menu_frame.pack(fill="x", padx=10, pady=10)

        self.pray_var = ctk.StringVar(value="Мужик")
        self.btn_pray_for = ctk.CTkOptionMenu(
            self.menu_frame, values=["Детский сад", "Мужик", "Хардкор"],
            command=self.set_complexity, variable=self.pray_var, width=160
        )
        self.btn_pray_for.pack(side="left", padx=5)

        self.btn_creators = ctk.CTkButton(
            self.menu_frame, text="Создатели", width=100,
            command=self.show_creators, fg_color="#333333", hover_color="#444444"
        )
        self.btn_creators.pack(side="right", padx=5)

        self.res_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", border_width=1)
        self.res_frame.pack(pady=15, padx=20, fill="x")

        self.entry = ctk.CTkEntry(
            self.res_frame, font=("Consolas", 20), show="*",
            border_width=0, fg_color="#1a1a1a", justify="center"
        )
        self.entry.pack(side="left", expand=True, fill="x", padx=(10, 5), pady=15)
        self.entry.bind("<Key-Escape>", lambda e: self.on_closing())

        self.eye_btn = ctk.CTkButton(
            self.res_frame, text="👁", width=40, command=self.toggle_eye,
            fg_color="transparent", hover_color="#2b2b2b"
        )
        self.eye_btn.pack(side="right", padx=(0, 10))

        self.len_label = ctk.CTkLabel(self, text="Длина откровения: 12")
        self.len_label.pack()

        self.slider = ctk.CTkSlider(
            self, from_=4, to=32, number_of_steps=28, command=self.update_slider_label
        )
        self.slider.set(12)
        self.slider.pack(pady=(5, 15), padx=40, fill="x")

        self.progress = ctk.CTkProgressBar(self, height=10)
        self.progress.pack(padx=50, pady=5)
        self.progress.set(12 / 32.0)

        self.btn_main = ctk.CTkButton(
            self, text="Воздать молитву богу рандома", height=45, command=self.generate_password
        )
        self.btn_main.pack(pady=(20, 10), padx=40, fill="x")

        self.btn_copy = ctk.CTkButton(
            self, text="Скопировать откровения", fg_color="transparent",
            border_width=1, text_color="#aaaaaa", command=self.copy_to_clipboard
        )
        self.btn_copy.pack(pady=5)

        self.bind_all("<Key-Escape>", lambda e: self.on_closing())
        self.bind("<Unmap>", lambda e: self.hide_on_minimize())
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def set_complexity(self, choice):
        self.сложность = choice

    def toggle_eye(self):
        self.скрыто = not self.скрыто
        self.entry.configure(show="*" if self.скрыто else "")

    def update_slider_label(self, value):
        val = int(value)
        self.len_label.configure(text=f"Длина откровения: {val}")
        self.progress.set(val / 32.0)

    def generate_password(self):
        self.clear_clipboard()
        длина = int(self.slider.get())
        if self.сложность == "Хардкор":
            if длина < 8:
                длина = 8
                self.slider.set(8)
                self.update_slider_label(8)
            обязаловка = [
                secrets.choice(string.ascii_lowercase),
                secrets.choice(string.ascii_uppercase),
                secrets.choice(string.digits),
                secrets.choice(string.punctuation)
            ]
            if длина >= 12:
                обязаловка.append(secrets.choice(string.digits))
                обязаловка.append(secrets.choice(string.punctuation))
            if длина >= 16:
                обязаловка.append(secrets.choice(string.ascii_uppercase))
                обязаловка.append(secrets.choice(string.ascii_lowercase))
            набор = string.ascii_letters + string.digits + string.punctuation
            хвост = [secrets.choice(набор) for _ in range(длина - len(обязаловка))]
            итого = обязаловка + хвост
            secrets.SystemRandom().shuffle(итого)
            пароль = ''.join(итого)
        elif self.сложность == "Мужик":
            набор = string.ascii_letters + (string.digits * 3)
            пароль = ''.join(secrets.choice(набор) for _ in range(длина))
        else:
            набор = string.digits
            пароль = ''.join(secrets.choice(набор) for _ in range(длина))
        self.entry.delete(0, 'end')
        self.entry.insert(0, пароль)
        пароль = None
        gc.collect()
        self.btn_main.configure(text="Молитва услышана!")
        self.after(1000, lambda: self.btn_main.configure(text="Воздать молитву богу рандома"))

    def copy_to_clipboard(self):
        if not PYPERCLIP_READY:
            messagebox.showerror("Ошибка", "pyperclip не найден!")
            return
        текст = self.entry.get()
        if self.btn_copy.cget("state") == "disabled" or not текст:
            return
        try:
            pyperclip.copy(текст)
            self.скрыто = True
            self.entry.configure(show="*")
            self.btn_main.configure(state="disabled", text="В БУФЕРЕ...")
            self.btn_copy.configure(state="disabled", text="45 сек")
            if self.таймер_id:
                self.after_cancel(self.таймер_id)
            self._countdown(45)
        except Exception:
            pass

    def _countdown(self, sec):
        if sec <= 0:
            self.clear_clipboard()
            return
        self.btn_copy.configure(text=f"{sec} сек")
        self.таймер_id = self.after(1000, self._countdown, sec - 1)

    def clear_clipboard(self):
        if self.таймер_id:
            self.after_cancel(self.таймер_id)
            self.таймер_id = None
        try:
            user32 = ctypes.windll.user32
            for _ in range(3):
                if user32.OpenClipboard(0):
                    user32.EmptyClipboard()
                    user32.CloseClipboard()
                ctypes.windll.kernel32.Sleep(15)
            if PYPERCLIP_READY:
                pyperclip.copy("")
        except Exception:
            pass
        self.entry.delete(0, 'end')
        self.скрыто = True
        self.entry.configure(show="*")
        gc.collect()
        self.btn_main.configure(state="normal", text="Воздать молитву богу рандома")
        self.btn_copy.configure(state="normal", text="Скопировать откровения",
                               fg_color="transparent", text_color="#aaaaaa")

    def on_closing(self):
        self.clear_clipboard()
        self.destroy()

    def hide_on_minimize(self, event=None):
        self.скрыто = True
        self.entry.configure(show="*")

    def show_creators(self):
        creators_info = "Создано с помощью ИИ\nGemini 3 Flash\nПроверил и доработал Grok (xAI)\nАвтор идеи: Александр"
        messagebox.showinfo("Создатели", creators_info)

if __name__ == "__main__":
    app = OrionProjectApp()
    app.mainloop()