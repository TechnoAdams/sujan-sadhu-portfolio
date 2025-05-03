import tkinter as tk
from tkinter import scrolledtext, filedialog, simpledialog
import sys
from io import StringIO
import os
import subprocess
import keyword

# Function to execute Python code and capture output
def execute_code():
    code = code_area.get("1.0", tk.END)  # Get code from the text widget
    
    # Redirect stdout to capture print statements
    output = StringIO()
    sys.stdout = output
    
    try:
        exec(code)  # Execute the code entered in the text area
    except Exception as e:
        output.write(f"Error: {e}")
    
    # Show output in the output_area widget
    result = output.getvalue()
    output_area.config(state=tk.NORMAL)  # Enable editing temporarily
    output_area.delete(1.0, tk.END)
    output_area.insert(tk.END, result)
    output_area.config(state=tk.DISABLED)  # Disable editing again
    sys.stdout = sys.__stdout__  # Reset stdout

# Function to open a file and load its contents into the code area
def open_file():
    filepath = filedialog.askopenfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    if filepath:
        with open(filepath, 'r') as file:
            code = file.read()
            code_area.delete(1.0, tk.END)  # Clear existing text
            code_area.insert(tk.END, code)  # Insert file contents
            execute_code()  # Automatically run the code after opening it

# Function to save the current code to a file
def save_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    if filepath:
        with open(filepath, 'w') as file:
            code = code_area.get("1.0", tk.END)
            file.write(code)
        
        # Once the project is saved, open it in VS Code and show the file name in the editor
        open_in_vs_code(filepath)

# Function to open the saved file in VS Code
def open_in_vs_code(filepath):
    if filepath and os.path.exists(filepath):
        # Check if VS Code is installed and try to open the file
        try:
            subprocess.run(['code', filepath], check=True)
        except FileNotFoundError:
            print("VS Code is not installed or not found in the PATH.")
        
        # Optionally, show the file name in the editor
        filename = os.path.basename(filepath)
        print(f"Opening {filename} in VS Code...")


# Function to clear the code editor
def clear_code():
    code_area.delete(1.0, tk.END)

# Undo function
def undo_action(event=None):
    try:
        code_area.edit_undo()
    except tk.TclError:
        pass

# Redo function
def redo_action(event=None):
    try:
        code_area.edit_redo()
    except tk.TclError:
        pass

def track_text_changes(event=None):
    code_area.edit_separator()

# Function to handle indentation for code
def on_key_release(event):
    code = code_area.get("1.0", tk.END)
    
    # Handle automatic indentation for Python syntax
    if event.keysym == 'Return':
        last_line = code.splitlines()[-2]  # Get the second last line
        if last_line.endswith(':'):  # If last line ends with a colon (Python structure)
            code_area.insert(tk.END, '    ')  # Add 4 spaces indentation for new line (gap)
            return 'break'  # Prevent default action and add the gap

    # Update syntax highlighting
    highlight_syntax()

# Syntax highlighting function
def highlight_syntax():
    code = code_area.get("1.0", tk.END)
    code_area.tag_remove("keyword", "1.0", tk.END)  # Remove previous tags
    code_area.tag_remove("function", "1.0", tk.END)
    code_area.tag_remove("string", "1.0", tk.END)
    
    # Highlight keywords
    for word in keyword.kwlist:
        start_pos = "1.0"
        while True:
            start_pos = code_area.search(rf"\b{word}\b", start_pos, stopindex=tk.END, regexp=True)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(word)}c"
            code_area.tag_add("keyword", start_pos, end_pos)
            code_area.tag_configure("keyword", foreground="blue")
            start_pos = end_pos
    
    # Highlight function definitions
    start_pos = "1.0"
    while True:
        start_pos = code_area.search(r"\bdef\b", start_pos, stopindex=tk.END, regexp=True)
        if not start_pos:
            break
        end_pos = f"{start_pos}+3c"  # Move over the "def" keyword
        code_area.tag_add("function", start_pos, end_pos)
        code_area.tag_configure("function", foreground="green")
        start_pos = end_pos
    
    # Highlight string literals
    start_pos = "1.0"
    while True:
        start_pos = code_area.search(r"\".*?\"|'.*?'", start_pos, stopindex=tk.END, regexp=True)
        if not start_pos:
            break
        end_pos = code_area.index(f"{start_pos}+{len(code_area.get(start_pos, start_pos + '+10c'))}c")
        code_area.tag_add("string", start_pos, end_pos)
        code_area.tag_configure("string", foreground="red")
        start_pos = end_pos

# Function to download assets (e.g., libraries like pygame, opengl)
def download_assets():
    # Create a new window for downloading assets
    download_window = tk.Toplevel(root)
    download_window.title("Download Assets")

    # Set the size of the window
    download_window.geometry("400x300")

    # Add a label
    label = tk.Label(download_window, text="Enter asset/library name to download (e.g., pygame):")
    label.pack(padx=10, pady=10)

    # Create an input field for entering library names
    asset_name_entry = tk.Entry(download_window, width=40)
    asset_name_entry.pack(padx=10, pady=10)

    # Function to install the asset via pip
    def install_asset():
        asset_name = asset_name_entry.get().strip()
        if asset_name:
            # Install the asset via pip
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", asset_name], check=True)
                status_label.config(text=f"Asset '{asset_name}' installed successfully!", fg="green")
            except subprocess.CalledProcessError:
                status_label.config(text=f"Failed to install '{asset_name}'.", fg="red")
    
    # Button to install the asset
    install_button = tk.Button(download_window, text="Download", command=install_asset)
    install_button.pack(pady=10)

    # Label to show installation status
    status_label = tk.Label(download_window, text="", fg="black")
    status_label.pack(padx=10, pady=10)

# Create the main window
root = tk.Tk()
root.title("Simple Python IDE")

# Set window size
root.geometry("600x500")

# Create a Menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create "File" menu with Open, Save, and Assets options
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Assets", command=download_assets)  # New option for downloading assets

# Create "Edit" menu with Clear option
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=undo_action, accelerator="Ctrl+Z")
edit_menu.add_command(label="Redo", command=redo_action, accelerator="Ctrl+Shift+Z")
edit_menu.add_command(label="Clear", command=clear_code, accelerator="Ctrl+X")  # New "Clear" Option

# Create a Text widget for code input
code_area = scrolledtext.ScrolledText(root, width=70, height=15, wrap=tk.WORD, undo=True, autoseparators=False, maxundo=-1)
code_area.pack(padx=10, pady=10)

# Bind key events to track changes for better undo/redo
code_area.bind("<KeyPress>", track_text_changes)

# Bind keyboard shortcuts
root.bind("<Control-z>", undo_action)  # Ctrl + Z for Undo
root.bind("<Control-Z>", undo_action)  # Support for Shift + Z too
root.bind("<Control-Shift-Z>", redo_action)  # Ctrl + Shift + Z for Redo
root.bind("<Control-x>", lambda event: clear_code())  # Ctrl + X for Clear

# Bind the key release event to handle indentation
code_area.bind("<KeyRelease>", on_key_release)

# Create a button to execute the code
execute_button = tk.Button(root, text="Run Code", command=execute_code)
execute_button.pack(pady=5)

# Create a Text widget for showing output
output_area = scrolledtext.ScrolledText(root, width=70, height=10)
output_area.pack(padx=10, pady=10)

# Disable editing in the output area
output_area.config(state=tk.DISABLED)

# Start the main event loop
root.mainloop()





