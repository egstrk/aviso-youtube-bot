# aviso-youtube-bot

Бот обеспечивает платные просмотры видео с YouTube на площадке Aviso

## Зависимости
- Firefox
- [geckodriver](https://github.com/mozilla/geckodriver/releases)
- [selenium](https://pypi.org/project/selenium/)

## Запуск

Перед запуском бота запустить скрипт для записи файла с данными авторизации

	python make_cookies.py

Откроется окно браузера с главной страницей сайта Aviso, необходимо вручную авторизироваться, после чего нажать любую клавишу в консоли для завершения скрипта. В результате будет записан файл cookies с данными авторизации.
[label](http://example.com)
Теперь можно запустить бота

	python aviso_youtube.py

