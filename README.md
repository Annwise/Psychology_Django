# Проект

Веб-приложение на Django с классическим MVC-подходом: Сайт частного психолога.

---

## Установка и запуск

1. ### Клонирование репозитория:
   ```bash
   git clone <ссылка_на_репозиторий>
   cd psy

2. ### Установка зависимостей:
    ```bash
   pip install -r requirements.txt

3. ### Выполнить миграции:
    ```bash
   python manage.py migrate

4. ### Запустить сервер:
    ```bash
    python manage.py runserver

## Примеры запросов

### Запись на консультацию

Отправка данных через AJAX на `/booking/`.
Метод: POST  
URL: `/booking/`  
Тип данных: JSON  

**Пример тела запроса:**

{
  "name": "Анна",
  "phone": "+79991234567",
  "email": "anna@example.com"
}

**Пример ответа:**

{
  "success": true
}

**Ошибки:** 

- {"success": false, "error": "Пожалуйста, заполните все поля корректно"}
- {"success": false, "error": "Документы политики и согласия не найдены"}

## Скриншоты интерфейса

![Главная страница](https://raw.githubusercontent.com/Annwise/Psychology_Django/main/screnshots/home.png)
![Форма записи](https://raw.githubusercontent.com/Annwise/Psychology_Django/main/screnshots/form.png)
![Регистрация](https://raw.githubusercontent.com/Annwise/Psychology_Django/main/screnshots/register.png)
![Страница входа](https://raw.githubusercontent.com/Annwise/Psychology_Django/main/screnshots/login.png)
![Услуги](https://raw.githubusercontent.com/Annwise/Psychology_Django/main/screnshots/service.png)
![Админ-панель](https://raw.githubusercontent.com/Annwise/Psychology_Django/main/screnshots/admin.png)

## Обработка ошибок

- **Кастомные страницы 404/500** — если страница не найдена или произошла внутренняя ошибка.
- **Валидация форм** — проверка правильности ввода данных (имя, email, телефон).

## Тесты

**Проект содержит 5 unit-тестов, проверяющих:**
- Доступность главной страницы.
- Доступность страниц регистрации и входа.
- Защиту личного кабинета.
- Обработку ошибок в форме записи.