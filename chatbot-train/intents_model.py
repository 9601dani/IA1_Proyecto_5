import json
import string
import random
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Dense, Embedding, LSTM, Input, Flatten
from tensorflow.keras.models import Model
from sklearn.preprocessing import LabelEncoder
import tensorflowjs as tfjs

# Cargar el archivo JSON proporcionado
with open('./data-programming.json', 'r', encoding='utf-8') as file:
    intents_data = json.load(file)

# Preparar los datos
all_inputs = []
all_outputs = []
responses_map = {}

for item in intents_data:
    responses_map[item["input"]] = item["output"]
    all_inputs.append(item["input"])
    all_outputs.append(item["input"])  # Usamos los inputs como etiquetas únicas

# Crear DataFrame
data_frame = pd.DataFrame({"inputs": all_inputs, "outputs": all_outputs})
data_frame['inputs'] = data_frame['inputs'].apply(
    lambda sentence: ''.join([char.lower() for char in sentence if char not in string.punctuation])
)

# Tokenización
tokenizer = Tokenizer(num_words=3000)
tokenizer.fit_on_texts(data_frame['inputs'])
sequences = tokenizer.texts_to_sequences(data_frame['inputs'])
x_data = pad_sequences(sequences)

# Codificar etiquetas
label_encoder = LabelEncoder()
y_data = label_encoder.fit_transform(data_frame['outputs'])

# Parámetros del modelo
input_length = x_data.shape[1]
vocab_size = len(tokenizer.word_index) + 1
output_size = len(label_encoder.classes_)

# Construir el modelo
input_layer = Input(shape=(input_length,))
embedding_layer = Embedding(vocab_size, 16)(input_layer)
lstm_layer = LSTM(16, return_sequences=True)(embedding_layer)
flatten_layer = Flatten()(lstm_layer)
hidden_layer = Dense(32, activation='relu')(flatten_layer)
output_layer = Dense(output_size, activation='softmax')(hidden_layer)

model = Model(input_layer, output_layer)
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Entrenar el modelo
model.fit(x_data, y_data, epochs=200, batch_size=15, verbose=1)

# Guardar el modelo y el tokenizer
tfjs.converters.save_keras_model(model, './chatbot_model_js')
max_length = max(len(seq) for seq in sequences)

# Convertir el tokenizer a JSON y agregar max_length
tokenizer_config = json.loads(tokenizer.to_json())
tokenizer_config['config']['word_counts'] = tokenizer.word_counts
tokenizer_config['config']['word_docs'] = tokenizer.word_docs
tokenizer_config['config']['index_word'] = tokenizer.index_word
tokenizer_config['config']['index_docs'] = tokenizer.index_docs
tokenizer_config['config']['word_index'] = tokenizer.word_index
tokenizer_config['max_length'] = max_length

with open('./chatbot_tokenizer.json', 'w') as file:
    json.dump(tokenizer_config, file)

# Chatbot interactivo
print("\nChatbot listo. Escribe 'salir' para terminar.")
print(model.summary())
while True:
    user_input = input("You: ")
    if user_input.lower() == 'salir':
        print("Chatbot: ¡Hasta pronto!")
        break

    # Limpiar y tokenizar input
    cleaned_input = ''.join([char.lower() for char in user_input if char not in string.punctuation])
    sequence_input = tokenizer.texts_to_sequences([cleaned_input])
    padded_input = pad_sequences(sequence_input, maxlen=input_length)

    # Predicción
    prediction = model.predict(padded_input)
    predicted_tag = label_encoder.inverse_transform([np.argmax(prediction)])[0]
    response = random.choice(responses_map[predicted_tag])

    print(f"Chatbot: {response}")
