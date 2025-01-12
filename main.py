import tkinter as tk
from tkinter import messagebox
import datetime
import json

# Load and save tasks from/to file
tasks = []

def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

# GUI Functions
def update_task_list():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        status = "✓" if task["completed"] else "✗"
        due_date = task["due_date"] if task["due_date"] else "No due date"
        task_listbox.insert(tk.END, f"{status} {task['description']} (Due: {due_date})")

def add_task():
    description = entry_description.get()
    due_date = entry_due_date.get()

    # Validate due date
    if due_date:
        try:
            datetime.datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date (YYYY-MM-DD).")
            return

    tasks.append({"description": description, "due_date": due_date, "completed": False})
    save_tasks()
    update_task_list()
    entry_description.delete(0, tk.END)
    entry_due_date.delete(0, tk.END)

def complete_task():
    try:
        selected_index = task_listbox.curselection()[0]
        tasks[selected_index]["completed"] = True
        save_tasks()
        update_task_list()
    except IndexError:
        messagebox.showwarning("No Task Selected", "Please select a task to mark as completed.")

def delete_task():
    try:
        selected_index = task_listbox.curselection()[0]
        deleted_task = tasks.pop(selected_index)
        save_tasks()
        update_task_list()
        messagebox.showinfo("Task Deleted", f"Task '{deleted_task['description']}' deleted successfully!")
    except IndexError:
        messagebox.showwarning("No Task Selected", "Please select a task to delete.")

# GUI Setup
root = tk.Tk()
root.title("To-Do List App")

# Load existing tasks
tasks = load_tasks()

# Frame for Listbox and Scrollbar
frame_listbox = tk.Frame(root)
frame_listbox.pack(pady=10)

task_listbox = tk.Listbox(frame_listbox, height=10, width=50, selectmode=tk.SINGLE)
task_listbox.pack(side=tk.LEFT)

scrollbar = tk.Scrollbar(frame_listbox, orient=tk.VERTICAL, command=task_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

task_listbox.config(yscrollcommand=scrollbar.set)

# Input fields
label_description = tk.Label(root, text="Task Description:", font=("Helvetica", 12))
label_description.pack()

entry_description = tk.Entry(root, width=40, font=("Helvetica", 12))
entry_description.pack(pady=5)

label_due_date = tk.Label(root, text="Due Date (YYYY-MM-DD):", font=("Helvetica", 12))
label_due_date.pack()

entry_due_date = tk.Entry(root, width=40, font=("Helvetica", 12))
entry_due_date.pack(pady=5)

# Buttons with styling
button_add_task = tk.Button(root, text="Add Task", width=20, font=("Helvetica", 12, "bold"),
                            bg="#4CAF50", fg="white", relief="raised", command=add_task)
button_add_task.pack(pady=5)

button_complete_task = tk.Button(root, text="Complete Task", width=20, font=("Helvetica", 12, "bold"),
                                 bg="#008CBA", fg="white", relief="raised", command=complete_task)
button_complete_task.pack(pady=5)

button_delete_task = tk.Button(root, text="Delete Task", width=20, font=("Helvetica", 12, "bold"),
                               bg="#f44336", fg="white", relief="raised", command=delete_task)
button_delete_task.pack(pady=5)

# Initial update
update_task_list()

# Start the Tkinter event loop
root.mainloop()
