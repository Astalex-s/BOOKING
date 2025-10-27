#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PostgreSQL Driver Module
Модуль-драйвер для работы с PostgreSQL базой данных
Можно использовать во внешних проектах
"""

import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor, execute_values
import os
import logging
from typing import Optional, Dict, Any, List, Tuple, Union
from contextlib import contextmanager
from dotenv import load_dotenv


class PostgreSQLDriver:
    """
    Драйвер для работы с PostgreSQL базой данных
    Поддерживает CRUD операции, транзакции и управление подключениями
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Инициализация драйвера
        
        Args:
            config: Словарь с параметрами подключения. Если не указан, 
                   загружаются из переменных окружения
        """
        # Настройка логирования
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            # Настройка кодировки для Windows
            import sys
            if sys.platform == "win32":
                handler.stream.reconfigure(encoding='utf-8')
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        
        # Загрузка конфигурации
        if config is None:
            load_dotenv()
            config = {
                'host': os.getenv('DB_HOST', 'localhost'),
                'port': int(os.getenv('DB_PORT', '5432')),
                'database': os.getenv('DB_NAME', 'postgres'),
                'user': os.getenv('DB_USER', 'postgres'),
                'password': os.getenv('DB_PASSWORD', 'password')
            }
        
        self.connection_params = config
        self.connection: Optional[psycopg2.extensions.connection] = None
        self.cursor: Optional[psycopg2.extensions.cursor] = None
        self._in_transaction = False
        
        self.logger.info(f"PostgreSQL Driver инициализирован для {config['host']}:{config['port']}")
    
    def connect(self) -> bool:
        """
        Подключение к базе данных
        
        Returns:
            bool: True если подключение успешно, False в противном случае
        """
        try:
            self.logger.info("Подключение к PostgreSQL...")
            self.connection = psycopg2.connect(**self.connection_params)
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            self.logger.info("[OK] Подключение к PostgreSQL успешно!")
            return True
            
        except psycopg2.OperationalError as e:
            self.logger.error(f"[ERROR] Ошибка подключения к базе данных: {e}")
            return False
        except Exception as e:
            self.logger.error(f"[ERROR] Неожиданная ошибка при подключении: {e}")
            return False
    
    def disconnect(self):
        """Отключение от базы данных"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            self.logger.info("[INFO] Подключение к базе данных закрыто")
        except Exception as e:
            self.logger.error(f"[WARNING] Ошибка при закрытии подключения: {e}")
    
    def is_connected(self) -> bool:
        """Проверка статуса подключения"""
        return self.connection is not None and not self.connection.closed
    
    @contextmanager
    def transaction(self):
        """Контекстный менеджер для транзакций"""
        if not self.is_connected():
            raise Exception("Нет активного подключения к базе данных")
        
        try:
            self.logger.debug("Начало транзакции")
            self._in_transaction = True
            yield self
            self.connection.commit()
            self.logger.debug("Транзакция зафиксирована")
        except Exception as e:
            self.connection.rollback()
            self.logger.error(f"Транзакция отменена: {e}")
            raise
        finally:
            self._in_transaction = False
    
    def execute_query(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """
        Выполнение SELECT запроса
        
        Args:
            query: SQL запрос
            params: Параметры для запроса
            
        Returns:
            List[Dict[str, Any]]: Результат запроса
        """
        if not self.is_connected():
            raise Exception("Нет активного подключения к базе данных")
        
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            self.logger.error(f"Ошибка выполнения запроса: {e}")
            raise
    
    def execute_command(self, command: str, params: Optional[Tuple] = None) -> int:
        """
        Выполнение команды (INSERT, UPDATE, DELETE)
        
        Args:
            command: SQL команда
            params: Параметры для команды
            
        Returns:
            int: Количество затронутых строк
        """
        if not self.is_connected():
            raise Exception("Нет активного подключения к базе данных")
        
        try:
            self.cursor.execute(command, params)
            return self.cursor.rowcount
        except psycopg2.Error as e:
            self.logger.error(f"Ошибка выполнения команды: {e}")
            raise
    
    # ==================== CRUD ОПЕРАЦИИ ====================
    
    def create_table(self, table_name_or_model, columns: Dict[str, str] = None, 
                    constraints: Optional[List[str]] = None) -> bool:
        """
        Создание таблицы
        
        Args:
            table_name_or_model: Имя таблицы (str) или модель (объект с атрибутами TABLE_NAME и COLUMNS)
            columns: Словарь {имя_колонки: тип_данных} (используется если передан table_name как строка)
            constraints: Список дополнительных ограничений
            
        Returns:
            bool: True если таблица создана успешно
        """
        try:
            # Проверяем, передана ли модель
            if hasattr(table_name_or_model, 'TABLE_NAME') and hasattr(table_name_or_model, 'COLUMNS'):
                # Передан объект модели
                table_name = table_name_or_model.TABLE_NAME
                columns = table_name_or_model.COLUMNS
                self.logger.info(f"Создание таблицы '{table_name}' из модели")
            else:
                # Передан обычный путь (имя таблицы как строка)
                table_name = table_name_or_model
                if columns is None:
                    self.logger.error("Необходимо указать columns или передать модель")
                    return False
            
            columns_sql = []
            for col_name, col_type in columns.items():
                columns_sql.append(f"{col_name} {col_type}")
            
            if constraints:
                columns_sql.extend(constraints)
            
            query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {', '.join(columns_sql)}
            );
            """
            
            self.execute_command(query)
            # Коммитим создание таблицы
            if self.connection and not self._in_transaction:
                self.connection.commit()
            self.logger.info(f"Таблица '{table_name}' создана успешно")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка создания таблицы: {e}")
            return False
    
    def insert(self, table_name: str, data: Dict[str, Any], 
              return_id: bool = False) -> Optional[int]:
        """
        Вставка записи в таблицу
        
        Args:
            table_name: Имя таблицы
            data: Словарь с данными для вставки
            return_id: Возвращать ли ID вставленной записи
            
        Returns:
            Optional[int]: ID вставленной записи (если return_id=True)
        """
        try:
            columns = list(data.keys())
            values = list(data.values())
            placeholders = ['%s'] * len(values)
            
            query = f"""
            INSERT INTO {table_name} ({', '.join(columns)})
            VALUES ({', '.join(placeholders)})
            """
            
            if return_id:
                query += " RETURNING id"
                self.cursor.execute(query, values)
                result = self.cursor.fetchone()
                return result['id'] if result else None
            else:
                self.execute_command(query, tuple(values))
                return None
                
        except Exception as e:
            self.logger.error(f"Ошибка вставки в таблицу '{table_name}': {e}")
            raise
    
    def insert_many(self, table_name: str, data_list: List[Dict[str, Any]]) -> int:
        """
        Массовая вставка записей
        
        Args:
            table_name: Имя таблицы
            data_list: Список словарей с данными
            
        Returns:
            int: Количество вставленных записей
        """
        try:
            if not data_list:
                return 0
            
            columns = list(data_list[0].keys())
            values = [tuple(record[col] for col in columns) for record in data_list]
            
            query = f"""
            INSERT INTO {table_name} ({', '.join(columns)})
            VALUES %s
            """
            
            execute_values(self.cursor, query, values)
            return len(values)
            
        except Exception as e:
            self.logger.error(f"Ошибка массовой вставки в таблицу '{table_name}': {e}")
            raise
    
    def select(self, table_name: str, columns: Optional[List[str]] = None,
              where: Optional[Dict[str, Any]] = None, 
              order_by: Optional[str] = None,
              limit: Optional[int] = None,
              offset: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Выборка записей из таблицы
        
        Args:
            table_name: Имя таблицы
            columns: Список колонок для выборки (None = все колонки)
            where: Условия WHERE в виде словаря
            order_by: Сортировка
            limit: Ограничение количества записей
            offset: Смещение
            
        Returns:
            List[Dict[str, Any]]: Результат выборки
        """
        try:
            # Формирование SELECT части
            if columns:
                select_part = ', '.join(columns)
            else:
                select_part = '*'
            
            query = f"SELECT {select_part} FROM {table_name}"
            params = []
            
            # Добавление WHERE условий
            if where:
                where_conditions = []
                for col, val in where.items():
                    where_conditions.append(f"{col} = %s")
                    params.append(val)
                query += f" WHERE {' AND '.join(where_conditions)}"
            
            # Добавление сортировки
            if order_by:
                query += f" ORDER BY {order_by}"
            
            # Добавление LIMIT и OFFSET
            if limit:
                query += f" LIMIT {limit}"
            if offset:
                query += f" OFFSET {offset}"
            
            return self.execute_query(query, tuple(params) if params else None)
            
        except Exception as e:
            self.logger.error(f"Ошибка выборки из таблицы '{table_name}': {e}")
            raise
    
    def select_by_id(self, table_name: str, record_id: int) -> Optional[Dict[str, Any]]:
        """
        Выборка записи по ID
        
        Args:
            table_name: Имя таблицы
            record_id: ID записи
            
        Returns:
            Optional[Dict[str, Any]]: Найденная запись или None
        """
        try:
            query = f"SELECT * FROM {table_name} WHERE id = %s"
            result = self.execute_query(query, (record_id,))
            return result[0] if result else None
            
        except Exception as e:
            self.logger.error(f"Ошибка выборки записи по ID из таблицы '{table_name}': {e}")
            raise
    
    def update(self, table_name: str, data: Dict[str, Any], 
              where: Dict[str, Any]) -> int:
        """
        Обновление записей в таблице
        
        Args:
            table_name: Имя таблицы
            data: Словарь с данными для обновления
            where: Условия WHERE
            
        Returns:
            int: Количество обновленных записей
        """
        try:
            set_clauses = []
            params = []
            
            for col, val in data.items():
                set_clauses.append(f"{col} = %s")
                params.append(val)
            
            where_clauses = []
            for col, val in where.items():
                where_clauses.append(f"{col} = %s")
                params.append(val)
            
            query = f"""
            UPDATE {table_name} 
            SET {', '.join(set_clauses)}
            WHERE {' AND '.join(where_clauses)}
            """
            
            return self.execute_command(query, tuple(params))
            
        except Exception as e:
            self.logger.error(f"Ошибка обновления в таблице '{table_name}': {e}")
            raise
    
    def update_by_id(self, table_name: str, record_id: int, 
                    data: Dict[str, Any]) -> int:
        """
        Обновление записи по ID
        
        Args:
            table_name: Имя таблицы
            record_id: ID записи
            data: Словарь с данными для обновления
            
        Returns:
            int: Количество обновленных записей
        """
        return self.update(table_name, data, {'id': record_id})
    
    def delete(self, table_name: str, where: Dict[str, Any]) -> int:
        """
        Удаление записей из таблицы
        
        Args:
            table_name: Имя таблицы
            where: Условия WHERE
            
        Returns:
            int: Количество удаленных записей
        """
        try:
            where_clauses = []
            params = []
            
            for col, val in where.items():
                where_clauses.append(f"{col} = %s")
                params.append(val)
            
            query = f"DELETE FROM {table_name} WHERE {' AND '.join(where_clauses)}"
            
            return self.execute_command(query, tuple(params))
            
        except Exception as e:
            self.logger.error(f"Ошибка удаления из таблицы '{table_name}': {e}")
            raise
    
    def delete_by_id(self, table_name: str, record_id: int) -> int:
        """
        Удаление записи по ID
        
        Args:
            table_name: Имя таблицы
            record_id: ID записи
            
        Returns:
            int: Количество удаленных записей
        """
        return self.delete(table_name, {'id': record_id})
    
    def count(self, table_name: str, where: Optional[Dict[str, Any]] = None) -> int:
        """
        Подсчет количества записей в таблице
        
        Args:
            table_name: Имя таблицы
            where: Условия WHERE
            
        Returns:
            int: Количество записей
        """
        try:
            query = f"SELECT COUNT(*) FROM {table_name}"
            params = []
            
            if where:
                where_clauses = []
                for col, val in where.items():
                    where_clauses.append(f"{col} = %s")
                    params.append(val)
                query += f" WHERE {' AND '.join(where_clauses)}"
            
            result = self.execute_query(query, tuple(params) if params else None)
            return result[0]['count']
            
        except Exception as e:
            self.logger.error(f"Ошибка подсчета записей в таблице '{table_name}': {e}")
            raise
    
    def exists(self, table_name: str, where: Dict[str, Any]) -> bool:
        """
        Проверка существования записи
        
        Args:
            table_name: Имя таблицы
            where: Условия WHERE
            
        Returns:
            bool: True если запись существует
        """
        return self.count(table_name, where) > 0
    
    def drop_table(self, table_name: str, if_exists: bool = True) -> bool:
        """
        Удаление таблицы
        
        Args:
            table_name: Имя таблицы
            if_exists: Удалять только если таблица существует
            
        Returns:
            bool: True если таблица удалена успешно
        """
        try:
            if_exists_clause = "IF EXISTS" if if_exists else ""
            query = f"DROP TABLE {if_exists_clause} {table_name}"
            
            self.execute_command(query)
            self.logger.info(f"Таблица '{table_name}' удалена успешно")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка удаления таблицы '{table_name}': {e}")
            return False
    
    # ==================== ДОПОЛНИТЕЛЬНЫЕ МЕТОДЫ ====================
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Получение информации о структуре таблицы
        
        Args:
            table_name: Имя таблицы
            
        Returns:
            List[Dict[str, Any]]: Информация о колонках таблицы
        """
        try:
            query = """
            SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default,
                character_maximum_length
            FROM information_schema.columns 
            WHERE table_name = %s
            ORDER BY ordinal_position
            """
            
            return self.execute_query(query, (table_name,))
            
        except Exception as e:
            self.logger.error(f"Ошибка получения информации о таблице '{table_name}': {e}")
            raise
    
    def get_tables_list(self) -> List[str]:
        """
        Получение списка всех таблиц в базе данных
        
        Returns:
            List[str]: Список имен таблиц
        """
        try:
            query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
            """
            
            result = self.execute_query(query)
            return [row['table_name'] for row in result]
            
        except Exception as e:
            self.logger.error(f"Ошибка получения списка таблиц: {e}")
            raise
    
    def table_exists(self, table_name: str) -> bool:
        """
        Проверка существования таблицы
        
        Args:
            table_name: Имя таблицы
            
        Returns:
            bool: True если таблица существует
        """
        try:
            query = """
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            )
            """
            
            result = self.execute_query(query, (table_name,))
            return result[0]['exists'] if result else False
            
        except Exception as e:
            self.logger.error(f"Ошибка проверки существования таблицы '{table_name}': {e}")
            return False
    
    def execute_raw_sql(self, sql: str, params: Optional[Tuple] = None) -> Any:
        """
        Выполнение произвольного SQL запроса
        
        Args:
            sql: SQL запрос
            params: Параметры для запроса
            
        Returns:
            Any: Результат выполнения запроса
        """
        try:
            self.cursor.execute(sql, params)
            
            # Если это SELECT запрос, возвращаем результат
            if sql.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                return self.cursor.rowcount
                
        except Exception as e:
            self.logger.error(f"Ошибка выполнения SQL запроса: {e}")
            raise
    
    def __enter__(self):
        """Поддержка контекстного менеджера"""
        if not self.connect():
            raise Exception("Не удалось подключиться к базе данных")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Поддержка контекстного менеджера"""
        # Коммитим изменения перед закрытием
        if self.connection and not self._in_transaction:
            try:
                self.connection.commit()
            except Exception as e:
                self.logger.error(f"Ошибка при коммите: {e}")
        self.disconnect()


# ==================== ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ====================

def example_usage():
    """Пример использования PostgreSQLDriver"""
    
    # Инициализация драйвера
    db = PostgreSQLDriver()
    
    try:
        # Подключение
        if not db.connect():
            print("Не удалось подключиться к базе данных")
            return
        
        # Создание таблицы
        columns = {
            'id': 'SERIAL PRIMARY KEY',
            'name': 'VARCHAR(100) NOT NULL',
            'email': 'VARCHAR(100) UNIQUE',
            'age': 'INTEGER',
            'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        }
        db.create_table('users', columns)
        
        # Вставка данных
        user_data = {
            'name': 'Иван Иванов',
            'email': 'ivan@example.com',
            'age': 30
        }
        user_id = db.insert('users', user_data, return_id=True)
        print(f"Создан пользователь с ID: {user_id}")
        
        # Массовая вставка
        users_data = [
            {'name': 'Петр Петров', 'email': 'petr@example.com', 'age': 25},
            {'name': 'Мария Сидорова', 'email': 'maria@example.com', 'age': 28}
        ]
        db.insert_many('users', users_data)
        
        # Выборка данных
        users = db.select('users', where={'age': 30})
        print(f"Найдено пользователей с возрастом 30: {len(users)}")
        
        # Обновление данных
        updated_count = db.update_by_id('users', user_id, {'age': 31})
        print(f"Обновлено записей: {updated_count}")
        
        # Подсчет записей
        total_users = db.count('users')
        print(f"Всего пользователей: {total_users}")
        
        # Получение информации о таблице
        table_info = db.get_table_info('users')
        print(f"Колонки в таблице users: {[col['column_name'] for col in table_info]}")
        
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        db.disconnect()


if __name__ == "__main__":
    example_usage()
