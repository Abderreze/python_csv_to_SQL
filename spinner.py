import time
import customtkinter as ctk
import threading
import sys

def rainbow_spinner(duration, label):
    chars = ['⣾','⣽','⣻','⢿','⡿','⣟', '⣯', '⣷']
    #chars = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█', '▇', '▆', '▅', '▄', '▃', '▁']
    #chars = "⡀⡁⡂⡃⡄⡅⡆⡇⡈⡉⡊⡋⡌⡍⡎⡏⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛⡜⡝⡞⡟⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏⢐⢑⢒⢓⢔⢕⢖⢗⢘⢙⢚⢛⢜⢝⢞⢟⢠⢡⢢⢣⢤⢥⢦⢧⢨⢩⢪⢫⢬⢭⢮⢯⢰⢱⢲⢳⢴⢵⢶⢷⢸⢹⢺⢻⢼⢽⢾⢿⣀⣁⣂⣃⣄⣅⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟⣠⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯⣰⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿"
    colors = [
        "\033[91m",  # Red
        "\033[93m",  # Yellow
        "\033[92m",  # Green
        "\033[96m",  # Cyan
        "\033[94m",  # Blue
        "\033[95m",  # Magenta
    ]
    reset_color = "\033[0m"
    start_time = time.time()
    color_index = 0
    while time.time() - start_time < duration:
        for char in chars:
            color = colors[color_index % len(colors)]
            text = 'Working... ' + color + char + reset_color
            label.configure(text=text)
            label.update()  # Force the label to update immediately
            time.sleep(0.1)
            color_index = (color_index + 1) % len(colors)
    label.configure(text='Done!          ')

def start_spinner():
    duration = 10
    spinner_thread = threading.Thread(target=rainbow_spinner, args=(duration, label))
    spinner_thread.start()

app = ctk.CTk()
app.title("Spinner Animation")

label = ctk.CTkLabel(app, text="Starting...")
label.pack(padx=20, pady=20)


start_button = ctk.CTkButton(app, text="Start Spinner", command=start_spinner)
start_button.pack(padx=20, pady=10)

app.mainloop()
