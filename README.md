# Портал для статей
Web сервис для написания статьей.
Сервер баз данных MariaDB(MySQL).
Проект имеет простую структуру:
- User - логины пользователей
- Article - статьи пользователей
- Comment - комментарии к статьям

Код для разворачивания базы данных на сервере: 
``` mysql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nickname VARCHAR(255) NOT NULL
);

CREATE TABLE articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    article_id INT,
    user_id INT,
    content TEXT,
    FOREIGN KEY (article_id) REFERENCES articles(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```
Для начала работы нужно воспользоваться утилитой для генерации зашифрованных данных о пользвоателе и сервере базы данных для подключения.
Утилита находиться в папке ___utilites/crypto.py___. Нужно заменить данные в секции на свои

```python
# Данные для шифрования (вставить свои)
host = "You_IP"
user = "You_User_Name"
password = "You_password"
db_name = "You_database_name"
```

Далее полученные данные вставить в модуль по адресу ___secret/secret.py___
```python
# Заменить значение в кавычках на сгенерированное
key = '4bTgLWu6fyhIpzA4='
```

и модуль ___login/login.py___

```python
# Заменить значение в кавычках на сгенерированное
host_encrypt = b'twRTXgMPFcfFQClaL0OiDi-w=='
user_encrypt = b'y7pem8ZldVb_sIsrHsxHG6g=='
password_encrypt = b'qLwAc7r35Y4bD0-h5po45I8O48T1G71LJNOLlDhVkpJiU='
database_encrypt = b'uS5aEsT6M1BkL4u8nRxlT_Hlw7X_bs58w=='
```

После всех процедур можно запустить модуль в корневом каталоге ___run.py___ и пользоваться.