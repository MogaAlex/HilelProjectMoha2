# Книжковий магазин (Django Project)

Проєкт онлайн-магазину книг з функціями чату, кошика та інтеграцією платежів Stripe.

## Используемые технологии

### Backend
- Python 3.12
- Django 4.2+
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Gunicorn
- NGINX

### DevOps
- Docker
- Docker Compose
- GitHub Actions (CI/CD)
- Sentry Monitoring

### Безопасность
- JWT Authentication
- Custom User Model
- Permissions & Groups

### Дополнительно
- Swagger / OpenAPI
- i18n (RU / EN)
- Caching
- Logging
- Unit & Integration Tests

## Основні функції
- **Каталог книг**: Відображення товарів за категоріями (MPTT).
- **Кошик**: Додавання, видалення та оновлення кількості товарів.
- **Оформлення замовлень**: Створення замовлень з прив'язкою до профілю користувача.
- **Платежі**: Інтеграція зі Stripe API для безпечної оплати.
- **Чат**: Чат-кімнати для зареєстрованих користувачів.

## Error Handling

### Реалізовано:

- кастомний API exception handling
- логування помилок
- retry механізм
- timeout для міжсервісних запитів
- централізований logging

## Кешування

### Використовується Redis caching.

#### Кешуються:

- популярні книги
- список категорій
- аналітика

## Internationalization (i18n)

### Підтримувані мови:

- Українська
- Російська
- English

## Docker Infrastructure
### Сервіси:
- nginx
- bookstore_api
- warehouse_api
- postgres_bookstore
- postgres_warehouse
- redis
- celery
- celery_beat

## CI/CD

### Використовується GitHub Actions.

#### Pipeline включає:

- linting
- tests
- coverage
- docker build
- deploy

## Production Deployment

### Production stack:

- Gunicorn
- NGINX
- Docker
- PostgreSQL
- Redis

## Monitoring

Використовується Sentry для моніторингу помилок.

## Безпека

### Реалізовано:

- JWT authentication
- permissions
- groups
- CSRF protection
- secure headers
- environment variables

## AI Usage (Використання ШІ)
Цей проєкт був вдосконалений за допомогою AI (ChatGPT/Claude) відповідно до навчального завдання.

### Використані промпти:
- "Проведи code review для Django view (реєстрація та чат), зверни увагу на безпеку та DRY."
- "Оптимізуй PaymentViewSet для роботи зі Stripe, приберіть хардкод ID замовлення."
- "Напиши юніт-тести на pytest для моделей Product та Customer з використанням factories, досягни покриття >60%."
- "Згенеруй професійні docstrings для в'юх магазину та платежів за стандартом Google."

### Виконана робота з AI:
1. **Code Review**: Проаналізовано та виправлено 3 складних компоненти (Chat views, PaymentViewSet, PaymentSerializer). Результати в файлі `AI_REVIEW.md`.
2. **Тестування**: Згенеровано тести для моделей `Product` та `Customer`. Досягнуто необхідний рівень Coverage (понад 60%).
3. **Документація**: Всі views отримали описові docstrings. Створено звіти `AI_REVIEW.md` та `AI_PROMPTS.md`.

### Автор

Мога Олександр 

### Технології:

- Django
- DRF
- Docker
- PostgreSQL
- Redis
- Celery
