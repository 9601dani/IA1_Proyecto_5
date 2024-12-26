import tkinter as tk
from tkinter import ttk

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Chatbot Grupo 5 - Chatbot")
ventana.geometry("800x600")

# Crear un marco para el título
frame_titulo = tk.Frame(ventana, bg="#283593", height=50)
frame_titulo.pack(side="top", fill="x")

titulo = tk.Label(frame_titulo, text="Chatbot Grupo 5 - Chatbot12", bg="#283593", fg="white", font=("Helvetica", 16))
titulo.pack(pady=10)

# Crear un marco para el área de chat
frame_chat = tk.Frame(ventana, bg="white", bd=1, relief="solid")
frame_chat.pack(side="top", fill="both", expand=True, padx=10, pady=10)

# Área de texto para mostrar los mensajes del chat
text_area = tk.Text(frame_chat, wrap="word", bg="white", fg="black", font=("Helvetica", 12), state="disabled")
text_area.pack(side="left", fill="both", expand=True, padx=5, pady=5)

# Barra de desplazamiento
scrollbar = ttk.Scrollbar(frame_chat, command=text_area.yview)
scrollbar.pack(side="right", fill="y")
text_area["yscrollcommand"] = scrollbar.set

# Crear un marco para la entrada de texto y el botón
frame_input = tk.Frame(ventana, bg="white")
frame_input.pack(side="bottom", fill="x", padx=10, pady=5)

# Entrada de texto
entrada_texto = tk.Entry(frame_input, bg="white", fg="black", font=("Helvetica", 12))
entrada_texto.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=5)

# Botón para enviar mensaje
boton_enviar = tk.Button(frame_input, text="Enviar", bg="#283593", fg="white", font=("Helvetica", 12), width=10)
boton_enviar.pack(side="right", padx=5, pady=5)


# Función para enviar el mensaje
def enviar_mensaje(event=None):
    mensaje = entrada_texto.get()
    if mensaje.strip():
        text_area.config(state="normal")
        text_area.insert("end", f"Tú: {mensaje}\n")
        text_area.config(state="disabled")
        text_area.see("end")
        entrada_texto.delete(0, "end")


# Evento del boton enviar
ventana.bind("<Return>", enviar_mensaje)
boton_enviar.config(command=enviar_mensaje)

# Ejecutar la ventana
ventana.mainloop()
