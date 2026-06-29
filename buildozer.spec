[app]

title = Зикр
package.name = zikr
package.domain = org.gamidoff

source.dir = .
source.main = main.py

source.include_exts = py,png,jpg,kv,atlas,ttf,wav,json
source.include_patterns = fonts/*.ttf,sounds/*.wav

version = 0.1

requirements = python3,kivy,plyer,arabic-reshaper,python-bidi

[buildozer]

log_level = 2

[app:android]

android.minapi = 21
android.api = 33
android.ndk = 25b
android.accept_sdk_license = True
android.permissions = VIBRATE

orientation = portrait
fullscreen = 0
