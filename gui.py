#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Графический интерфейс для системы бронирования
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, date, time, timedelta
import backend


class BookingSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Система бронирования столов")
        self.root.geometry("1300x700")
        
        # Создаем вкладки
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Инициализация вкладок
        self.init_users_tab()
        self.init_tables_tab()
        self.init_bookings_tab()
        
        # Загружаем данные при запуске
        self.load_users()
        self.load_tables()
        self.load_bookings()
    
    # ==================== ВКЛАДКА ПОЛЬЗОВАТЕЛЕЙ ====================
    
    def init_users_tab(self):
        """Вкладка управления пользователями"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Пользователи")
        
        # Основной контейнер
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Левая часть - Таблица
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(left_frame, text="Список пользователей", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Таблица пользователей
        self.users_tree = ttk.Treeview(left_frame, columns=("id", "username", "email", "first_name", "last_name", "phone", "role", "status"), show="headings")
        self.users_tree.heading("id", text="ID")
        self.users_tree.heading("username", text="Имя пользователя")
        self.users_tree.heading("email", text="Email")
        self.users_tree.heading("first_name", text="Имя")
        self.users_tree.heading("last_name", text="Фамилия")
        self.users_tree.heading("phone", text="Телефон")
        self.users_tree.heading("role", text="Роль")
        self.users_tree.heading("status", text="Статус")
        
        self.users_tree.column("id", width=50)
        self.users_tree.column("username", width=120)
        self.users_tree.column("email", width=150)
        self.users_tree.column("first_name", width=100)
        self.users_tree.column("last_name", width=100)
        self.users_tree.column("phone", width=120)
        self.users_tree.column("role", width=80)
        self.users_tree.column("status", width=80)
        
        self.users_tree.pack(fill=tk.BOTH, expand=True)
        
        # Правая часть - Управление
        right_frame = ttk.LabelFrame(main_frame, text="Управление пользователями", padding=10)
        right_frame.pack(side=tk.RIGHT, padx=10, fill=tk.Y)
        
        ttk.Button(right_frame, text="Создать пользователя", command=self.create_user_dialog, width=25).pack(pady=5)
        ttk.Button(right_frame, text="Редактировать", command=self.edit_user_dialog, width=25).pack(pady=5)
        ttk.Button(right_frame, text="Удалить", command=self.delete_user_dialog, width=25).pack(pady=5)
        ttk.Button(right_frame, text="Обновить список", command=self.load_users, width=25).pack(pady=5)
        
        # Информация о пользователе
        ttk.Separator(right_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        ttk.Label(right_frame, text="Информация о пользователе", font=("Arial", 9, "bold")).pack(pady=5)
        self.user_info_text = scrolledtext.ScrolledText(right_frame, width=30, height=10)
        self.user_info_text.pack(pady=5)
        
        self.users_tree.bind("<<TreeviewSelect>>", self.on_user_select)
    
    def init_tables_tab(self):
        """Вкладка управления столами"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Столы")
        
        # Основной контейнер
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Левая часть - Таблица
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(left_frame, text="Список столов", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Таблица столов
        self.tables_tree = ttk.Treeview(left_frame, columns=("id", "number", "capacity", "location", "type", "status"), show="headings")
        self.tables_tree.heading("id", text="ID")
        self.tables_tree.heading("number", text="Номер")
        self.tables_tree.heading("capacity", text="Мест")
        self.tables_tree.heading("location", text="Расположение")
        self.tables_tree.heading("type", text="Тип")
        self.tables_tree.heading("status", text="Статус")
        
        self.tables_tree.column("id", width=50)
        self.tables_tree.column("number", width=80)
        self.tables_tree.column("capacity", width=60)
        self.tables_tree.column("location", width=180)
        self.tables_tree.column("type", width=150)
        self.tables_tree.column("status", width=80)
        
        self.tables_tree.pack(fill=tk.BOTH, expand=True)
        
        # Правая часть - Управление
        right_frame = ttk.LabelFrame(main_frame, text="Управление столами", padding=10)
        right_frame.pack(side=tk.RIGHT, padx=10, fill=tk.Y)
        
        ttk.Button(right_frame, text="Создать стол", command=self.create_table_dialog, width=25).pack(pady=5)
        ttk.Button(right_frame, text="Редактировать", command=self.edit_table_dialog, width=25).pack(pady=5)
        ttk.Button(right_frame, text="Удалить", command=self.delete_table_dialog, width=25).pack(pady=5)
        ttk.Button(right_frame, text="Обновить список", command=self.load_tables, width=25).pack(pady=5)
        
        # Информация о столе
        ttk.Separator(right_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        ttk.Label(right_frame, text="Информация о столе", font=("Arial", 9, "bold")).pack(pady=5)
        self.table_info_text = scrolledtext.ScrolledText(right_frame, width=30, height=10)
        self.table_info_text.pack(pady=5)
        
        self.tables_tree.bind("<<TreeviewSelect>>", self.on_table_select)
    
    def init_bookings_tab(self):
        """Вкладка управления бронированиями"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Бронирования")
        
        # Основной контейнер
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Левая часть - Таблица
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(left_frame, text="Список бронирований", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Таблица бронирований
        self.bookings_tree = ttk.Treeview(left_frame, columns=("id", "user", "table", "date", "start_time", "end_time", "guests"), show="headings")
        self.bookings_tree.heading("id", text="ID")
        self.bookings_tree.heading("user", text="Пользователь")
        self.bookings_tree.heading("table", text="Стол")
        self.bookings_tree.heading("date", text="Дата")
        self.bookings_tree.heading("start_time", text="Время начала")
        self.bookings_tree.heading("end_time", text="Время окончания")
        self.bookings_tree.heading("guests", text="Гостей")
        
        self.bookings_tree.column("id", width=50)
        self.bookings_tree.column("user", width=150)
        self.bookings_tree.column("table", width=100)
        self.bookings_tree.column("date", width=120)
        self.bookings_tree.column("start_time", width=100)
        self.bookings_tree.column("end_time", width=100)
        self.bookings_tree.column("guests", width=70)
        
        self.bookings_tree.pack(fill=tk.BOTH, expand=True)
        
        # Правая часть - Управление
        right_frame = ttk.LabelFrame(main_frame, text="Управление бронированиями", padding=10)
        right_frame.pack(side=tk.RIGHT, padx=10, fill=tk.Y)
        
        # Кнопки управления
        ttk.Button(right_frame, text="Создать бронирование", command=self.create_booking_dialog, width=25).pack(pady=5)
        ttk.Button(right_frame, text="Редактировать", command=self.edit_booking_dialog, width=25).pack(pady=5)
        ttk.Button(right_frame, text="Удалить", command=self.delete_booking_dialog, width=25).pack(pady=5)
        ttk.Button(right_frame, text="Обновить список", command=self.load_bookings, width=25).pack(pady=5)
        
        ttk.Separator(right_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Фильтры
        filter_frame = ttk.LabelFrame(right_frame, text="Фильтры", padding=10)
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="Дата (YYYY-MM-DD):").pack(anchor="w")
        self.filter_date_entry = ttk.Entry(filter_frame, width=22)
        self.filter_date_entry.pack(pady=5)
        
        ttk.Button(filter_frame, text="Фильтр по дате", command=self.filter_by_date, width=22).pack(pady=2)
        ttk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter, width=22).pack(pady=2)
        
        ttk.Separator(right_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Проверка доступности
        availability_frame = ttk.LabelFrame(right_frame, text="Проверка доступности", padding=10)
        availability_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(availability_frame, text="Проверить доступность", command=self.check_availability_dialog, width=22).pack(pady=2)
        
        ttk.Separator(right_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Информация о бронировании
        info_frame = ttk.LabelFrame(right_frame, text="Информация о бронировании", padding=10)
        info_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(info_frame, text="Детали", font=("Arial", 9, "bold")).pack(anchor="w")
        self.booking_info_text = scrolledtext.ScrolledText(info_frame, width=25, height=8)
        self.booking_info_text.pack(pady=5)
        
        self.bookings_tree.bind("<<TreeviewSelect>>", self.on_booking_select)
    
    # ==================== ОБРАБОТЧИКИ ВЫБОРА ====================
    
    def on_user_select(self, event):
        """Обработка выбора пользователя"""
        selected = self.users_tree.selection()
        if not selected:
            return
        
        user_id = int(self.users_tree.item(selected[0])['values'][0])
        user = backend.get_user_by_id(user_id)
        
        if user:
            info = f"ID: {user['id']}\n"
            info += f"Имя: {user['username']}\n"
            info += f"Email: {user['email']}\n"
            info += f"ФИО: {user.get('first_name', '')} {user.get('last_name', '')}\n"
            info += f"Телефон: {user.get('phone', '-')}\n"
            info += f"Роль: {user['role']}\n"
            info += f"Статус: {'Активен' if user['is_active'] else 'Неактивен'}"
            self.user_info_text.delete(1.0, tk.END)
            self.user_info_text.insert(1.0, info)
    
    def on_table_select(self, event):
        """Обработка выбора стола"""
        selected = self.tables_tree.selection()
        if not selected:
            return
        
        table_id = int(self.tables_tree.item(selected[0])['values'][0])
        table = backend.get_table_by_id(table_id)
        
        if table:
            info = f"ID: {table['id']}\n"
            info += f"Номер: №{table['number']}\n"
            info += f"Мест: {table['capacity']}\n"
            info += f"Расположение: {table.get('location', '-')}\n"
            info += f"Тип: {table.get('table_type', '-')}\n"
            info += f"Описание: {table.get('description', '-')}\n"
            info += f"Статус: {'Активен' if table['is_active'] else 'Неактивен'}"
            self.table_info_text.delete(1.0, tk.END)
            self.table_info_text.insert(1.0, info)
    
    def on_booking_select(self, event):
        """Обработка выбора бронирования"""
        selected = self.bookings_tree.selection()
        if not selected:
            return
        
        booking_id = int(self.bookings_tree.item(selected[0])['values'][0])
        booking = backend.get_booking_by_id(booking_id)
        
        if booking:
            # Получаем информацию о пользователе
            user = backend.get_user_by_id(booking['user_id'])
            user_name = f"{user['first_name']} {user['last_name']}" if user else f"ID:{booking['user_id']}"
            
            # Получаем информацию о столе
            table = backend.get_table_by_id(booking['table_id'])
            table_num = f"№{table['number']}" if table else f"ID:{booking['table_id']}"
            
            info = f"ID: {booking['id']}\n"
            info += f"Пользователь: {user_name}\n"
            info += f"Стол: {table_num}\n"
            info += f"Дата: {booking['booking_date']}\n"
            info += f"Время: {booking['booking_time']}\n"
            start_time = datetime.strptime(str(booking['booking_time']), "%H:%M:%S")
            end_time = start_time + timedelta(minutes=booking.get('duration', 120))
            info += f"Длительность: {booking.get('duration', 120)} мин\n"
            info += f"Гостей: {booking['guests_count']}\n"
            info += f"Статус: {booking['status']}"
            self.booking_info_text.delete(1.0, tk.END)
            self.booking_info_text.insert(1.0, info)
    
    # ==================== ФИЛЬТРАЦИЯ ====================
    
    def filter_by_date(self):
        """Фильтрация бронирований по дате"""
        date_str = self.filter_date_entry.get()
        if not date_str:
            messagebox.showwarning("Внимание", "Введите дату для фильтрации")
            return
        
        try:
            filter_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            bookings = backend.get_all_bookings(booking_date=filter_date)
            self.display_bookings(bookings)
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте YYYY-MM-DD")
    
    def reset_filter(self):
        """Сброс фильтра"""
        self.filter_date_entry.delete(0, tk.END)
        self.load_bookings()
    
    def display_bookings(self, bookings):
        """Отображение списка бронирований"""
        for item in self.bookings_tree.get_children():
            self.bookings_tree.delete(item)
        
        for booking in bookings:
            # Получаем информацию о пользователе
            user = backend.get_user_by_id(booking['user_id'])
            user_name = f"{user['first_name']} {user['last_name']}" if user else f"ID:{booking['user_id']}"
            
            # Получаем информацию о столе
            table = backend.get_table_by_id(booking['table_id'])
            table_num = f"№{table['number']}" if table else f"ID:{booking['table_id']}"
            
            # Вычисляем время окончания
            start_time = datetime.strptime(str(booking['booking_time']), "%H:%M:%S")
            end_time = start_time + timedelta(minutes=booking.get('duration', 120))
            
            self.bookings_tree.insert("", tk.END, values=(
                booking.get('id'),
                user_name,
                table_num,
                str(booking.get('booking_date')),
                str(booking.get('booking_time')),
                end_time.strftime("%H:%M"),
                booking.get('guests_count')
            ))
    
    # ==================== ДИАЛОГИ СОЗДАНИЯ ====================
    
    def create_user_dialog(self):
        """Диалоговое окно создания пользователя"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Создать пользователя")
        dialog.geometry("450x550")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)  # Фиксированный размер
        
        # Центральный контейнер
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(expand=True)
        
        ttk.Label(form_frame, text="Имя пользователя *").grid(row=0, column=0, pady=5)
        username_entry = ttk.Entry(form_frame, width=30)
        username_entry.grid(row=1, column=0, pady=5)
        
        ttk.Label(form_frame, text="Email *").grid(row=2, column=0, pady=5)
        email_entry = ttk.Entry(form_frame, width=30)
        email_entry.grid(row=3, column=0, pady=5)
        
        ttk.Label(form_frame, text="Пароль (hash) *").grid(row=4, column=0, pady=5)
        password_entry = ttk.Entry(form_frame, width=30)
        password_entry.grid(row=5, column=0, pady=5)
        
        ttk.Label(form_frame, text="Имя").grid(row=6, column=0, pady=5)
        first_name_entry = ttk.Entry(form_frame, width=30)
        first_name_entry.grid(row=7, column=0, pady=5)
        
        ttk.Label(form_frame, text="Фамилия").grid(row=8, column=0, pady=5)
        last_name_entry = ttk.Entry(form_frame, width=30)
        last_name_entry.grid(row=9, column=0, pady=5)
        
        ttk.Label(form_frame, text="Телефон").grid(row=10, column=0, pady=5)
        phone_entry = ttk.Entry(form_frame, width=30)
        phone_entry.grid(row=11, column=0, pady=5)
        
        ttk.Label(form_frame, text="Роль").grid(row=12, column=0, pady=5)
        role_combo = ttk.Combobox(form_frame, values=["user", "admin"], state="readonly", width=27)
        role_combo.grid(row=13, column=0, pady=5)
        role_combo.set("user")
        
        def save():
            if not username_entry.get() or not email_entry.get() or not password_entry.get():
                messagebox.showerror("Ошибка", "Заполните обязательные поля")
                return
            
            user_id = backend.create_user(
                username_entry.get(), email_entry.get(), password_entry.get(),
                first_name_entry.get() or None, last_name_entry.get() or None,
                phone_entry.get() or None, role_combo.get()
            )
            
            if user_id:
                messagebox.showinfo("Успех", f"Пользователь создан с ID: {user_id}")
                dialog.destroy()
                self.load_users()
            else:
                messagebox.showerror("Ошибка", "Не удалось создать пользователя")
        
        # Кнопки
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Создать", command=save, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
    
    def create_table_dialog(self):
        """Диалоговое окно создания стола"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Создать стол")
        dialog.geometry("450x520")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Центральный контейнер
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(expand=True)
        
        ttk.Label(form_frame, text="Номер стола *").grid(row=0, column=0, pady=5)
        number_entry = ttk.Entry(form_frame, width=30)
        number_entry.grid(row=1, column=0, pady=5)
        
        ttk.Label(form_frame, text="Количество мест *").grid(row=2, column=0, pady=5)
        capacity_entry = ttk.Entry(form_frame, width=30)
        capacity_entry.grid(row=3, column=0, pady=5)
        
        ttk.Label(form_frame, text="Расположение").grid(row=4, column=0, pady=5)
        location_entry = ttk.Entry(form_frame, width=30)
        location_entry.grid(row=5, column=0, pady=5)
        
        ttk.Label(form_frame, text="Тип стола").grid(row=6, column=0, pady=5)
        type_entry = ttk.Entry(form_frame, width=30)
        type_entry.grid(row=7, column=0, pady=5)
        
        ttk.Label(form_frame, text="Описание").grid(row=8, column=0, pady=5)
        description_text = tk.Text(form_frame, width=30, height=2)
        description_text.grid(row=9, column=0, pady=5)
        
        active_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(form_frame, text="Активен", variable=active_var).grid(row=10, column=0, pady=5)
        
        def save():
            try:
                number = int(number_entry.get())
                capacity = int(capacity_entry.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Номер и количество мест должны быть числами")
                return
            
            table_id = backend.create_table_record(
                number, capacity, location_entry.get() or None,
                type_entry.get() or None, active_var.get(),
                description_text.get(1.0, tk.END).strip() or None
            )
            
            if table_id:
                messagebox.showinfo("Успех", f"Стол создан с ID: {table_id}")
                dialog.destroy()
                self.load_tables()
            else:
                messagebox.showerror("Ошибка", "Не удалось создать стол")
        
        # Кнопки
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Создать", command=save, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
    
    def create_booking_dialog(self):
        """Диалоговое окно создания бронирования"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Создать бронирование")
        dialog.geometry("450x720")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Центральный контейнер
        main_frame = ttk.Frame(dialog, padding=15)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Загружаем пользователей и столы
        users = backend.get_all_users()
        tables = backend.get_all_tables(is_active=True)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(expand=True)
        
        ttk.Label(form_frame, text="Пользователь *").grid(row=0, column=0, pady=3)
        user_combo = ttk.Combobox(form_frame, state="readonly", width=28)
        user_combo.grid(row=1, column=0, pady=3)
        user_combo['values'] = [f"{u['id']} - {u['username']} ({u['email']})" for u in users]
        
        ttk.Label(form_frame, text="Стол *").grid(row=2, column=0, pady=3)
        table_combo = ttk.Combobox(form_frame, state="readonly", width=28)
        table_combo.grid(row=3, column=0, pady=3)
        table_combo['values'] = [f"{t['id']} - №{t['number']} ({t['capacity']} мест)" for t in tables]
        
        ttk.Label(form_frame, text="Дата (YYYY-MM-DD) *").grid(row=4, column=0, pady=3)
        date_entry = ttk.Entry(form_frame, width=30)
        date_entry.grid(row=5, column=0, pady=3)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ttk.Label(form_frame, text="Время (HH:MM) *").grid(row=6, column=0, pady=3)
        time_entry = ttk.Entry(form_frame, width=30)
        time_entry.grid(row=7, column=0, pady=3)
        time_entry.insert(0, "19:00")
        
        ttk.Label(form_frame, text="Количество гостей *").grid(row=8, column=0, pady=3)
        guests_entry = ttk.Entry(form_frame, width=30)
        guests_entry.grid(row=9, column=0, pady=3)
        
        ttk.Label(form_frame, text="Длительность (минут) *").grid(row=10, column=0, pady=3)
        duration_entry = ttk.Entry(form_frame, width=30)
        duration_entry.grid(row=11, column=0, pady=3)
        duration_entry.insert(0, "120")
        
        ttk.Label(form_frame, text="Статус").grid(row=12, column=0, pady=3)
        status_combo = ttk.Combobox(form_frame, values=["pending", "confirmed", "cancelled", "completed"], 
                                    state="readonly", width=27)
        status_combo.grid(row=13, column=0, pady=3)
        status_combo.set("pending")
        
        ttk.Label(form_frame, text="Телефон").grid(row=14, column=0, pady=3)
        phone_entry = ttk.Entry(form_frame, width=30)
        phone_entry.grid(row=15, column=0, pady=3)
        
        ttk.Label(form_frame, text="Контактное имя").grid(row=16, column=0, pady=3)
        contact_name_entry = ttk.Entry(form_frame, width=30)
        contact_name_entry.grid(row=17, column=0, pady=3)
        
        ttk.Label(form_frame, text="Особые запросы").grid(row=18, column=0, pady=3)
        special_requests_text = tk.Text(form_frame, width=30, height=2)
        special_requests_text.grid(row=19, column=0, pady=3)
        
        check_label = ttk.Label(form_frame, text="")
        check_label.grid(row=20, column=0, pady=5)
        
        def check_availability():
            if not table_combo.get() or not date_entry.get() or not time_entry.get():
                check_label.config(text="")
                return
            
            try:
                table_id = int(table_combo.get().split(" - ")[0])
                booking_date = datetime.strptime(date_entry.get(), "%Y-%m-%d").date()
                booking_time = datetime.strptime(time_entry.get(), "%H:%M").time()
                duration = int(duration_entry.get()) if duration_entry.get() else 120
                
                if backend.is_table_available(table_id, booking_date, booking_time, duration):
                    check_label.config(text="✓ Стол свободен", foreground="green")
                else:
                    check_label.config(text="✗ Стол занят на это время", foreground="red")
            except Exception:
                check_label.config(text="")
        
        table_combo.bind("<<ComboboxSelected>>", lambda e: check_availability())
        date_entry.bind("<KeyRelease>", lambda e: check_availability())
        time_entry.bind("<KeyRelease>", lambda e: check_availability())
        duration_entry.bind("<KeyRelease>", lambda e: check_availability())
        
        def save():
            if not user_combo.get() or not table_combo.get() or not date_entry.get() or not time_entry.get() or not guests_entry.get():
                messagebox.showerror("Ошибка", "Заполните все обязательные поля")
                return
            
            try:
                user_id = int(user_combo.get().split(" - ")[0])
                table_id = int(table_combo.get().split(" - ")[0])
                booking_date = datetime.strptime(date_entry.get(), "%Y-%m-%d").date()
                booking_time = datetime.strptime(time_entry.get(), "%H:%M").time()
                guests_count = int(guests_entry.get())
                duration = int(duration_entry.get()) if duration_entry.get() else 120
            except ValueError as e:
                messagebox.showerror("Ошибка", f"Неверный формат данных: {e}")
                return
            
            # Проверяем доступность с указанной длительностью
            if not backend.is_table_available(table_id, booking_date, booking_time, duration):
                from datetime import timedelta
                end_time = datetime.combine(booking_date, booking_time) + timedelta(minutes=duration)
                if not messagebox.askyesno(
                    "Предупреждение", 
                    f"Стол занят на это время ({booking_time} - {end_time.strftime('%H:%M')}).\n"
                    "Создать бронирование?"
                ):
                    return
            
            booking_id = backend.create_booking(
                user_id, table_id, booking_date, booking_time, guests_count,
                status_combo.get(), phone_entry.get() or None,
                contact_name_entry.get() or None,
                special_requests_text.get(1.0, tk.END).strip() or None,
                duration
            )
            
            if booking_id:
                messagebox.showinfo("Успех", f"Бронирование создано с ID: {booking_id}")
                dialog.destroy()
                self.load_bookings()
            else:
                messagebox.showerror("Ошибка", "Не удалось создать бронирование")
        
        # Кнопки
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Создать", command=save, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
    
    def check_availability_dialog(self):
        """Диалог проверки доступности стола"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Проверка доступности")
        dialog.geometry("350x300")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(form_frame, text="ID стола:").grid(row=0, column=0, pady=3)
        table_id_entry = ttk.Entry(form_frame, width=25)
        table_id_entry.grid(row=1, column=0, pady=3)
        
        ttk.Label(form_frame, text="Дата (YYYY-MM-DD):").grid(row=2, column=0, pady=3)
        date_entry = ttk.Entry(form_frame, width=25)
        date_entry.grid(row=3, column=0, pady=3)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ttk.Label(form_frame, text="Время (HH:MM):").grid(row=4, column=0, pady=3)
        time_entry = ttk.Entry(form_frame, width=25)
        time_entry.grid(row=5, column=0, pady=3)
        
        ttk.Label(form_frame, text="Длительность (мин):").grid(row=6, column=0, pady=3)
        duration_entry = ttk.Entry(form_frame, width=25)
        duration_entry.grid(row=7, column=0, pady=3)
        duration_entry.insert(0, "120")
        
        result_label = ttk.Label(form_frame, text="", font=("Arial", 10, "bold"))
        result_label.grid(row=8, column=0, pady=10)
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(side=tk.BOTTOM, pady=15)
        
        def check():
            try:
                table_id = int(table_id_entry.get())
                booking_date = datetime.strptime(date_entry.get(), "%Y-%m-%d").date()
                booking_time = datetime.strptime(time_entry.get(), "%H:%M").time()
                duration = int(duration_entry.get()) if duration_entry.get() else 120
                
                is_available = backend.is_table_available(table_id, booking_date, booking_time, duration)
                
                if is_available:
                    result_label.config(text="✓ СТОЛ СВОБОДЕН", foreground="green")
                else:
                    result_label.config(text="✗ СТОЛ ЗАНЯТ", foreground="red")
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректные данные")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        
        ttk.Button(btn_frame, text="Проверить", command=check, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Закрыть", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
    
    # ==================== РЕДАКТИРОВАНИЕ И УДАЛЕНИЕ ====================
    
    def edit_user_dialog(self):
        """Диалог редактирования пользователя"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите пользователя")
            return
        
        user_id = int(self.users_tree.item(selected[0])['values'][0])
        user = backend.get_user_by_id(user_id)
        if not user:
            messagebox.showerror("Ошибка", "Пользователь не найден")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактировать пользователя")
        dialog.geometry("400x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(form_frame, text="Имя").grid(row=0, column=0, sticky="w", pady=5)
        first_name_entry = ttk.Entry(form_frame, width=35)
        first_name_entry.insert(0, user.get('first_name', ''))
        first_name_entry.grid(row=1, column=0, pady=5)
        
        ttk.Label(form_frame, text="Фамилия").grid(row=2, column=0, sticky="w", pady=5)
        last_name_entry = ttk.Entry(form_frame, width=35)
        last_name_entry.insert(0, user.get('last_name', ''))
        last_name_entry.grid(row=3, column=0, pady=5)
        
        ttk.Label(form_frame, text="Телефон").grid(row=4, column=0, sticky="w", pady=5)
        phone_entry = ttk.Entry(form_frame, width=35)
        phone_entry.insert(0, user.get('phone', ''))
        phone_entry.grid(row=5, column=0, pady=5)
        
        ttk.Label(form_frame, text="Роль").grid(row=6, column=0, sticky="w", pady=5)
        role_combo = ttk.Combobox(form_frame, values=["user", "admin"], state="readonly", width=32)
        role_combo.set(user['role'])
        role_combo.grid(row=7, column=0, pady=5)
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(side=tk.BOTTOM, pady=15)
        
        def save():
            update_data = {}
            if first_name_entry.get():
                update_data['first_name'] = first_name_entry.get()
            if last_name_entry.get():
                update_data['last_name'] = last_name_entry.get()
            if phone_entry.get():
                update_data['phone'] = phone_entry.get()
            update_data['role'] = role_combo.get()
            
            if backend.update_user(user_id, **update_data):
                messagebox.showinfo("Успех", "Пользователь обновлен")
                dialog.destroy()
                self.load_users()
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить пользователя")
        
        ttk.Button(btn_frame, text="Сохранить", command=save, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
    
    def edit_table_dialog(self):
        """Диалог редактирования стола"""
        selected = self.tables_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите стол")
            return
        
        table_id = int(self.tables_tree.item(selected[0])['values'][0])
        table = backend.get_table_by_id(table_id)
        if not table:
            messagebox.showerror("Ошибка", "Стол не найден")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактировать стол")
        dialog.geometry("400x450")
        dialog.transient(self.root)
        dialog.grab_set()
        
        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(form_frame, text="Расположение").grid(row=0, column=0, sticky="w", pady=5)
        location_entry = ttk.Entry(form_frame, width=35)
        location_entry.insert(0, table.get('location', ''))
        location_entry.grid(row=1, column=0, pady=5)
        
        ttk.Label(form_frame, text="Тип стола").grid(row=2, column=0, sticky="w", pady=5)
        type_entry = ttk.Entry(form_frame, width=35)
        type_entry.insert(0, table.get('table_type', ''))
        type_entry.grid(row=3, column=0, pady=5)
        
        ttk.Label(form_frame, text="Описание").grid(row=4, column=0, sticky="w", pady=5)
        description_text = tk.Text(form_frame, width=35, height=3)
        description_text.insert(1.0, table.get('description', ''))
        description_text.grid(row=5, column=0, pady=5)
        
        active_var = tk.BooleanVar(value=table.get('is_active', True))
        ttk.Checkbutton(form_frame, text="Активен", variable=active_var).grid(row=6, column=0, pady=5, sticky="w")
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(side=tk.BOTTOM, pady=15)
        
        def save():
            update_data = {}
            if location_entry.get():
                update_data['location'] = location_entry.get()
            if type_entry.get():
                update_data['table_type'] = type_entry.get()
            if description_text.get(1.0, tk.END).strip():
                update_data['description'] = description_text.get(1.0, tk.END).strip()
            update_data['is_active'] = active_var.get()
            
            if backend.update_table(table_id, **update_data):
                messagebox.showinfo("Успех", "Стол обновлен")
                dialog.destroy()
                self.load_tables()
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить стол")
        
        ttk.Button(btn_frame, text="Сохранить", command=save, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
    
    def edit_booking_dialog(self):
        """Диалог редактирования бронирования"""
        selected = self.bookings_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите бронирование")
            return
        
        booking_id = int(self.bookings_tree.item(selected[0])['values'][0])
        booking = backend.get_booking_by_id(booking_id)
        if not booking:
            messagebox.showerror("Ошибка", "Бронирование не найдено")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактировать бронирование")
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(form_frame, text="Количество гостей").grid(row=0, column=0, sticky="w", pady=5)
        guests_entry = ttk.Entry(form_frame, width=35)
        guests_entry.insert(0, str(booking['guests_count']))
        guests_entry.grid(row=1, column=0, pady=5)
        
        ttk.Label(form_frame, text="Статус").grid(row=2, column=0, sticky="w", pady=5)
        status_combo = ttk.Combobox(form_frame, values=["pending", "confirmed", "cancelled", "completed"], 
                                   state="readonly", width=32)
        status_combo.set(booking['status'])
        status_combo.grid(row=3, column=0, pady=5)
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(side=tk.BOTTOM, pady=15)
        
        def save():
            try:
                guests_count = int(guests_entry.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Количество гостей должно быть числом")
                return
            
            if backend.update_booking(booking_id, guests_count=guests_count, status=status_combo.get()):
                messagebox.showinfo("Успех", "Бронирование обновлено")
                dialog.destroy()
                self.load_bookings()
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить бронирование")
        
        ttk.Button(btn_frame, text="Сохранить", command=save, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
    
    def delete_user_dialog(self):
        """Удаление пользователя"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите пользователя")
            return
        
        if not messagebox.askyesno("Подтверждение", "Удалить этого пользователя?"):
            return
        
        user_id = int(self.users_tree.item(selected[0])['values'][0])
        if backend.delete_user(user_id):
            messagebox.showinfo("Успех", "Пользователь удален")
            self.load_users()
        else:
            messagebox.showerror("Ошибка", "Не удалось удалить пользователя")
    
    def delete_table_dialog(self):
        """Удаление стола"""
        selected = self.tables_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите стол")
            return
        
        if not messagebox.askyesno("Подтверждение", "Удалить этот стол?"):
            return
        
        table_id = int(self.tables_tree.item(selected[0])['values'][0])
        if backend.delete_table(table_id):
            messagebox.showinfo("Успех", "Стол удален")
            self.load_tables()
        else:
            messagebox.showerror("Ошибка", "Не удалось удалить стол")
    
    def delete_booking_dialog(self):
        """Удаление бронирования"""
        selected = self.bookings_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите бронирование")
            return
        
        if not messagebox.askyesno("Подтверждение", "Удалить это бронирование?"):
            return
        
        booking_id = int(self.bookings_tree.item(selected[0])['values'][0])
        if backend.delete_booking(booking_id):
            messagebox.showinfo("Успех", "Бронирование удалено")
            self.load_bookings()
        else:
            messagebox.showerror("Ошибка", "Не удалось удалить бронирование")
    
    # ==================== ЗАГРУЗКА ДАННЫХ ====================
    
    def load_users(self):
        """Загрузка списка пользователей"""
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        users = backend.get_all_users()
        for user in users:
            status = "Активен" if user.get('is_active') else "Неактивен"
            self.users_tree.insert("", tk.END, values=(
                user.get('id'), user.get('username'), user.get('email'),
                user.get('first_name', ''), user.get('last_name', ''),
                user.get('phone', ''), user.get('role'), status
            ))
    
    def load_tables(self):
        """Загрузка списка столов"""
        for item in self.tables_tree.get_children():
            self.tables_tree.delete(item)
        
        tables = backend.get_all_tables()
        for table in tables:
            status = "Активен" if table.get('is_active') else "Неактивен"
            self.tables_tree.insert("", tk.END, values=(
                table.get('id'), table.get('number'), table.get('capacity'),
                table.get('location', ''), table.get('table_type', ''), status
            ))
    
    def load_bookings(self):
        """Загрузка списка бронирований"""
        for item in self.bookings_tree.get_children():
            self.bookings_tree.delete(item)
        
        bookings = backend.get_all_bookings()
        for booking in bookings:
            # Получаем информацию о пользователе
            user = backend.get_user_by_id(booking['user_id'])
            user_name = f"{user['first_name']} {user['last_name']}" if user and user.get('first_name') and user.get('last_name') else (user['username'] if user else f"ID:{booking['user_id']}")
            
            # Получаем информацию о столе
            table = backend.get_table_by_id(booking['table_id'])
            table_num = f"№{table['number']}" if table else f"ID:{booking['table_id']}"
            
            # Вычисляем время окончания
            start_time = datetime.strptime(str(booking['booking_time']), "%H:%M:%S")
            end_time = start_time + timedelta(minutes=booking.get('duration', 120))
            
            self.bookings_tree.insert("", tk.END, values=(
                booking.get('id'), user_name, table_num,
                str(booking.get('booking_date')),
                str(booking.get('booking_time')),
                end_time.strftime("%H:%M"),
                booking.get('guests_count')
            ))


def main():
    root = tk.Tk()
    app = BookingSystemGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
