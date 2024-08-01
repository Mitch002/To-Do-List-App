from tkinter import *


# Create the main window
window = Tk()
window.title("My To Do List")
window.geometry("500x400")
tasks = {}
task_var = StringVar()

listbox = Listbox(window, width=50, height=20)
listbox.pack()

# Add function definitions

# Load tasks from txt file to list box
def load_tasks():
    global tasks
    tasks = {}
    try:
        with open("my_tasks.txt", "r") as task_file:
            for line in task_file.readlines():
                task_text, done_flag = line.strip().split(",")
                tasks[task_text] = (done_flag == "D")  
    except FileNotFoundError:
        print(f"Tasks file 'my_tasks.txt' not found. Starting with an empty list")
    update_listbox()

# Save task list to txt file
def save_tasks():
    try:
        with open("my_tasks.txt", "w") as task_file:
            for task_text, is_done in tasks.items():
                done_flag = "D" if is_done else "N"  
                task_file.write(f"{task_text},{done_flag}\n")
    except FileNotFoundError:
        print(f"Error could not save tasks to '{task_file}'")

# Update listbox with current txt file
def update_listbox():
    listbox.delete(0, END)
    for task_text, is_done in tasks.items():
        if is_done:
            listbox.insert(END, "** " + task_text + " ** DONE")
        else:
            listbox.insert(END, task_text)

# Mark tasks done
def mark_done():
    selected_index = listbox.curselection()
    if selected_index:
        task_text = listbox.get(selected_index[0])  
        tasks[task_text] = not tasks[task_text] 
        update_listbox()
        save_tasks()
    else:
        print("No task selected!")

# Undo mark tasks done
def undo_done():
    selected_index = listbox.curselection()
    if selected_index:
        full_text = listbox.get(selected_index[0])
        task_text = full_text.split('**')[1].strip()  
        if task_text in tasks:
            tasks[task_text] = not tasks[task_text]
            update_listbox()
            save_tasks()
        else:
            print(f"Task '{task_text}' not found. Cannot undo.")
    else:
        print("No task selected")

# Add task to list
def add_task():
    task = task_var.get()
    if task:
        tasks[task] = False 
        update_listbox()
        task_var.set("")
        save_tasks()

# Delete task from list
def delete_task():
    selected_index = listbox.curselection()
    if selected_index:
        index = selected_index[0]
        full_text = listbox.get(index)
        task_text = full_text.split('**')[1].strip() if "**" in full_text else full_text  
        for key in tasks.keys():
            if task_text in key:
                del tasks[key]  
                update_listbox()
                save_tasks()
                return
        print(f"Task '{task_text}' not found. Cannot delete.")
    else:
        print("No task selected")

# Clear all tasks from list
def clear_all():
    tasks.clear()
    update_listbox()
    save_tasks()

load_tasks()


entry = Entry(window, width=50, textvariable=task_var)
entry.pack()

# Button Frame for horizontal arrangement
button_frame = Frame(window)
button_frame.pack()

# Add Button
add_button = Button(button_frame, text="Add Task", command=add_task)
add_button.pack(side=LEFT, padx=5, pady=5)

# Mark Done Button
mark_done_button = Button(button_frame, text="Mark Done", command=mark_done)
mark_done_button.pack(side=LEFT, padx=5, pady=5)

# Delete Selected button
delete_button = Button(button_frame, text="Delete Selected", command=delete_task)
delete_button.pack(side=LEFT, padx=5, pady=5)

# Clear All button
clear_button = Button(button_frame, text="Clear All", command=clear_all)
clear_button.pack(side=LEFT, padx=5, pady=5)

# Undo button
undo_button = Button(button_frame, text="Undo", command=undo_done)
undo_button.pack(side=LEFT, padx=5, pady=5)


# Start the main event loop to display the window
window.mainloop()