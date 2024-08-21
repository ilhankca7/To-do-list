import tkinter as tk
from tkinter import messagebox
import sqlite3

class ToDoApp:
    def __init__(self,root):
        self.root = root
        self.root.title("To-Do List")

        self.conn = sqlite3.connect("todo.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        self.task_entry = tk.Entry(root, width=40) #Metin kutusu
        self.task_entry.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Task",command=self.add_task)
        self.add_button.pack(pady=5)

        self.task_listbox = tk.Listbox(root, width=60, height=15)
        self.task_listbox.pack(pady=10)

        self.load_tasks()

        self.delete_button = tk.Button(root, text="Delete Task",command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.complete_button= tk.Button(root, text="Complete Task", command=self.complete_task)
        self.complete_button.pack(pady=5)
    def create_table(self):
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)))
                ''')
        self.conn.commit()
    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.cursor.execute("INSERT INTO tasks (task, completed) VALUES (?, 0)",(task,))
            self.conn.commit()
            self.task_entry.delete(0, tk.END)
            self.load_tasks()
        else:
            messagebox.showwarning("Warning","Task Cannot be empty")

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT id, task, completed FROM tasks")
        tasks = self.cursor.fetchall()
        for task in tasks:
            display_text = f"[{'X' if task[2] else ' '}] {task[1]}"
            self.task_listbox.insert(tk.END, (task[0], display_text))
    def delete_task(self):
        selected_task = self.task_listbox.curselection()
        if selected_task:
            task_id = self.task_listbox.get(selected_task)[0]
            self.cursor.execute("DELETE FROM tasks WHERE id = ?",(task_id,))
            self.conn.commit()
            self.load_tasks()
        else:
            messagebox.showwarning("warning","Select a task to delete.")

    def complete_task(self):
        selected_task = self.task_listbox.curselection()
        if selected_task:
            task_id = self.task_listbox.get(selected_task)[0]
            self.cursor.execute('UPDATE tasks SET completed = 1 WHERE id = ?',(task_id,))
            self.conn.commit()
            self.load_tasks()
        else:
            messagebox.showwarning("Warning","Select a task to mark as complete")

if __name__== "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()


















