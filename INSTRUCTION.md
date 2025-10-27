# 📚 Инструкция по использованию PostgreSQL Driver

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install psycopg2-binary python-dotenv
```

### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
```

### 3. Базовое использование

```python
from postgresql_driver import PostgreSQLDriver

# Использование контекстного менеджера (рекомендуется)
with PostgreSQLDriver() as db:
    # Ваши операции с БД
    users = db.select('users')
    print(f"Найдено пользователей: {len(users)}")
    # Автоматическое подключение и отключение
```

---

## 🔧 Основные методы драйвера

### Управление подключением

#### Контекстный менеджер (рекомендуется)

```python
# Автоматическое подключение и отключение
with PostgreSQLDriver() as db:
    # Ваши операции
    users = db.select('users')
    # Автоматически зафиксируется транзакция и закроется подключение
```

#### Ручное управление

```python
db = PostgreSQLDriver()

# Подключение
success = db.connect()

# Проверка статуса подключения
if db.is_connected():
    print("Подключение активно")

# Отключение
db.disconnect()
```

---

## 📊 CRUD операции

### CREATE (Создание)

#### Создание таблицы

```python
with PostgreSQLDriver() as db:
    # Вариант 1: Передача имени таблицы и колонок
    columns = {
        'id': 'SERIAL PRIMARY KEY',
        'name': 'VARCHAR(100) NOT NULL',
        'email': 'VARCHAR(100) UNIQUE',
        'age': 'INTEGER',
        'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
    }
    db.create_table('users', columns)
    
    # Вариант 2: Использование модели
    db.create_table(User)  # User.TABLE_NAME и User.COLUMNS
```

#### Вставка одной записи

```python
with PostgreSQLDriver() as db:
    user_data = {
        'name': 'Иван Иванов',
        'email': 'ivan@example.com',
        'age': 30
    }
    
    # Обычная вставка
    db.insert('users', user_data)
    
    # Вставка с возвратом ID
    user_id = db.insert('users', user_data, return_id=True)
    print(f"Создан пользователь с ID: {user_id}")
```

#### Массовая вставка

```python
with PostgreSQLDriver() as db:
    users_data = [
        {'name': 'Петр Петров', 'email': 'petr@example.com', 'age': 25},
        {'name': 'Мария Сидорова', 'email': 'maria@example.com', 'age': 28},
        {'name': 'Анна Козлова', 'email': 'anna@example.com', 'age': 32}
    ]
    
    inserted_count = db.insert_many('users', users_data)
    print(f"Вставлено записей: {inserted_count}")
```

---

### READ (Чтение)

#### Выборка всех записей

```python
with PostgreSQLDriver() as db:
    # Все записи
    all_users = db.select('users')
    
    # Только определенные колонки
    users_names = db.select('users', columns=['name', 'email'])
    
    # С условием
    adults = db.select('users', where={'age': 30})
    
    # С сортировкой
    sorted_users = db.select('users', order_by='name ASC')
    
    # С лимитом
    first_10 = db.select('users', limit=10)
    next_10 = db.select('users', limit=10, offset=10)
    
    # Комбинированно
    result = db.select('users', 
                      columns=['name', 'email'],
                      where={'age': {'>': 18}},
                      order_by='name ASC',
                      limit=10)
```

#### Выборка по ID

```python
with PostgreSQLDriver() as db:
    user = db.select_by_id('users', user_id)
    if user:
        print(f"Найден пользователь: {user['name']}")
    else:
        print("Пользователь не найден")
```

#### Подсчет записей

```python
with PostgreSQLDriver() as db:
    # Общее количество
    total_users = db.count('users')
    
    # С условиями
    adults_count = db.count('users', where={'age': 30})
    active_count = db.count('users', where={'is_active': True})
```

#### Проверка существования

```python
with PostgreSQLDriver() as db:
    exists = db.exists('users', {'email': 'ivan@example.com'})
    if exists:
        print("Пользователь с таким email уже существует")
```

---

### UPDATE (Обновление)

#### Обновление по ID

```python
with PostgreSQLDriver() as db:
    updated_count = db.update_by_id('users', user_id, {
        'age': 31,
        'name': 'Иван Обновленный'
    })
    print(f"Обновлено записей: {updated_count}")
```

#### Обновление с условиями

```python
with PostgreSQLDriver() as db:
    updated_count = db.update('users', 
                             {'is_active': False},  # новые значения
                             {'age': 18})           # условия
    print(f"Деактивировано пользователей: {updated_count}")
```

---

### DELETE (Удаление)

#### Удаление по ID

```python
with PostgreSQLDriver() as db:
    deleted_count = db.delete_by_id('users', user_id)
    print(f"Удалено записей: {deleted_count}")
```

#### Удаление с условиями

```python
with PostgreSQLDriver() as db:
    deleted_count = db.delete('users', {'is_active': False})
    print(f"Удалено неактивных пользователей: {deleted_count}")
```

---

## 🗃️ Управление таблицами

#### Проверка существования таблицы

```python
with PostgreSQLDriver() as db:
    if db.table_exists('users'):
        print("Таблица 'users' существует")
```

#### Получение списка таблиц

```python
with PostgreSQLDriver() as db:
    tables = db.get_tables_list()
    print(f"Таблицы в БД: {tables}")
```

#### Информация о структуре таблицы

```python
with PostgreSQLDriver() as db:
    table_info = db.get_table_info('users')
    for column in table_info:
        print(f"Колонка: {column['column_name']}, "
              f"Тип: {column['data_type']}")
```

#### Удаление таблицы

```python
with PostgreSQLDriver() as db:
    success = db.drop_table('users', if_exists=True)
    if success:
        print("Таблица удалена")
```

---

## 🔄 Работа с транзакциями

### Использование контекстного менеджера для транзакций

```python
with PostgreSQLDriver() as db:
    try:
        with db.transaction():
            # Все операции в одной транзакции
            user_id = db.insert('users', user_data, return_id=True)
            db.insert('profiles', {'user_id': user_id, 'bio': 'Описание'})
            db.insert('settings', {'user_id': user_id, 'theme': 'dark'})
            # При успешном выполнении всех операций транзакция зафиксируется
            print("Все операции выполнены успешно")
    except Exception as e:
        # При ошибке произойдет автоматический откат
        print(f"Ошибка в транзакции: {e}")
```

---

## 🔍 Дополнительные методы

### Выполнение произвольного SQL

```python
with PostgreSQLDriver() as db:
    # Простой SELECT
    result = db.execute_raw_sql("SELECT COUNT(*) as total FROM users")
    print(f"Всего пользователей: {result[0]['total']}")
    
    # Сложный запрос с параметрами
    sql = """
    SELECT u.name, p.bio 
    FROM users u 
    LEFT JOIN profiles p ON u.id = p.user_id 
    WHERE u.age > %s
    """
    result = db.execute_raw_sql(sql, (25,))
    
    # Команды изменения данных
    affected_rows = db.execute_raw_sql(
        "UPDATE users SET last_login = NOW() WHERE is_active = %s", 
        (True,)
    )
```

### Выполнение запросов напрямую

```python
with PostgreSQLDriver() as db:
    # SELECT запрос
    users = db.execute_query(
        "SELECT * FROM users WHERE age > %s",
        (30,)
    )
    
    # INSERT/UPDATE/DELETE
    affected_rows = db.execute_command(
        "DELETE FROM users WHERE age < %s",
        (18,)
    )
```

---

## 📝 Практические примеры

### Пример 1: Система пользователей

```python
from postgresql_driver import PostgreSQLDriver

def setup_user_system():
    """Настройка системы пользователей"""
    
    with PostgreSQLDriver() as db:
        # Создание таблицы пользователей
        users_columns = {
            'id': 'SERIAL PRIMARY KEY',
            'username': 'VARCHAR(50) UNIQUE NOT NULL',
            'email': 'VARCHAR(100) UNIQUE NOT NULL',
            'password_hash': 'VARCHAR(255) NOT NULL',
            'is_active': 'BOOLEAN DEFAULT TRUE',
            'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        }
        db.create_table('users', users_columns)
        
        # Создание таблицы профилей
        profiles_columns = {
            'id': 'SERIAL PRIMARY KEY',
            'user_id': 'INTEGER REFERENCES users(id) ON DELETE CASCADE',
            'first_name': 'VARCHAR(50)',
            'last_name': 'VARCHAR(50)',
            'bio': 'TEXT',
            'avatar_url': 'VARCHAR(255)'
        }
        db.create_table('profiles', profiles_columns)
        
        print("Система пользователей настроена")

def create_user(username, email, password_hash, first_name=None, last_name=None):
    """Создание нового пользователя с профилем"""
    
    with PostgreSQLDriver() as db:
        try:
            with db.transaction():
                # Создание пользователя
                user_data = {
                    'username': username,
                    'email': email,
                    'password_hash': password_hash
                }
                user_id = db.insert('users', user_data, return_id=True)
                
                # Создание профиля
                if first_name or last_name:
                    profile_data = {
                        'user_id': user_id,
                        'first_name': first_name,
                        'last_name': last_name
                    }
                    db.insert('profiles', profile_data)
                
                print(f"Пользователь {username} создан с ID: {user_id}")
                return user_id
                
        except Exception as e:
            print(f"Ошибка создания пользователя: {e}")
            return None
```

---

## ⚠️ Обработка ошибок

### Базовый пример

```python
from postgresql_driver import PostgreSQLDriver
import psycopg2

def safe_database_operation():
    """Безопасная операция с базой данных"""
    
    db = PostgreSQLDriver()
    
    try:
        if not db.connect():
            print("Не удалось подключиться к базе данных")
            return False
        
        # Ваши операции с БД
        users = db.select('users')
        print(f"Найдено пользователей: {len(users)}")
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"Ошибка подключения к БД: {e}")
        return False
        
    except psycopg2.IntegrityError as e:
        print(f"Ошибка целостности данных: {e}")
        return False
        
    except psycopg2.Error as e:
        print(f"Ошибка PostgreSQL: {e}")
        return False
        
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return False
        
    finally:
        db.disconnect()

# Использование
success = safe_database_operation()
if success:
    print("Операция выполнена успешно")
```

### Рекомендуемый способ с контекстным менеджером

```python
from postgresql_driver import PostgreSQLDriver
import psycopg2

def safe_database_operation():
    """Безопасная операция с использованием контекстного менеджера"""
    
    try:
        with PostgreSQLDriver() as db:
            users = db.select('users')
            print(f"Найдено пользователей: {len(users)}")
            return True
            
    except psycopg2.OperationalError as e:
        print(f"Ошибка подключения к БД: {e}")
        return False
        
    except psycopg2.IntegrityError as e:
        print(f"Ошибка целостности данных: {e}")
        return False
        
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return False

# Использование
success = safe_database_operation()
```

---

## 🔧 Настройка логирования

```python
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database.log'),
        logging.StreamHandler()
    ]
)

# Использование с логированием
with PostgreSQLDriver() as db:
    db.logger.setLevel(logging.DEBUG)  # Для более подробного логирования
    users = db.select('users')
```

---

## 📋 Полный список методов

### Управление подключением
- `__init__(config)` - инициализация драйвера
- `connect()` - подключение к БД
- `disconnect()` - отключение от БД
- `is_connected()` - проверка статуса подключения
- `__enter__()` - вход в контекстный менеджер
- `__exit__(exc_type, exc_val, exc_tb)` - выход из контекстного менеджера

### Управление таблицами
- `create_table(table_name_or_model, columns, constraints)` - создание таблицы
- `drop_table(table_name, if_exists)` - удаление таблицы
- `table_exists(table_name)` - проверка существования таблицы
- `get_tables_list()` - список всех таблиц
- `get_table_info(table_name)` - информация о структуре таблицы

### CRUD операции
- `insert(table_name, data, return_id)` - вставка одной записи
- `insert_many(table_name, data_list)` - массовая вставка
- `select(table_name, columns, where, order_by, limit, offset)` - выборка
- `select_by_id(table_name, record_id)` - выборка по ID
- `update(table_name, data, where)` - обновление с условиями
- `update_by_id(table_name, record_id, data)` - обновление по ID
- `delete(table_name, where)` - удаление с условиями
- `delete_by_id(table_name, record_id)` - удаление по ID
- `count(table_name, where)` - подсчет записей
- `exists(table_name, where)` - проверка существования

### Транзакции
- `transaction()` - контекстный менеджер для транзакций

### SQL запросы
- `execute_query(query, params)` - выполнение SELECT запросов
- `execute_command(command, params)` - выполнение команд (INSERT/UPDATE/DELETE)
- `execute_raw_sql(sql, params)` - выполнение произвольного SQL

---

## 🎯 Лучшие практики

1. **Всегда используйте контекстный менеджер** (`with PostgreSQLDriver() as db`)
2. **Обрабатывайте исключения** для всех операций с БД
3. **Используйте транзакции** для связанных операций
4. **Проверяйте существование** записей перед операциями
5. **Используйте параметризованные запросы** для безопасности
6. **Настройте логирование** для отладки
7. **Тестируйте подключение** перед выполнением операций

---

## 📝 Чек-лист для использования

- [ ] Установлены зависимости: `psycopg2-binary`, `python-dotenv`
- [ ] Создан файл `.env` с параметрами подключения
- [ ] Проверено подключение к базе данных
- [ ] Настроено логирование (опционально)
- [ ] Реализована обработка ошибок
- [ ] Используются транзакции для критических операций
- [ ] Ресурсы корректно освобождаются через контекстный менеджер

---

**Готово!** Теперь вы знаете, как эффективно использовать PostgreSQL Driver в своих проектах. 🚀
