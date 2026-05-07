import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker - Управление прочитанными книгами")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        # Список книг
        self.books = []
        self.filtered_books = []
        
        # Загрузка данных из файла
        self.load_data()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление таблицы
        self.refresh_table()
    
    def create_widgets(self):
        """Создание всех элементов интерфейса"""
        
        # === Левая панель: ввод данных ===
        input_frame = tk.LabelFrame(self.root, text="Добавление новой книги", padx=10, pady=10, font=("Arial", 12, "bold"))
        input_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        
        # Поле: Название
        tk.Label(input_frame, text="Название книги:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_title = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.entry_title.grid(row=0, column=1, pady=5, padx=5)
        
        # Поле: Автор
        tk.Label(input_frame, text="Автор:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_author = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.entry_author.grid(row=1, column=1, pady=5, padx=5)
        
        # Поле: Жанр
        tk.Label(input_frame, text="Жанр:", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_genre = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.entry_genre.grid(row=2, column=1, pady=5, padx=5)
        
        # Поле: Количество страниц
        tk.Label(input_frame, text="Количество страниц:", font=("Arial", 10)).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entry_pages = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.entry_pages.grid(row=3, column=1, pady=5, padx=5)
        
        # Кнопка "Добавить книгу"
        self.btn_add = tk.Button(input_frame, text="➕ Добавить книгу", command=self.add_book,
                                 bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), padx=10, pady=5)
        self.btn_add.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Разделитель
        separator = ttk.Separator(input_frame, orient='horizontal')
        separator.grid(row=5, column=0, columnspan=2, sticky="ew", pady=10)
        
        # === Панель фильтрации ===
        filter_frame = tk.LabelFrame(input_frame, text="Фильтрация", padx=10, pady=10, font=("Arial", 12, "bold"))
        filter_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")
        
        # Фильтр по жанру
        tk.Label(filter_frame, text="Жанр:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.filter_genre = tk.Entry(filter_frame, width=20, font=("Arial", 10))
        self.filter_genre.grid(row=0, column=1, pady=5, padx=5)
        
        # Фильтр по страницам
        tk.Label(filter_frame, text="Страниц больше:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.filter_pages = tk.Entry(filter_frame, width=20, font=("Arial", 10))
        self.filter_pages.grid(row=1, column=1, pady=5, padx=5)
        
        # Кнопка "Применить фильтр"
        self.btn_filter = tk.Button(filter_frame, text="🔍 Применить фильтр", command=self.apply_filter,
                                    bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
        self.btn_filter.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Кнопка "Сбросить фильтр"
        self.btn_reset = tk.Button(filter_frame, text="🗑 Сбросить фильтр", command=self.reset_filter,
                                   bg="#FF9800", fg="white", font=("Arial", 10, "bold"))
        self.btn_reset.grid(row=3, column=0, columnspan=2, pady=5)
        
        # === Правая панель: таблица книг ===
        table_frame = tk.Frame(self.root)
        table_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Скроллбары
        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        # Таблица (Treeview)
        columns = ("Название", "Автор", "Жанр", "Страницы")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                                  yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        # Настройка заголовков
        self.tree.heading("Название", text="Название книги")
        self.tree.heading("Автор", text="Автор")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Страницы", text="Страниц")
        
        # Настройка ширины колонок
        self.tree.column("Название", width=250)
        self.tree.column("Автор", width=150)
        self.tree.column("Жанр", width=120)
        self.tree.column("Страницы", width=80, anchor=tk.CENTER)
        
        # Упаковка скроллбаров
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Упаковка таблицы
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Кнопка "Удалить выбранную книгу"
        self.btn_delete = tk.Button(table_frame, text="❌ Удалить выбранную книгу", command=self.delete_book,
                                    bg="#f44336", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        self.btn_delete.pack(pady=10)
    
    def add_book(self):
        """Добавление новой книги"""
        title = self.entry_title.get().strip()
        author = self.entry_author.get().strip()
        genre = self.entry_genre.get().strip()
        pages = self.entry_pages.get().strip()
        
        # Проверка на пустые поля
        if not title or not author or not genre or not pages:
            messagebox.showwarning("Предупреждение", "Пожалуйста, заполните все поля!")
            return
        
        # Проверка, что количество страниц - число
        try:
            pages = int(pages)
            if pages <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
            return
        
        # Добавление книги
        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages
        }
        self.books.append(book)
        
        # Очистка полей
        self.entry_title.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_pages.delete(0, tk.END)
        
        # Сохранение и обновление
        self.save_data()
        self.refresh_table()
        
        messagebox.showinfo("Успех", f"Книга \"{title}\" добавлена!")
    
    def delete_book(self):
        """Удаление выбранной книги"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите книгу для удаления!")
            return
        
        # Получаем индекс выбранной книги
        item = self.tree.item(selected[0])
        title = item['values'][0]
        
        # Подтверждение удаления
        if messagebox.askyesno("Подтверждение", f"Удалить книгу \"{title}\"?"):
            # Удаляем из списка
            index = self.tree.index(selected[0])
            if self.filtered_books:
                # Если включён фильтр, удаляем из отфильтрованного списка
                book_to_remove = self.filtered_books[index]
                self.books.remove(book_to_remove)
            else:
                self.books.pop(index)
            
            self.save_data()
            self.refresh_table()
            messagebox.showinfo("Успех", "Книга удалена!")
    
    def apply_filter(self):
        """Применение фильтрации"""
        genre_filter = self.filter_genre.get().strip().lower()
        pages_filter = self.filter_pages.get().strip()
        
        self.filtered_books = self.books.copy()
        
        # Фильтр по жанру
        if genre_filter:
            self.filtered_books = [book for book in self.filtered_books 
                                   if genre_filter in book["genre"].lower()]
        
        # Фильтр по страницам
        if pages_filter:
            try:
                min_pages = int(pages_filter)
                self.filtered_books = [book for book in self.filtered_books 
                                       if book["pages"] > min_pages]
            except ValueError:
                messagebox.showerror("Ошибка", "Фильтр по страницам должен быть числом!")
                return
        
        self.display_books(self.filtered_books)
    
    def reset_filter(self):
        """Сброс фильтрации"""
        self.filter_genre.delete(0, tk.END)
        self.filter_pages.delete(0, tk.END)
        self.filtered_books = []
        self.display_books(self.books)
    
    def display_books(self, books):
        """Отображение книг в таблице"""
        # Очистка таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Заполнение таблицы
        for book in books:
            self.tree.insert("", tk.END, values=(book["title"], book["author"], 
                                                 book["genre"], book["pages"]))
    
    def refresh_table(self):
        """Обновление таблицы (с учётом фильтра)"""
        if self.filtered_books:
            self.display_books(self.filtered_books)
        else:
            self.display_books(self.books)
    
    def save_data(self):
        """Сохранение данных в JSON"""
        try:
            with open("books.json", "w", encoding="utf-8") as file:
                json.dump(self.books, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")
    
    def load_data(self):
        """Загрузка данных из JSON"""
        if os.path.exists("books.json"):
            try:
                with open("books.json", "r", encoding="utf-8") as file:
                    self.books = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                self.books = []
        else:
            self.books = []


if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()