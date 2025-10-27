#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Booking Model
Модель бронирования стола в ресторане
"""

from typing import Optional
from datetime import datetime


class Booking:
    """
    Модель бронирования стола в ресторане
    
    Атрибуты:
        id: Уникальный идентификатор бронирования
        user_id: ID пользователя (внешний ключ на users.id)
        table_id: ID стола (внешний ключ на tables.id)
        booking_date: Дата бронирования
        booking_time: Время бронирования
        guests_count: Количество гостей
        status: Статус бронирования ('pending', 'confirmed', 'cancelled', 'completed')
        contact_phone: Контактный телефон
        contact_name: Имя для контакта
        special_requests: Особые пожелания
        duration: Длительность бронирования в минутах
        created_at: Дата создания бронирования
        updated_at: Дата последнего обновления
    """
    
    # Определение схемы таблицы для базы данных
    TABLE_NAME = 'bookings'
    
    COLUMNS = {
        'id': 'SERIAL PRIMARY KEY',
        'user_id': 'INTEGER REFERENCES users(id) ON DELETE CASCADE',
        'table_id': 'INTEGER REFERENCES tables(id) ON DELETE CASCADE',
        'booking_date': 'DATE NOT NULL',
        'booking_time': 'TIME NOT NULL',
        'guests_count': 'INTEGER NOT NULL',
        'status': 'VARCHAR(20) DEFAULT \'pending\'',
        'contact_phone': 'VARCHAR(20)',
        'contact_name': 'VARCHAR(100)',
        'special_requests': 'TEXT',
        'duration': 'INTEGER DEFAULT 120',
        'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
        'updated_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
    }
    
    VALID_STATUSES = ['pending', 'confirmed', 'cancelled', 'completed']
    
    def __init__(self,
                 id: Optional[int] = None,
                 user_id: int = 0,
                 table_id: int = 0,
                 booking_date: Optional[datetime] = None,
                 booking_time: Optional[datetime] = None,
                 guests_count: int = 1,
                 status: str = 'pending',
                 contact_phone: Optional[str] = None,
                 contact_name: Optional[str] = None,
                 special_requests: Optional[str] = None,
                 duration: int = 120,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        """Инициализация модели бронирования"""
        self.id = id
        self.user_id = user_id
        self.table_id = table_id
        self.booking_date = booking_date
        self.booking_time = booking_time
        self.guests_count = guests_count
        self.status = status
        self.contact_phone = contact_phone
        self.contact_name = contact_name
        self.special_requests = special_requests
        self.duration = duration
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __str__(self) -> str:
        """Строковое представление объекта"""
        return f"Booking(id={self.id}, user_id={self.user_id}, table_id={self.table_id}, status='{self.status}')"
    
    def __repr__(self) -> str:
        """Представление объекта для отладки"""
        return self.__str__()


