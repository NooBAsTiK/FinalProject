from cryptography.fernet import Fernet
from colorama import Fore, Style

# Генерация ключа
key = Fernet.generate_key()
print(f"Ваш ключ шифрования: {Fore.GREEN}{key.decode()}{Style.RESET_ALL}")

# Создание объекта Fernet
cipher = Fernet(key)

# Данные для шифрования (вставить свои)
host = "You_IP"
user = "You_User_Name"
password = "You_password"
db_name = "You_database_name"

# Шифрование данных
encrypted_host = cipher.encrypt(host.encode())
encrypted_user = cipher.encrypt(user.encode())
encrypted_password = cipher.encrypt(password.encode())
encrypted_db_name = cipher.encrypt(db_name.encode())

print(f'Зашифрованные данные подключения')
print(f"Имя хоста: {Fore.CYAN}{encrypted_host.decode()}{Style.RESET_ALL}")
print(f"Имя пользователя: {Fore.CYAN}{encrypted_user.decode()}{Style.RESET_ALL}")
print(f"Пароль: {Fore.CYAN}{encrypted_password.decode()}{Style.RESET_ALL}")
print(f"Имя базы данных: {Fore.CYAN}{encrypted_db_name.decode()}{Style.RESET_ALL}")