from models.booking import Booking
from models.tables import Table
from models.user import User
from postgresql_driver import PostgreSQLDriver
from typing import Optional, List, Dict, Any
from datetime import datetime, date, time


# ==================== ФУНКЦИЯ СОЗДАНИЯ ТАБЛИЦ ====================

def create_tables():
    """Создание всех таблиц в базе данных"""
    try:
        with PostgreSQLDriver() as db:
            print("Создание таблицы users...")
            db.create_table(User)
            
            print("Создание таблицы tables...")
            db.create_table(Table)
            
            print("Создание таблицы bookings...")
            db.create_table(Booking)

            print("\n✓ Все таблицы успешно созданы!")
        return True
        
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
        return False


# ==================== CRUD ДЛЯ ПОЛЬЗОВАТЕЛЕЙ (USERS) ====================

def create_user(username: str, email: str, password_hash: str, 
                first_name: Optional[str] = None, last_name: Optional[str] = None,
                phone: Optional[str] = None, role: str = 'user') -> Optional[int]:
    """Создание нового пользователя"""
    try:
        with PostgreSQLDriver() as db:
            user_data = {
                'username': username,
                'email': email,
                'password_hash': password_hash,
                'first_name': first_name,
                'last_name': last_name,
                'phone': phone,
                'role': role
            }
            
            user_id = db.insert(User.TABLE_NAME, user_data, return_id=True)
            return user_id
            
    except Exception as e:
        print(f"Ошибка создания пользователя: {e}")
        return None


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Получение пользователя по ID"""
    try:
        with PostgreSQLDriver() as db:
            return db.select_by_id(User.TABLE_NAME, user_id)
    except Exception as e:
        print(f"Ошибка получения пользователя: {e}")
        return None


def get_all_users(is_active: Optional[bool] = None) -> List[Dict[str, Any]]:
    """Получение всех пользователей"""
    try:
        with PostgreSQLDriver() as db:
            if is_active is not None:
                return db.select(User.TABLE_NAME, where={'is_active': is_active})
            return db.select(User.TABLE_NAME)
    except Exception as e:
        print(f"Ошибка получения пользователей: {e}")
        return []


def update_user(user_id: int, **kwargs) -> bool:
    """Обновление пользователя"""
    try:
        with PostgreSQLDriver() as db:
            affected = db.update_by_id(User.TABLE_NAME, user_id, kwargs)
            return affected > 0
    except Exception as e:
        print(f"Ошибка обновления пользователя: {e}")
        return False


def delete_user(user_id: int) -> bool:
    """Удаление пользователя"""
    try:
        with PostgreSQLDriver() as db:
            affected = db.delete_by_id(User.TABLE_NAME, user_id)
            return affected > 0
    except Exception as e:
        print(f"Ошибка удаления пользователя: {e}")
        return False


# ==================== CRUD ДЛЯ СТОЛОВ (TABLES) ====================

def create_table_record(number: int, capacity: int, 
                       location: Optional[str] = None, 
                       table_type: Optional[str] = None,
                       is_active: bool = True,
                       description: Optional[str] = None) -> Optional[int]:
    """Создание нового стола"""
    try:
        with PostgreSQLDriver() as db:
            table_data = {
                'number': number,
                'capacity': capacity,
                'location': location,
                'table_type': table_type,
                'is_active': is_active,
                'description': description
            }
            
            table_id = db.insert(Table.TABLE_NAME, table_data, return_id=True)
            return table_id
    except Exception as e:
        print(f"Ошибка создания стола: {e}")
        return None


def get_table_by_id(table_id: int) -> Optional[Dict[str, Any]]:
    """Получение стола по ID"""
    try:
        with PostgreSQLDriver() as db:
            return db.select_by_id(Table.TABLE_NAME, table_id)
    except Exception as e:
        print(f"Ошибка получения стола: {e}")
        return None


def get_all_tables(is_active: Optional[bool] = None) -> List[Dict[str, Any]]:
    """Получение всех столов"""
    try:
        with PostgreSQLDriver() as db:
            if is_active is not None:
                return db.select(Table.TABLE_NAME, where={'is_active': is_active})
            return db.select(Table.TABLE_NAME)
    except Exception as e:
        print(f"Ошибка получения столов: {e}")
        return []


def update_table(table_id: int, **kwargs) -> bool:
    """Обновление стола"""
    try:
        with PostgreSQLDriver() as db:
            affected = db.update_by_id(Table.TABLE_NAME, table_id, kwargs)
            return affected > 0
    except Exception as e:
        print(f"Ошибка обновления стола: {e}")
        return False


def delete_table(table_id: int) -> bool:
    """Удаление стола"""
    try:
        with PostgreSQLDriver() as db:
            affected = db.delete_by_id(Table.TABLE_NAME, table_id)
            return affected > 0
    except Exception as e:
        print(f"Ошибка удаления стола: {e}")
        return False


# ==================== CRUD ДЛЯ БРОНИРОВАНИЙ (BOOKINGS) ====================

def create_booking(user_id: int, table_id: int, booking_date: date, 
                  booking_time: time, guests_count: int,
                  status: str = 'pending',
                  contact_phone: Optional[str] = None,
                  contact_name: Optional[str] = None,
                  special_requests: Optional[str] = None,
                  duration: int = 120) -> Optional[int]:
    """Создание нового бронирования"""
    try:
        with PostgreSQLDriver() as db:
            booking_data = {
                'user_id': user_id,
                'table_id': table_id,
                'booking_date': booking_date,
                'booking_time': booking_time,
                'guests_count': guests_count,
                'status': status,
                'contact_phone': contact_phone,
                'contact_name': contact_name,
                'special_requests': special_requests,
                'duration': duration
            }
            
            booking_id = db.insert(Booking.TABLE_NAME, booking_data, return_id=True)
            return booking_id
    except Exception as e:
        print(f"Ошибка создания бронирования: {e}")
        return None


def get_booking_by_id(booking_id: int) -> Optional[Dict[str, Any]]:
    """Получение бронирования по ID"""
    try:
        with PostgreSQLDriver() as db:
            return db.select_by_id(Booking.TABLE_NAME, booking_id)
    except Exception as e:
        print(f"Ошибка получения бронирования: {e}")
        return None


def get_all_bookings(user_id: Optional[int] = None, 
                    table_id: Optional[int] = None,
                    status: Optional[str] = None,
                    booking_date: Optional[date] = None) -> List[Dict[str, Any]]:
    """Получение всех бронирований с фильтрацией"""
    try:
        with PostgreSQLDriver() as db:
            where_clause = {}
            if user_id is not None:
                where_clause['user_id'] = user_id
            if table_id is not None:
                where_clause['table_id'] = table_id
            if status is not None:
                where_clause['status'] = status
            if booking_date is not None:
                where_clause['booking_date'] = booking_date
            
            return db.select(Booking.TABLE_NAME, where=where_clause if where_clause else None,
                            order_by='booking_date DESC, booking_time DESC')
    except Exception as e:
        print(f"Ошибка получения бронирований: {e}")
        return []


def update_booking(booking_id: int, **kwargs) -> bool:
    """Обновление бронирования"""
    try:
        with PostgreSQLDriver() as db:
            affected = db.update_by_id(Booking.TABLE_NAME, booking_id, kwargs)
            return affected > 0
    except Exception as e:
        print(f"Ошибка обновления бронирования: {e}")
        return False


def delete_booking(booking_id: int) -> bool:
    """Удаление бронирования"""
    try:
        with PostgreSQLDriver() as db:
            affected = db.delete_by_id(Booking.TABLE_NAME, booking_id)
            return affected > 0
    except Exception as e:
        print(f"Ошибка удаления бронирования: {e}")
        return False


def is_table_available(table_id: int, booking_date: date, booking_time: time, 
                      duration: int = 120, exclude_booking_id: Optional[int] = None) -> bool:
    """
    Проверка доступности стола на указанное время
    
    Args:
        table_id: ID стола
        booking_date: Дата бронирования
        booking_time: Время начала бронирования
        duration: Длительность бронирования в минутах
        exclude_booking_id: ID бронирования, которое нужно исключить из проверки (для обновления)
    
    Returns:
        True если стол свободен, False если занят
    """
    try:
        from datetime import datetime, timedelta
        
        with PostgreSQLDriver() as db:
            # Получаем все активные бронирования стола на эту дату
            # Исключаем только cancelled и completed
            bookings = db.select(
                Booking.TABLE_NAME,
                where={
                    'table_id': table_id,
                    'booking_date': booking_date
                }
            )
            
            # Фильтруем по статусу: исключаем отмененные и завершенные
            bookings = [b for b in bookings if b.get('status') not in ['cancelled', 'completed']]
            
            # Если есть exclude_booking_id, исключаем его из списка
            if exclude_booking_id is not None:
                bookings = [b for b in bookings if b['id'] != exclude_booking_id]
            
            # Если на эту дату нет бронирований - стол свободен
            if not bookings:
                return True
            
            # Вычисляем время начала и окончания запрашиваемого бронирования
            booking_datetime = datetime.combine(booking_date, booking_time)
            booking_end = booking_datetime + timedelta(minutes=duration)
            
            # Проверяем пересечение с каждым существующим бронированием
            for booking in bookings:
                # Получаем существующее бронирование
                existing_start = datetime.combine(booking['booking_date'], booking['booking_time'])
                existing_duration = booking.get('duration', 120)  # По умолчанию 120 минут
                existing_end = existing_start + timedelta(minutes=existing_duration)
                
                # Проверяем пересечение временных интервалов
                # Интервалы НЕ пересекаются если:
                # - новый бронирование заканчивается до начала существующего: booking_end <= existing_start
                # - новый бронирование начинается после конца существующего: booking_datetime >= existing_end
                # Интервалы ПЕРЕСЕКАЮТСЯ если НЕ выполнено ни одно из условий выше
                if not (booking_end <= existing_start or booking_datetime >= existing_end):
                    return False  # Стол занят (есть пересечение)
            
            # Стол свободен
            return True
            
    except Exception as e:
        print(f"Ошибка проверки доступности стола: {e}")
        return False


def get_table_availability(table_id: int, booking_date: date) -> List[Dict[str, Any]]:
    """
    Получение всех бронирований стола на указанную дату
    
    Args:
        table_id: ID стола
        booking_date: Дата для проверки
    
    Returns:
        Список бронирований на эту дату
    """
    try:
        with PostgreSQLDriver() as db:
            bookings = db.select(
                Booking.TABLE_NAME,
                where={
                    'table_id': table_id,
                    'booking_date': booking_date
                },
                order_by='booking_time ASC'
            )
            return bookings
    except Exception as e:
        print(f"Ошибка получения доступности стола: {e}")
        return []



if __name__ == "__main__":
    create_tables()