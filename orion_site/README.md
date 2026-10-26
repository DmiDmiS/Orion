# ЖК «Орион» — каталог квартир (Django)

Сайт на Django + HTML/CSS + canvas (диаграммы) с печатью документов и авторизацией жильцов.

## Запуск

```bash
python -m venv venv
venv\Scripts\activate          # Windows;  Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations catalog
python manage.py migrate
python manage.py seed          # демо-данные (необязательно)
python manage.py runserver
```
