import os
import arabic_reshaper
from bidi.algorithm import get_display

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle
from kivy.core.text import LabelBase

# --- Шрифт ---
# Регистрируем Amiri под именем "Amiri", чтобы использовать в font_name="Amiri"
FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts", "Amiri-Regular.ttf")
LabelBase.register(name="Amiri", fn_regular=FONT_PATH)

# --- Цвета ---
BG_COLOR    = get_color_from_hex("#0D1B3E")   # тёмно-синий фон
TEXT_COLOR  = get_color_from_hex("#F0EAD6")   # кремовый текст
BTN_GREEN   = (0.13, 0.45, 0.30, 1)           # кнопка +1
BTN_GRAY    = (0.25, 0.28, 0.35, 1)           # кнопка сброса

# --- Арабские зикры ---
# arabic_reshaper соединяет буквы в правильную вязь,
# get_display разворачивает строку справа-налево (bidi-алгоритм)
_RAW_ZIKRS = [
    "سُبْحَانَ ٱللَّٰه",
    "ٱلْحَمْدُ لِلَّٰه",
    "ٱللَّٰهُ أَكْبَر",
]
ZIKRS = [get_display(arabic_reshaper.reshape(z)) for z in _RAW_ZIKRS]

# Русские названия для подписи (чтобы ты знал, какой зикр)
ZIKRS_RU = ["СубханАллах", "Альхамдулиллах", "Аллаху Акбар"]


class ZikrCounter(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = [20, 30, 20, 20]
        self.spacing = 10

        # Тёмно-синий фон: рисуем прямоугольник на canvas
        with self.canvas.before:
            Color(*BG_COLOR)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        # Записная книжка на диске
        self.store = JsonStore("zikr.json")
        if self.store.exists("data"):
            data = self.store.get("data")
            self.total = data["total"]
            self.zikr_index = data["zikr_index"]
        else:
            self.total = 0
            self.zikr_index = 0

        self.count = 0
        self.circles = 0

        # Загружаем звук щелчка
        sound_path = os.path.join(os.path.dirname(__file__), "sounds", "click.wav")
        self.click_sound = SoundLoader.load(sound_path)

        # --- Виджеты ---

        # Русское название зикра (маленькое, сверху)
        self.zikr_ru_label = Label(
            font_size="18sp",
            color=get_color_from_hex("#8899BB"),  # приглушённый синеватый
            size_hint=(1, 0.15),
        )

        # Арабская вязь — большая, шрифт Amiri
        self.zikr_label = Label(
            font_name="Amiri",
            font_size="48sp",
            color=TEXT_COLOR,
            size_hint=(1, 0.25),
        )

        # Большая цифра счётчика
        self.count_label = Label(
            font_size="100sp",
            bold=True,
            color=TEXT_COLOR,
            size_hint=(1, 0.3),
        )

        # Кругов и всего
        self.circles_label = Label(
            font_size="20sp",
            color=get_color_from_hex("#AABBCC"),
            size_hint=(1, 0.1),
        )
        self.total_label = Label(
            font_size="18sp",
            color=get_color_from_hex("#8899BB"),
            size_hint=(1, 0.1),
        )

        # Кнопка +1
        plus_button = Button(
            text="+1",
            font_size="54sp",
            size_hint=(1, 0.35),
            background_color=BTN_GREEN,
            background_normal="",  # убирает стандартную текстуру Kivy
        )
        plus_button.bind(on_press=self.add_one)

        # Кнопка сброса
        reset_button = Button(
            text="Сброс круга",
            font_size="22sp",
            size_hint=(1, 0.12),
            background_color=BTN_GRAY,
            background_normal="",
        )
        reset_button.bind(on_press=self.reset_circle)

        for w in [
            self.zikr_ru_label,
            self.zikr_label,
            self.count_label,
            self.circles_label,
            self.total_label,
            plus_button,
            reset_button,
        ]:
            self.add_widget(w)

        self.update_screen()

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def add_one(self, instance):
        self.count += 1
        self.total += 1

        # Звук на каждое нажатие
        self.play_click()
        # Вибрация на каждое нажатие (короткая, работает на телефоне)
        self.vibrate(0.05)

        if self.count >= 33:
            self.count = 0
            self.circles += 1
            self.next_zikr()

        self.save()
        self.update_screen()

    def play_click(self):
        if self.click_sound:
            # stop() перед play() позволяет быстро кликать без наложений
            self.click_sound.stop()
            self.click_sound.play()

    def next_zikr(self):
        self.zikr_index = (self.zikr_index + 1) % len(ZIKRS)

    def reset_circle(self, instance):
        self.count = 0
        self.save()
        self.update_screen()

    def vibrate(self, duration=0.05):
        try:
            from plyer import vibrator
            vibrator.vibrate(duration)
        except Exception:
            pass

    def save(self):
        self.store.put("data", total=self.total, zikr_index=self.zikr_index)

    def update_screen(self):
        self.zikr_ru_label.text = ZIKRS_RU[self.zikr_index]
        self.zikr_label.text = ZIKRS[self.zikr_index]
        self.count_label.text = str(self.count)
        self.circles_label.text = f"Кругов: {self.circles}"
        self.total_label.text = f"Всего за всё время: {self.total}"


class ZikrApp(App):
    def build(self):
        self.title = "Зикр"
        # Цвет фона окна на десктопе
        Window.clearcolor = get_color_from_hex("#0D1B3E")
        return ZikrCounter()


if __name__ == "__main__":
    ZikrApp().run()
