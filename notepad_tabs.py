import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog, font

root = tk.Tk()
root.title("Python Notepad with Tabs")
root.geometry("900x600")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Dictionary to store file paths for each tab
file_paths = {}

# ========== FUNCTIONS ==========

def new_tab(name="Untitled"):
    """Create a new tab with a text area"""
    frame = ttk.Frame(notebook)
    text_area = tk.Text(frame, wrap="word", undo=True)
    text_area.pack(fill="both", expand=True)

    # Scrollbar
    scroll = tk.Scrollbar(text_area)
    scroll.pack(side="right", fill="y")
    scroll.config(command=text_area.yview)
    text_area.config(yscrollcommand=scroll.set)

    notebook.add(frame, text=name)
    notebook.select(frame)
    file_paths[frame] = None

def current_text_area():
    """Return the text widget of the current tab"""
    current_tab = notebook.select()
    if not current_tab:
        return None
    frame = notebook.nametowidget(current_tab)
    return frame.winfo_children()[0]  # first child is text_area

def new_file():
    new_tab()

def open_file():
    """Open and read a file into current tab"""
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        new_tab(name=file_path.split("/")[-1])
        text = current_text_area()
        text.delete(1.0, tk.END)
        text.insert(1.0, content)
        frame = notebook.nametowidget(notebook.select())
        file_paths[frame] = file_path

def save_file():
    """Save current tab content"""
    text = current_text_area()
    if not text:
        return

    frame = notebook.nametowidget(notebook.select())
    file_path = file_paths.get(frame)

    if not file_path:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not file_path:
            return

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text.get(1.0, tk.END))

    file_paths[frame] = file_path
    notebook.tab(frame, text=file_path.split("/")[-1])
    messagebox.showinfo("Saved", f"File saved successfully:\n{file_path}")

def close_tab():
    """Close the current tab"""
    if len(notebook.tabs()) > 0:
        current = notebook.select()
        notebook.forget(current)

def exit_app():
    if messagebox.askyesno("Confirm Exit", "Do you want to exit?"):
        root.destroy()

# ========== TEXT FEATURES ==========

def find_replace():
    text = current_text_area()
    if not text:
        return
    find = simpledialog.askstring("Find", "Find what:")
    if not find:
        return
    replace = simpledialog.askstring("Replace", "Replace with:")
    if replace is None:
        return
    content = text.get(1.0, tk.END)
    text.delete(1.0, tk.END)
    text.insert(1.0, content.replace(find, replace))

def change_font_size_selection():
    """Change font size for selected text only"""
    text = current_text_area()
    if not text:
        return
    try:
        if not text.tag_ranges(tk.SEL):
            messagebox.showinfo("No Selection", "Select some text first.")
            return
        size = simpledialog.askinteger("Font Size", "Enter font size (e.g., 12, 18, 24):")
        if not size:
            return
        tag_name = f"size_{size}"
        if not tag_name in text.tag_names():
            text.tag_configure(tag_name, font=(None, size))
        text.tag_add(tag_name, tk.SEL_FIRST, tk.SEL_LAST)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def change_font_size_for_writing(size):
    """Change current writing font size (for next text you type)"""
    text = current_text_area()
    if not text:
        return
    current_font = font.Font(font=text["font"])
    text.configure(font=(current_font.actual("family"), size))

# ========== MENU BAR ==========

menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New Tab", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Close Tab", command=close_tab)
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Find/Replace", command=find_replace)
edit_menu.add_command(label="Change Font Size (Selected Text)", command=change_font_size_selection)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

font_menu = tk.Menu(menu_bar, tearoff=0)
for size in [12, 14, 16, 18, 20, 24, 28, 32]:
    font_menu.add_command(label=f"{size}px", command=lambda s=size: change_font_size_for_writing(s))
menu_bar.add_cascade(label="Font Size", menu=font_menu)

root.config(menu=menu_bar)

# Start with one tab
new_tab("Untitled")

root.mainloop()