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

Откройте http://127.0.0.1:8000/

Демо-аккаунты после `seed` (смените пароли перед публикацией):

| Роль | Логин | Пароль |
|------|-------|--------|
| Сотрудник (видит заявки, договоры, отчёты) | manager | manager123 |
| Жилец | resident | resident123 |

Админка: http://127.0.0.1:8000/admin/ (создайте администратора: `python manage.py createsuperuser`).
Сотрудником становится любой пользователь с галочкой «Статус персонала» в админке.

## Страницы (соответствуют скриншотам)

| Адрес | Страница |
|-------|----------|
| `/catalog/` | Каталог с поиском и фильтром (количество комнат, площадь); пустой результат — «ничего не найдено» |
| `/apartment/<id>/book/` | Форма бронирования |
| `/` | Главная: описание, галерея, соцсети; меню слева |
| `/requests/` | Заявки (сотрудник) со ссылкой «Составить договор» |
| `/contract/new/<id>/` | Форма договора |
| `/reports/` | Диаграммы на canvas с кнопками «Сохранить» (PNG) |
| `/contracts/` | Контракты и печать (одного договора или списка) |
| `/login/`, `/register/`, `/favorites/` | Вход, регистрация жильцов, избранное |
- Ссылки на Telegram и ВК: `templates/home.html`.
- Тексты на главной и в «Управляющей компании»: `templates/home.html`, `templates/management.html`.
