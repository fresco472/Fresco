# Отгрука на GIT
- git add .
- git commit -m "update"
- git push origin master (если не работает git push origin main)

# Выход из GitHub
- echo "url=https://github.com" | git credential reject

Для запуска скрипта требуется установить зависимости :

pip install -r requirements.txt

После скомпилируйте скрипт в .exe командой :

pyinstaller --onefile main.py
 сам ехе файл хранится в папке /dist

в файле config.yaml опиманы настройки бота