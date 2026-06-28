[app]

# Название и идентификатор приложения
title = Зикр
package.name = zikr
package.domain = org.gamidoff

# Точка входа
source.dir = .
source.main = main.py

# ВАЖНО: по умолчанию Buildozer берёт только .py файлы.
# Добавляем расширения, чтобы шрифт и звук попали в APK.
source.include_exts = py,png,jpg,kv,atlas,ttf,wav,json

# Явно указываем папки с ассетами
source.include_patterns = fonts/*.ttf,sounds/*.wav

version = 0.1

# Все Python-зависимости приложения.
# arabic-reshaper и python-bidi нужны для арабской вязи.
# Примечание: в buildozer пакеты через запятую БЕЗ пробелов.
requirements = python3,kivy==2.3.1,plyer,arabic-reshaper,python-bidi

# Заставка и иконка (можно добавить позже)
# presplash.filename = %(source.dir)s/data/presplash.png
# icon.filename = %(source.dir)s/data/icon.png

[buildozer]

# Уровень логов: 0=тихо, 1=инфо, 2=отладка
log_level = 2

[app:android]

# Минимальная версия Android (API 21 = Android 5.0)
android.minapi = 21

# Целевая версия Android для Google Play
android.api = 34

# NDK версия (Buildozer скачает автоматически)
android.ndk = 25b

# Фиксируем версию build-tools.
# 34.0.0 — стабильная, лицензия принимается без проблем.
# 37 — слишком новая, на CI падает с "license not accepted".
android.build_tools_version = 34.0.0

# Права приложения
# VIBRATE — для вибрации при нажатии
# INTERNET не нужен (работаем офлайн)
android.permissions = VIBRATE

# Ориентация экрана — portrait (вертикальная), как у телефона
orientation = portrait

# Fullscreen: 0 = показываем статус-бар Android
fullscreen = 0
