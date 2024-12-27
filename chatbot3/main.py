import tkinter as tk
from tkinter import ttk
from train import proccess_input

# Crear la ventana principal
window = tk.Tk()
window.title("Chatbot Grupo 5 - Chatbot")
window.geometry("600x700")
window.configure(bg="#f8f9fa")

# Crear un marco para el título
title_frame = tk.Frame(window, bg="#4a148c", height=60)
title_frame.pack(side="top", fill="x")

title = tk.Label(title_frame, text="Chatbot Grupo 5 - Chatbot12", bg="#4a148c", fg="white", font=("Helvetica", 18, "bold"))
title.pack(pady=15)

# Crear un marco para el área de chat
frame_chat = tk.Frame(window, bg="#ffffff", bd=1, relief="solid")
frame_chat.pack(side="top", fill="both", expand=True, padx=15, pady=(5, 15))

# Área de texto para mostrar los mensajes del chat
text_area = tk.Text(frame_chat, wrap="word", bg="#ffffff", fg="black", font=("Helvetica", 16), state="disabled", padx=10, pady=10)
text_area.pack(side="left", fill="both", expand=True)

# Barra de desplazamiento
scrollbar = ttk.Scrollbar(frame_chat, command=text_area.yview)
scrollbar.pack(side="right", fill="y")
text_area["yscrollcommand"] = scrollbar.set

# Crear un marco para la entrada de texto y el botón
frame_input = tk.Frame(window, bg="#f8f9fa")
frame_input.pack(side="bottom", fill="x", padx=15, pady=(0, 15))

# Entrada de texto
input_text = tk.Entry(frame_input, bg="#ffffff", fg="black", font=("Helvetica", 16), relief="solid", bd=1)
input_text.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=8)

# Botón de enviar
button_send = tk.Button(frame_input, text="Enviar", bg="#4a148c", fg="white", font=("Helvetica", 14, "bold"), width=12, relief="flat")
button_send.pack(side="right")

# Función para crear burbujas de chat
def insert_bubble(text, sender="user"):
    text_area.config(state="normal")

    if sender == "user":
        text_area.insert("end", "\n", "right_padding")
        text_area.insert("end", f"{text}\n", "user")
    else:
        text_area.insert("end", "\n", "left_padding")
        text_area.insert("end", f"{text}\n", "bot")

    text_area.config(state="disabled")
    text_area.see("end")

# Función para enviar un mensaje
def send_message(event=None):
    message = input_text.get()
    if message.strip():
        # Mostrar mensaje del usuario
        insert_bubble(message, sender="user")
        input_text.delete(0, "end")

        # Obtener respuesta del bot
        respuesta = proccess_input(message)

        # Mostrar respuesta del bot
        insert_bubble(respuesta, sender="bot")

# Configuración de estilos para las burbujas
text_area.tag_configure("user", foreground="black",justify="right", font=("Helvetica", 16, "normal"), lmargin1=50, rmargin=10, spacing1=5, spacing3=5)
text_area.tag_configure("bot", foreground="black", justify="left", font=("Helvetica", 16, "normal"), lmargin1=10, rmargin=50, spacing1=5, spacing3=5)
text_area.tag_configure("right_padding", justify="right", spacing1=5, spacing3=5)
text_area.tag_configure("left_padding", justify="left", spacing1=5, spacing3=5)

# Asignar el evento Enter para enviar mensajes
window.bind("<Return>", send_message)
button_send.config(command=send_message)

# Mostrar la ventana
window.mainloop()
