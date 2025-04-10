import time
import customtkinter as ctk
import threading

def spinner(duration, label):
    chars = ['⣾','⣽','⣻','⢿','⡿','⣟', '⣯', '⣷']
    #chars = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█', '▇', '▆', '▅', '▄', '▃', '▁']
    #chars = "⡀⡁⡂⡃⡄⡅⡆⡇⡈⡉⡊⡋⡌⡍⡎⡏⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛⡜⡝⡞⡟⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏⢐⢑⢒⢓⢔⢕⢖⢗⢘⢙⢚⢛⢜⢝⢞⢟⢠⢡⢢⢣⢤⢥⢦⢧⢨⢩⢪⢫⢬⢭⢮⢯⢰⢱⢲⢳⢴⢵⢶⢷⢸⢹⢺⢻⢼⢽⢾⢿⣀⣁⣂⣃⣄⣅⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟⣠⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯⣰⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿"
    start_time = time.time()
    while time.time() - start_time < duration:
        for char in chars:
            text = 'Working... ' + char
            label.configure(text=text)
            label.update()  # Force the label to update immediately
            time.sleep(0.1)
    label.configure(text='Done!          ')

def start_spinner():
    duration = 10
    spinner_thread = threading.Thread(target=spinner, args=(duration, label))
    spinner_thread.start()

app = ctk.CTk()
app.title("Spinner Animation")

label = ctk.CTkLabel(app, text="Starting...")
label.pack(padx=20, pady=20)


start_button = ctk.CTkButton(app, text="Start Spinner", command=start_spinner)
start_button.pack(padx=20, pady=10)

app.mainloop()
