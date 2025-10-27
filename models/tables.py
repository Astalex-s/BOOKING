#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table Model
Модель стола для системы бронирования ресторана
"""

from typing import Optional
from datetime import datetime


class Table:
    """
    Модель стола в ресторане для системы бронирования
    
    Атрибуты:
        id: Уникальный идентификатор стола
        number: Номер стола (уникальный)
        capacity: Количество мест за столом
        location: Расположение стола (например, 'у окна', 'VIP', 'основной зал')
        table_type: Тип стола (например, 'на 2 персоны', 'семейный')
        is_active: Статус активности стола (можно ли бронировать)
        description: Описание стола
        created_at: Дата создания записи
        updated_at: Дата последнего обновления
    """
    
    # Определение схемы таблицы для базы данных
    TABLE_NAME = 'tables'
    
    COLUMNS = {
        'id': 'SERIAL PRIMARY KEY',
        'number': 'INTEGER UNIQUE NOT NULL',
        'capacity': 'INTEGER NOT NULL',
        'location': 'VARCHAR(100)',
        'table_type': 'VARCHAR(50)',
        'is_active': 'BOOLEAN DEFAULT TRUE',
        'description': 'TEXT',
        'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
        'updated_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
    }
    
    VALID_LOCATIONS = ['у окна', 'VIP', 'основной зал', 'летняя веранда', 'некурящий зал']
    
    def __init__(self,
                 id: Optional[int] = None,
                 number: int = 0,
                 capacity: int = 2,
                 location: Optional[str] = None,
                 table_type: Optional[str] = None,
                 is_active: bool = True,
                 description: Optional[str] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        """Инициализация модели стола"""
        self.id = id
        self.number = number
        self.capacity = capacity
        self.location = location
        self.table_type = table_type
        self.is_active = is_active
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __str__(self) -> str:
        """Строковое представление объекта"""
        return f"Table(id={self.id}, number={self.number}, capacity={self.capacity}, location='{self.location}')"
    
    def __repr__(self) -> str:
        """Представление объекта для отладки"""
        return self.__str__()

