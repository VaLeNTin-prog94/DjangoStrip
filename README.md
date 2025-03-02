# Django + Stripe Checkout

## 📌 Описание проекта

Этот проект представляет собой веб-приложение на Django с интеграцией платежной системы **Stripe Checkout**. Позволяет пользователям просматривать товары, оформлять заказы и оплачивать их через Stripe. Также реализована поддержка **скидок и налогов**.

## 🛠 Функциональность

✔ Просмотр списка товаров ✔ Оформление заказа с несколькими товарами ✔ Поддержка скидок и налогов ✔ Оплата через **Stripe Checkout** ✔ Административная панель Django для управления товарами и заказами ✔ Запуск с помощью Docker

---

## 🚀 Установка и запуск

### 🔹 1. Клонируем репозиторий

```bash
git clone https://github.com/your-username/DjangoStripe.git
cd DjangoStripe
```

### 🔹 2. Создаём и активируем виртуальное окружение (необязательно при использовании Docker)

```bash
python -m venv .venv
source .venv/bin/activate  # для Linux/Mac
.venv\Scripts\activate  # для Windows
```

### 🔹 3. Устанавливаем зависимости

```bash
pip install -r requirements.txt
```

### 🔹 4. Настраиваем переменные окружения

Создайте файл `.env` в корневой папке и добавьте:

```env
SECRET_KEY="your-secret-key"
DEBUG=True
STRIPE_PUBLIC_KEY="your-stripe-public-key"
STRIPE_SECRET_KEY="your-stripe-secret-key"
DATABASE_URL="sqlite:///db.sqlite3"  # Или используйте PostgreSQL
```

### 🔹 5. Применяем миграции и создаем суперпользователя

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 🔹 6. Запускаем сервер

```bash
python manage.py runserver
```

Перейдите в браузер: [**http://127.0.0.1:8000/**](http://127.0.0.1:8000/)

---

## 🐳 Запуск через Docker

Если хотите развернуть проект в **Docker**, используйте:

```bash
docker-compose up --build -d
```

Примените миграции:

```bash
docker-compose exec web python manage.py migrate
```

---

## 🎯 API Эндпоинты

| Метод | URL                           | Описание                            |
| ----- | ----------------------------- | ----------------------------------- |
| `GET` | `/`                           | Главная страница со списком товаров |
| `GET` | `/item/{id}/`                 | Страница товара с кнопкой оплаты    |
| `GET` | `/buy/{id}/`                  | Создание Stripe Checkout сессии     |
| `GET` | `/order/{order_id}/checkout/` | Оплата заказа через Stripe          |
| `GET` | `/success/`                   | Страница успешной оплаты            |
| `GET` | `/cancel/`                    | Страница отмены оплаты              |

---

## 🔑 Stripe Тестовые карты

Для тестирования оплаты введите следующую **тестовую карту Stripe**:

```
4242 4242 4242 4242
```

📌 Дата: любая будущая, CVC: любое 3-значное число

---

## 📜 Лицензия

Этот проект распространяется под **MIT License**.

---

## 👨‍💻 Автор

✍ **Ваше имя**\
GitHub: [your-username](https://github.com/your-username)

