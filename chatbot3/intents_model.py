import json
import pickle
import random
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Dense, Embedding, LSTM, Input, Flatten
from sklearn.preprocessing import LabelEncoder
from unidecode import unidecode
import string

# Definir los conectores a eliminar
CONNECTORS = [
    "y", "and", "que", "that", "o", "or", "u", "or", "pero", "but", "porque", "because",
    "aunque", "although", "si", "if", "cuando", "when", "como", "how", "por", "for", 
    "a", "to", "de", "of", "en", "in", "con", "with", "para", "for", "el", "the", 
    "la", "the", "los", "the", "las", "the", "un", "a", "una", "a", "unos", "some", 
    "unas", "some", "al", "to the", "del", "of the"
]

# Función para limpiar el texto
def clean_text(text):
    text = unidecode(text)
    text = ''.join(char for char in text if char not in string.punctuation)
    words = text.lower().split()
    words = [word for word in words if word not in CONNECTORS]
    return ' '.join(words)

def train_model():
    # Cargar el archivo JSON traducido
    with open('intents.json', 'r', encoding='utf-8') as file:
        intents_data = json.load(file)

    # Preparar los datos
    all_inputs = []
    all_outputs = []
    responses_map = {}

    for intent in intents_data["intents"]:
        tag = intent["tag"]
        patterns = intent["patterns"]
        responses = intent["responses"]

        # Limpiar patrones y mapear respuestas
        for pattern in patterns:
            all_inputs.append(clean_text(pattern))
            all_outputs.append(tag)
        
        responses_map[tag] = responses

    # Tokenización
    tokenizer = Tokenizer(num_words=3000, oov_token="<OOV>")
    tokenizer.fit_on_texts(all_inputs)
    sequences = tokenizer.texts_to_sequences(all_inputs)
    x_data = pad_sequences(sequences)

    # Codificar etiquetas
    label_encoder = LabelEncoder()
    y_data = label_encoder.fit_transform(all_outputs)

    # Parámetros del modelo
    input_length = x_data.shape[1]
    vocab_size = len(tokenizer.word_index) + 1
    output_size = len(label_encoder.classes_)

    # Construcción del modelo
    input_layer = Input(shape=(input_length,))
    embedding_layer = Embedding(vocab_size, 16)(input_layer)
    lstm_layer = LSTM(16, return_sequences=True)(embedding_layer)
    flatten_layer = Flatten()(lstm_layer)
    hidden_layer = Dense(32, activation='relu')(flatten_layer)
    output_layer = Dense(output_size, activation='softmax')(hidden_layer)

    model = Model(input_layer, output_layer)
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Entrenamiento del modelo
    model.fit(x_data, y_data, epochs=200, batch_size=15, verbose=1)

    # Guardar el modelo en formato .keras
    model.save('./chatbot_model.keras')

    # Guardar el tokenizer como archivo .pkl
    with open('./chatbot_tokenizer.pkl', 'wb') as file:
        pickle.dump({'tokenizer': tokenizer, 'max_length': input_length, 'label_encoder': label_encoder}, file)

    # Guardar el responses_map
    with open('./responses_map.pkl', 'wb') as file:
        pickle.dump(responses_map, file)

    print("Modelo entrenado y archivos guardados correctamente.")