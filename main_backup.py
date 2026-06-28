from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window

# Список зикров по кругу
ZIKRS = ["СубханАллах", "Альхамдулиллах", "Аллаху Акбар"]

class ZikrCounter(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Записная книжка на диске — не забывает после закрытия
        self.store = JsonStore("zikr.json")

        # Достаём сохранённое, или начинаем с нуля
        if self.store.exists("data"):
            data = self.store.get("data")
            self.total = data["total"]
            self.zikr_index = data["zikr_index"]
        else:
            self.total = 0
            self.zikr_index = 0

        self.count = 0      # текущий круг (в памяти, обнуляется)
        self.circles = 0    # сколько кругов за сессию

        # --- Сцена: виджеты на экране ---
        self.zikr_label = Label(font_size="32sp")
        self.count_label = Label(font_size="90sp", bold=True)
        self.total_label = Label(font_size="22sp")
        self.circles_label = Label(font_size="20sp")

        plus_button = Button(text="+1", font_size="50sp",
                             size_hint=(1, 2),
                             background_color=(0.2, 0.6, 0.4, 1))
        plus_button.bind(on_press=self.add_one)

        reset_button = Button(text="Сброс круга", font_size="22sp",
                              size_hint=(1, 0.4))
        reset_button.bind(on_press=self.reset_circle)

        # Складываем всё на экран
        self.add_widget(self.zikr_label)
        self.add_widget(self.count_label)
        self.add_widget(self.circles_label)
        self.add_widget(self.total_label)
        self.add_widget(plus_button)
        self.add_widget(reset_button)

        self.update_screen()

    def add_one(self, instance):
        self.count += 1
        self.total += 1
        if self.count >= 33:
            self.count = 0
            self.circles += 1
            self.next_zikr()    # переходим к следующему зикру
            self.vibrate()
        self.save()
        self.update_screen()

    def next_zikr(self):
        # Следующий зикр по кругу: Субхан → Альхамду → Аллаху Акбар → снова
        self.zikr_index = (self.zikr_index + 1) % len(ZIKRS)

    def reset_circle(self, instance):
        # Сбрасываем ТОЛЬКО текущий круг. Общий не трогаем!
        self.count = 0
        self.save()
        self.update_screen()

    def vibrate(self):
        # Вибрация работает только на телефоне, на маке тихо промолчит
        try:
            from plyer import vibrator
            vibrator.vibrate(0.1)
        except Exception:
            pass

    def save(self):
        # Записываем в файл, чтобы пережило закрытие
        self.store.put("data", total=self.total, zikr_index=self.zikr_index)

    def update_screen(self):
        self.zikr_label.text = ZIKRS[self.zikr_index]
        self.count_label.text = str(self.count)
        self.circles_label.text = f"Кругов: {self.circles}"
        self.total_label.text = f"Всего за всё время: {self.total}"

class ZikrApp(App):
    def build(self):
        self.title = "Зикр"
        return ZikrCounter()

if __name__ == "__main__":
    ZikrApp().run()
