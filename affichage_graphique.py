import customtkinter as ctk  # Make sure to install it with `pip install customtkinter`

# Configure CustomTkinter appearance
ctk.set_appearance_mode("dark")  # Light, Dark, or System
ctk.set_default_color_theme("dark-blue")  # You can change to "blue" or "green"

# Main App Window
root = ctk.CTk()
root.geometry("600x400")
root.title("CustomTkinter Dark UI")

# Sidebar
sidebar = ctk.CTkFrame(root, width=150, corner_radius=20)
sidebar.pack(side="left", fill="y", padx=10, pady=10)

ctk.CTkButton(sidebar, text="CTkButton 1", corner_radius=20).pack(pady=10)
ctk.CTkButton(sidebar, text="CTkButton 2", corner_radius=20).pack(pady=10)
ctk.CTkButton(sidebar, text="CTkButton 3", corner_radius=20).pack(pady=10)

# Main content area
main_frame = ctk.CTkFrame(root, corner_radius=20)
main_frame.pack(expand=True, fill="both", padx=10, pady=10)

label = ctk.CTkLabel(main_frame, text="CTkLabel: Lorem ipsum dolor sit...", fg_color=("gray20", "gray30"), corner_radius=10)
label.pack(pady=10, fill="x", padx=10)

# Sliders
slider1 = ctk.CTkSlider(main_frame, from_=0, to=100)
slider1.pack(pady=5, fill="x", padx=10)

slider2 = ctk.CTkSlider(main_frame, from_=0, to=100)
slider2.pack(pady=5, fill="x", padx=10)

# Checkboxes
checkbox1 = ctk.CTkCheckBox(main_frame, text="CheckBox Disabled", state="disabled", corner_radius=10)
checkbox1.pack(pady=5)

checkbox2 = ctk.CTkCheckBox(main_frame, text="CTkCheckBox", corner_radius=10)
checkbox2.pack(pady=5)

# Radio Buttons (Only one can be selected)
selected_radio = ctk.StringVar(value="Option1")

radio_frame = ctk.CTkFrame(main_frame, corner_radius=10)
radio_frame.pack(pady=10)

radio1 = ctk.CTkRadioButton(radio_frame, text="CTkRadioButton 1", variable=selected_radio, value="Option1", corner_radius=10)
radio1.pack(anchor="w")

radio2 = ctk.CTkRadioButton(radio_frame, text="CTkRadioButton 2", variable=selected_radio, value="Option2", corner_radius=10)
radio2.pack(anchor="w")

radio3 = ctk.CTkRadioButton(radio_frame, text="CTkRadioButton 3", variable=selected_radio, value="Option3", corner_radius=10)
radio3.pack(anchor="w")

# Entry field
entry = ctk.CTkEntry(main_frame, placeholder_text="Enter text...", corner_radius=20)
entry.pack(pady=10, fill="x", padx=10)

# Buttons
button1 = ctk.CTkButton(main_frame, text="CTkButton", corner_radius=20)
button1.pack(pady=5)

button2 = ctk.CTkButton(main_frame, text="Disabled Button", state="disabled", corner_radius=20)
button2.pack(pady=5)

# Switches
switch = ctk.CTkSwitch(main_frame, text="CTkSwitch", corner_radius=10)
switch.pack(pady=5)

dark_mode_switch = ctk.CTkSwitch(main_frame, text="Dark Mode", corner_radius=10, command=lambda: ctk.set_appearance_mode("dark" if dark_mode_switch.get() else "light"))
dark_mode_switch.pack(pady=5)

# Run the application
root.mainloop()

