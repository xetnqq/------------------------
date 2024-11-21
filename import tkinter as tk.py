import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_NAME = "tasks.json"


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер Завдань")

        # Список для завдань
        self.tasks = []
        self.load_tasks()

        # Фрейми для колонок
        self.active_frame = tk.LabelFrame(root, text="Активні Завдання", padx=10, pady=10)
        self.completed_frame = tk.LabelFrame(root, text="Виконані Завдання", padx=10, pady=10)
        self.active_frame.grid(row=0, column=0, padx=10, pady=10)
        self.completed_frame.grid(row=0, column=1, padx=10, pady=10)

        # Поле введення нового завдання
        self.new_task_entry = tk.Entry(root, width=40)
        self.new_task_entry.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Кнопки
        self.add_task_button = tk.Button(root, text="Додати Завдання", command=self.add_task)
        self.add_task_button.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        # Відображення завдань
        self.refresh_task_lists()

    def load_tasks(self):
        """Завантажує завдання з JSON-файлу."""
        if not os.path.exists(FILE_NAME):
            self.save_tasks()  # Створити файл, якщо його немає
        try:
            with open(FILE_NAME, "r") as file:
                self.tasks = json.load(file)
        except (json.JSONDecodeError, IOError):
            messagebox.showerror("Помилка", "Файл завдань пошкоджений. Дані буде скинуто.")
            self.tasks = []
            self.save_tasks()

    def save_tasks(self):
        """Зберігає завдання у JSON-файл."""
        with open(FILE_NAME, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self):
        """Додає нове завдання."""
        task_text = self.new_task_entry.get().strip()
        if task_text:
            self.tasks.append({"task": task_text, "completed": False})
            self.new_task_entry.delete(0, tk.END)
            self.save_tasks()
            self.refresh_task_lists()
        else:
            messagebox.showwarning("Попередження", "Завдання не може бути порожнім.")

    def mark_task_completed(self, task_index):
        """Позначає завдання як виконане."""
        self.tasks[task_index]["completed"] = True
        self.save_tasks()
        self.refresh_task_lists()

    def delete_task(self, task_index):
        """Видаляє завдання."""
        del self.tasks[task_index]
        self.save_tasks()
        self.refresh_task_lists()

    def move_task_to_active(self, task_index):
        """Переміщує виконане завдання назад до активних."""
        self.tasks[task_index]["completed"] = False
        self.save_tasks()
        self.refresh_task_lists()

    def refresh_task_lists(self):
        """Оновлює списки завдань у графічному інтерфейсі."""
        for widget in self.active_frame.winfo_children():
            widget.destroy()
        for widget in self.completed_frame.winfo_children():
            widget.destroy()

        # Відображення активних завдань
        for index, task in enumerate(self.tasks):
            if not task["completed"]:
                task_frame = tk.Frame(self.active_frame)
                task_frame.pack(fill="x", pady=2)
                tk.Label(task_frame, text=task["task"], width=30, anchor="w").pack(side="left")
                tk.Button(task_frame, text="Виконано", command=lambda idx=index: self.mark_task_completed(idx)).pack(side="right")
                tk.Button(task_frame, text="Видалити", command=lambda idx=index: self.delete_task(idx)).pack(side="right")

        # Відображення виконаних завдань
        for index, task in enumerate(self.tasks):
            if task["completed"]:
                task_frame = tk.Frame(self.completed_frame)
                task_frame.pack(fill="x", pady=2)
                tk.Label(task_frame, text=task["task"], width=30, anchor="w").pack(side="left")
                tk.Button(task_frame, text="Активувати", command=lambda idx=index: self.move_task_to_active(idx)).pack(side="right")
                tk.Button(task_frame, text="Видалити", command=lambda idx=index: self.delete_task(idx)).pack(side="right")


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
