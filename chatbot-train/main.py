
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# Cargar el modelo completo
inf_model = tf.keras.models.load_model('s2s_model.keras')

# Cargar el tokenizer y los metadatos
with open('tokenizer.pkl', 'rb') as file:
    metadata = pickle.load(file)

tokenizer = metadata["tokenizer"]
maxlen_questions = metadata["maxlen_questions"]
maxlen_answers = metadata["maxlen_answers"]

# Crear el modelo del codificador
encoder_inputs = inf_model.input[0]  # Primera entrada del modelo
encoder_outputs, state_h_enc, state_c_enc = inf_model.layers[4].output
encoder_states = [state_h_enc, state_c_enc]
encoder_model = tf.keras.models.Model(encoder_inputs, encoder_states)

# Crear el modelo del decodificador
decoder_inputs = inf_model.input[1]  # Segunda entrada del modelo
decoder_state_input_h = tf.keras.layers.Input(shape=(200,), name="input_3")  # Tamaño de la capa LSTM
decoder_state_input_c = tf.keras.layers.Input(shape=(200,), name="input_4")
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]

decoder_embedding = inf_model.layers[3](decoder_inputs)
decoder_lstm = inf_model.layers[5]
decoder_outputs, state_h, state_c = decoder_lstm(
    decoder_embedding, initial_state=decoder_states_inputs
)
decoder_dense = inf_model.layers[6]
decoder_outputs = decoder_dense(decoder_outputs)
decoder_states = [state_h, state_c]

decoder_model = tf.keras.models.Model(
    [decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states
)

def preprocess_input(input_sentence, tokenizer, maxlen_questions):
    tokens = input_sentence.lower().split()
    tokens_list = []
    for word in tokens:
        tokens_list.append(tokenizer.word_index[word])
    return pad_sequences([tokens_list], maxlen=maxlen_questions, padding='post')

tests = ['algo interesante', 'como esta tu salud', 'buen dia', 'me siento mal']

for test_sentence in tests:
    states_values = encoder_model.predict(preprocess_input(test_sentence.lower(), tokenizer, maxlen_questions))

    empty_target_seq = np.zeros((1, 1))
    empty_target_seq[0, 0] = tokenizer.word_index['start']
    stop_condition = False
    decoded_translation = ''

    while not stop_condition:
        # Predecir la siguiente palabra
        dec_outputs, h, c = decoder_model.predict([empty_target_seq] + states_values)
        sampled_word_index = np.argmax(dec_outputs[0, -1, :])
        sampled_word = None

        for word, index in tokenizer.word_index.items():
            if sampled_word_index == index:
                decoded_translation += f' {word}'
                sampled_word = word

        if sampled_word == 'end' or len(decoded_translation.split()) > maxlen_answers:
            stop_condition = True

        # Actualizar la secuencia de entrada y los estados
        empty_target_seq = np.zeros((1, 1))
        empty_target_seq[0, 0] = sampled_word_index
        states_values = [h, c]

    print(f'Human: {test_sentence}')
    print(f'Bot: {decoded_translation.split(" end")[0]}')
    print('-' * 25)
