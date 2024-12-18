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

# Cargar archivo intents.json
with open('./intents.json', 'r', encoding='utf-8') as file:
    intents_data = json.load(file)

# Preparar los datos
all_tags = []
all_patterns = []
responses_map = {}

for intent in intents_data['intents']:
    responses_map[intent['tag']] = intent['responses']
    for pattern in intent['patterns']:
        all_patterns.append(pattern)
        all_tags.append(intent['tag'])

# Crear DataFrame
data_frame = pd.DataFrame({"patterns": all_patterns, "tags": all_tags})
data_frame['patterns'] = data_frame['patterns'].apply(
    lambda sentence: ''.join([char.lower() for char in sentence if char not in string.punctuation])
)

# Tokenización
tokenizer = Tokenizer(num_words=3000)
tokenizer.fit_on_texts(data_frame['patterns'])
sequences = tokenizer.texts_to_sequences(data_frame['patterns'])
x_data = pad_sequences(sequences)

# Codificar etiquetas
label_encoder = LabelEncoder()
y_data = label_encoder.fit_transform(data_frame['tags'])

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
model.fit(x_data, y_data, epochs=100, batch_size=32, verbose=1)

# Guardar el modelo y el tokenizer
tfjs.converters.save_keras_model(model, './chatbot_model_js')
with open('./chatbot_tokenizer.json', 'w') as file:
    json.dump(json.loads(tokenizer.to_json()), file)

# Chatbot interactivo
print("\nChatbot listo. Escribe 'salir' para terminar.")
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
    print(prediction)
    predicted_tag = label_encoder.inverse_transform([np.argmax(prediction)])[0]
    response = random.choice(responses_map[predicted_tag])

    print(f"Chatbot: {response}")
