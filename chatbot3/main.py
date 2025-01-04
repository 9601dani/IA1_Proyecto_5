import tkinter as tk
from tkinter import ttk
from process_input import process_input, load_chatbot_resources

# Cargar el modelo
model, tokenizer, max_length, responses_map, label_encoder = load_chatbot_resources()

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

# Crear un marco para la entrada de texto y los botones
frame_input = tk.Frame(window, bg="#f8f9fa")
frame_input.pack(side="bottom", fill="x", padx=15, pady=(0, 15))

# Entrada de texto
input_text = tk.Entry(frame_input, bg="#ffffff", fg="black", font=("Helvetica", 16), relief="solid", bd=1)
input_text.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=8)

# Botón de enviar
button_send = tk.Button(frame_input, text="Enviar", bg="#4a148c", fg="white", font=("Helvetica", 14, "bold"), width=12, relief="flat")
button_send.pack(side="right")

# Botón de limpiar
button_clear = tk.Button(frame_input, text="Limpiar", bg="#dc3545", fg="white", font=("Helvetica", 14, "bold"), width=12, relief="flat")
button_clear.pack(side="right", padx=(0, 10))

# Configuración de estilos mejorados sin padx ni pady
text_area.tag_configure("user", foreground="black", justify="right",
                        font=("Helvetica", 14, "normal"), lmargin1=50, rmargin=10,
                        spacing1=10, spacing3=10, background="#d1e7ff", borderwidth=2,
                        relief="solid")
text_area.tag_configure("bot", foreground="black", justify="left",
                        font=("Helvetica", 14, "normal"), lmargin1=10, rmargin=50,
                        spacing1=10, spacing3=10, background="#e9ecef", borderwidth=2,
                        relief="solid")

# Función para insertar burbujas con padding simulado
def insert_bubble(text, sender="user"):
    text_area.config(state="normal")

    # Agregar padding simulado con espacios
    padded_text = f"   {text}   "  # Espacios antes y después del texto

    if sender == "user":
        text_area.insert("end", "\n", "right_padding")
        text_area.insert("end", f"{padded_text}\n", "user")  # Burbuja del usuario
    else:
        text_area.insert("end", "\n", "left_padding")
        text_area.insert("end", f"{padded_text}\n", "bot")  # Burbuja del bot

    text_area.insert("end", "\n\n")  # Espaciado entre mensajes
    text_area.config(state="disabled")
    text_area.see("end")

# Función para enviar un mensaje
def send_message(event=None):
    message = input_text.get()
    if message.strip():
        insert_bubble(message, sender="user")
        input_text.delete(0, "end")

        respuesta = process_input(message, model, tokenizer, max_length, responses_map, label_encoder)

        insert_bubble(respuesta, sender="bot")

# Función para limpiar el área de texto
def clear_text_area():
    text_area.config(state="normal")
    text_area.delete("1.0", "end")
    text_area.config(state="disabled")

# Asignar el evento Enter para enviar mensajes
window.bind("<Return>", send_message)
button_send.config(command=send_message)
button_clear.config(command=clear_text_area)

# Mostrar la ventana
window.mainloop()
