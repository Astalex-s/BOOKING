#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
User Model
Модель пользователя для системы бронирования
"""

from typing import Optional
from datetime import datetime


class User:
    """
    Модель пользователя системы бронирования
    
    Атрибуты:
        id: Уникальный идентификатор пользователя
        username: Имя пользователя (уникальное)
        email: Email пользователя (уникальный)
        password_hash: Хеш пароля
        first_name: Имя
        last_name: Фамилия
        phone: Номер телефона
        role: Роль пользователя ('user' или 'admin')
        is_active: Статус активности аккаунта
        created_at: Дата создания аккаунта
        updated_at: Дата последнего обновления
    """
    
    # Определение схемы таблицы для базы данных
    TABLE_NAME = 'users'
    
    COLUMNS = {
        'id': 'SERIAL PRIMARY KEY',
        'username': 'VARCHAR(50) UNIQUE NOT NULL',
        'email': 'VARCHAR(100) UNIQUE NOT NULL',
        'password_hash': 'VARCHAR(255) NOT NULL',
        'first_name': 'VARCHAR(50)',
        'last_name': 'VARCHAR(50)',
        'phone': 'VARCHAR(20)',
        'role': 'VARCHAR(20) DEFAULT \'user\'',
        'is_active': 'BOOLEAN DEFAULT TRUE',
        'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
        'updated_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
    }
    
    VALID_ROLES = ['user', 'admin']
    
    def __init__(self, 
                 id: Optional[int] = None,
                 username: str = '',
                 email: str = '',
                 password_hash: str = '',
                 first_name: Optional[str] = None,
                 last_name: Optional[str] = None,
                 phone: Optional[str] = None,
                 role: str = 'user',
                 is_active: bool = True,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        """Инициализация модели пользователя"""
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.role = role
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __str__(self) -> str:
        """Строковое представление объекта"""
        return f"User(id={self.id}, username='{self.username}', email='{self.email}', role='{self.role}')"
    
    def __repr__(self) -> str:
        """Представление объекта для отладки"""
        return self.__str__()
