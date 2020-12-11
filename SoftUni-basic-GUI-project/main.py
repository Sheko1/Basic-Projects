from tkinter.ttk import Combobox
from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
import json


def clear_view(tk):
    for i in tk.grid_slaves():
        i.destroy()


def get_all_tasks():
    try:
        with open("DB.txt", "r") as f:
            all_tasks = json.load(f)
            f.close()

    except Exception as e:
        print(e)
        all_tasks = []

    return all_tasks


def edit_task(**kwargs):
    msg_box = messagebox.askquestion("Edit", "Are you sure you want to edit this task?", icon="warning")
    if msg_box == "yes":
        all_tasks = get_all_tasks()
        index = kwargs.pop('index')
        all_tasks[index] = kwargs

        with open("DB.txt", "w+") as f:
            json.dump(all_tasks, f)
            f.close()

        view_tasks(master)


def edit_task_view(tk, task):
    if task:
        clear_view(tk)
        task = eval(task)
        get_all_tasks()
        index = get_all_tasks().index(task)

        tk.geometry("500x500")
        tk.title("Edit task")
        Label(tk, text="Enter your task name:").grid(row=0, column=0, padx=15, pady=25)
        name = Entry(tk, width=30)
        name.grid(row=0, column=1)
        name.insert(0, task['name'])

        Label(tk, text="Due date:").grid(row=1, column=0, pady=25)
        date = DateEntry(tk)
        date.grid(row=1, column=1)
        date.delete(0, END)
        date.insert(0, task['date'])

        Label(tk, text="Description:").grid(row=2, column=0, pady=25)
        description = Text(tk, width=25, height=10)
        description.grid(row=2, column=1)
        description.insert(INSERT, task['description'])

        Label(tk, text="Select priority:").grid(row=3, column=0, pady=25)
        priority = IntVar()
        current_priority = task['priority']

        rb1 = Radiobutton(tk, text="Low", value=1, variable=priority)
        rb2 = Radiobutton(tk, text="Medium", value=2, variable=priority)
        rb3 = Radiobutton(tk, text="High", value=3, variable=priority)

        if current_priority == 1:
            rb1.select()

        elif current_priority == 2:
            rb2.select()

        else:
            rb3.select()

        rb1.grid(row=3, column=1)
        rb2.grid(row=3, column=2)
        rb3.grid(row=3, column=3)

        Label(tk, text="Check if completed:").grid(row=4, column=0, pady=25)
        is_completed = BooleanVar()
        is_completed.set(task['is_completed'])
        Checkbutton(tk, text="Choose", variable=is_completed).grid(row=4, column=1)

        Button(tk, text="Edit task", bg="yellow",
               command=lambda: edit_task(name=name.get(), date=date.get(), description=description.get('1.0', END),
                                         priority=priority.get(), is_completed=is_completed.get(), index=index)) \
            .grid(row=5, column=0, pady=15)
        Button(tk, text="Cancel", bg="black", fg="white", command=lambda: view_tasks(tk)).grid(row=5, column=1)

    else:
        messagebox.showinfo("Error", "Please select a task!")


def delete_task(task_to_delete):
    if task_to_delete:
        msg_box = messagebox.askquestion("Delete", "Are you sure you want to delete this task?", icon="warning")

        if msg_box == "yes":
            all_tasks = get_all_tasks()
            all_tasks.remove(eval(task_to_delete))
    
            if len(all_tasks) > 0:
                with open("DB.txt", "w") as f:
                    json.dump(all_tasks, f)
                    f.close()

            else:
                open("DB.txt", "w").close()

            main_screen(master)

    else:
        messagebox.showinfo("Error", "Please select a task!")


def create_task(**kwargs):
    all_tasks = get_all_tasks()
    all_tasks.append(kwargs)

    with open("DB.txt", "w+") as f:
        json.dump(all_tasks, f)
        f.close()

    main_screen(master)


def add_task(tk):
    clear_view(tk)

    tk.title("Add task")
    tk.geometry("500x500")
    Label(tk, text="Enter your task name:").grid(row=0, column=0, padx=15, pady=25)
    name = Entry(tk, width=30)
    name.grid(row=0, column=1)

    Label(tk, text="Due date:").grid(row=1, column=0, pady=25)
    date = DateEntry(tk)
    date.grid(row=1, column=1)

    Label(tk, text="Description:").grid(row=2, column=0, pady=25)
    description = Text(tk, width=25, height=10)
    description.grid(row=2, column=1)

    Label(tk, text="Select priority:").grid(row=3, column=0, pady=25)
    priority = IntVar()
    Radiobutton(tk, text="Low", value=1, variable=priority).grid(row=3, column=1)
    Radiobutton(tk, text="Medium", value=2, variable=priority).grid(row=3, column=2)
    Radiobutton(tk, text="High", value=3, variable=priority).grid(row=3, column=3)

    Label(tk, text="Check if completed:").grid(row=4, column=0, pady=25)
    is_completed = BooleanVar()
    Checkbutton(tk, text="Choose", variable=is_completed).grid(row=4, column=1)

    Button(tk, text="Create task", bg="green", fg="white",
           command=lambda: create_task(name=name.get(), date=date.get(), description=description.get('1.0', END),
                                       priority=priority.get(), is_completed=is_completed.get())) \
        .grid(row=5, column=0, pady=15)
    Button(tk, text="Cancel", bg="black", fg="white", command=lambda: main_screen(tk)).grid(row=5, column=1)


def view_tasks(tk):
    try:
        with open("DB.txt", "r") as f:
            all_tasks = json.load(f)
            f.close()

        clear_view(tk)
        tk.geometry("600x300")
        tk.title("View tasks")

        box = Combobox(tk, width=80)
        box['values'] = all_tasks
        box.grid(row=0, column=0)

        Button(tk, text="Edit task", bg="yellow", command=lambda: edit_task_view(tk, box.get())).grid(row=1,
                                                                                                      column=1, pady=25)
        Button(tk, text="Delete task", bg="red", fg="white", command=lambda: delete_task(box.get())).grid(row=2,
                                                                                                          column=1)
        Button(tk, text="Cancel", bg="black", fg="white", command=lambda: main_screen(tk)).grid(row=3, column=1,
                                                                                                pady=25)

    except Exception as e:
        print(e)
        messagebox.showinfo("Error", "You don't have eny tasks")


def main_screen(tk):
    clear_view(tk)

    tk.geometry("300x300")
    tk.title("Main")
    tk.resizable(width=False, height=False)

    Button(tk, text="View tasks", width=10, bg="blue", fg="white", command=lambda: view_tasks(tk)) \
        .grid(row=0, padx=110, pady=70)
    Button(tk, text="Add task", width=10, bg="red", fg="white", command=lambda: add_task(tk)).grid(row=1)


master = Tk()

main_screen(master)

master.mainloop()
