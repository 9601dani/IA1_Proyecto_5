import pickle
import random
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from intents_model import clean_text

# Cargar el modelo y el tokenizer
def load_chatbot_resources():
    model = load_model('./chatbot_model.keras')

    with open('./chatbot_tokenizer.pkl', 'rb') as file:
        tokenizer_data = pickle.load(file)
        tokenizer = tokenizer_data['tokenizer']
        max_length = tokenizer_data['max_length']
        label_encoder = tokenizer_data['label_encoder']

    with open('./responses_map.pkl', 'rb') as file:
        responses_map = pickle.load(file)

    return model, tokenizer, max_length, responses_map, label_encoder

def process_input(input_text, model, tokenizer, max_length, responses_map, label_encoder):
    # Limpieza y tokenización del input
    cleaned_input = clean_text(input_text)
    sequence_input = tokenizer.texts_to_sequences([cleaned_input])
    padded_input = pad_sequences(sequence_input, maxlen=max_length)

    # Predicción
    prediction = model.predict(padded_input)
    predicted_tag = label_encoder.inverse_transform([np.argmax(prediction)])[0]

    # Seleccionar una respuesta aleatoria
    response = random.choice(responses_map[predicted_tag])

    return response
