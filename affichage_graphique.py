import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Tkinter Dark Theme")
root.geometry("600x400")
root.configure(bg="#2b2b2b")  # Dark background

# Apply a dark theme using ttk styles
style = ttk.Style()
style.theme_use("clam")  # Use a theme that allows custom styles

# Define custom colors
bg_color = "#2b2b2b"  # Main background
frame_color = "#3c3f41"  # Frame background
text_color = "white"
button_bg = "#444"
button_hover = "#666"

# Configure frame and label styles
style.configure("TFrame", background=bg_color)
style.configure("TLabel", background=frame_color, foreground=text_color, padding=10)
style.configure("TEntry", fieldbackground="#444", foreground=text_color)

# Configure button styles (prevent white highlight)
style.configure(
    "TButton",
    background=button_bg,
    foreground=text_color,
    borderwidth=1,
    focuscolor=button_bg,  # Prevents white focus
    relief="flat"
)
style.map("TButton", 
    background=[("active", button_hover), ("pressed", "#555")],
    foreground=[("disabled", "gray")]
)

# Configure Checkbutton & Radiobutton styles (prevent white selection)
style.configure(
    "TCheckbutton",
    background=bg_color,
    foreground=text_color,
    indicatorcolor=button_bg,
    focuscolor=button_bg  # Prevents highlight
)
style.map("TCheckbutton",
    background=[("active", button_hover)],
    foreground=[("selected", text_color)]
)

style.configure(
    "TRadiobutton",
    background=bg_color,
    foreground=text_color,
    focuscolor=button_bg  # Prevents highlight
)
style.map("TRadiobutton",
    background=[("active", button_hover)],
    foreground=[("selected", text_color)]
)

# Sidebar
sidebar = ttk.Frame(root, width=150, style="TFrame")
sidebar.pack(side="left", fill="y", padx=10, pady=10)

ttk.Button(sidebar, text="Button 1", style="TButton").pack(pady=10)
ttk.Button(sidebar, text="Button 2", style="TButton").pack(pady=10)
ttk.Button(sidebar, text="Button 3", style="TButton").pack(pady=10)

# Main content area
main_frame = ttk.Frame(root, style="TFrame")
main_frame.pack(expand=True, fill="both", padx=10, pady=10)

label = ttk.Label(main_frame, text="Label: Lorem ipsum dolor sit amet...", style="TLabel")
label.pack(pady=10)

# Sliders
slider1 = ttk.Scale(main_frame, from_=0, to=100)
slider1.pack(pady=5, fill="x")

slider2 = ttk.Scale(main_frame, from_=0, to=100)
slider2.pack(pady=5, fill="x")

# Checkboxes
checkbox1 = ttk.Checkbutton(main_frame, text="Disabled CheckBox", state="disabled", style="TCheckbutton")
checkbox1.pack(pady=5)

checkbox2 = ttk.Checkbutton(main_frame, text="CheckBox", style="TCheckbutton")
checkbox2.pack(pady=5)

# Radio buttons
# Variable to store selected radio button value
selected_radio = tk.StringVar(value="Option1")  # Default value

# Radio buttons (grouped by using the same variable)
radio1 = ttk.Radiobutton(main_frame, text="Option 1", variable=selected_radio, value="Option1", style="TRadiobutton")
radio1.pack(anchor="w")

radio2 = ttk.Radiobutton(main_frame, text="Option 2", variable=selected_radio, value="Option2", style="TRadiobutton")
radio2.pack(anchor="w")

radio3 = ttk.Radiobutton(main_frame, text="Option 3", variable=selected_radio, value="Option3", style="TRadiobutton")
radio3.pack(anchor="w")


# Entry field
entry = ttk.Entry(main_frame)
entry.pack(pady=10, fill="x")

# Buttons
button1 = ttk.Button(main_frame, text="Button", style="TButton")
button1.pack(pady=5)

button2 = ttk.Button(main_frame, text="Disabled Button", state="disabled", style="TButton")
button2.pack(pady=5)

# Run the application
root.mainloop()

