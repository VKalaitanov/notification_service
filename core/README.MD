# Инструкция по запуску проекта

### - скачиваем проект Git командой:
```bash 
git clone https://github.com/VKalaitanov/notification_service.git
```
### - добавляем в файл .env данные для сервисов

### - прописываем команды в терминале:
```bash 
cd notification_service
docker compose up --build -d
docker compose exec web sh -c "python manage.py makemigrations && python manage.py migrate"
```

### - переходим по адресу:
```bash 
http://127.0.0.1:8000
```
