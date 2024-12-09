import numpy as np
import pandas as pd
import tensorflow as tf
import pickle
from tensorflow.keras import layers, activations, models, utils
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
import os
import yaml


# Print filenames in the input directory
# for dirname, _, filenames in os.walk('./kaggle/input'):
#     for filename in filenames:
#         print(os.path.join(dirname, filename))

# Directory path for YAML files
dir_path = './kaggle/input/'
files_list = os.listdir(dir_path + os.sep)

# Parse conversations from YAML files
questions, answers = [], []

for filepath in files_list:
    with open(dir_path + os.sep + filepath, 'rb') as file_:
        docs = yaml.safe_load(file_)
        conversations = docs['conversations']
        for con in conversations:
            if len(con) > 2:
                questions.append(con[0])
                replies = con[1:]
                ans = ''
                for rep in replies:
                    ans += ' ' + str(rep)
                answers.append(ans)
            elif len(con) > 1:
                questions.append(con[0])
                answers.append(con[1])

# Preprocessing answers
answers_with_tags = []
for i in range(len(answers)):
    if type(answers[i]) == str:
        answers_with_tags.append(answers[i])
    else:
        questions.pop(i)

answers = []
for i in range(len(answers_with_tags)):
    answers.append('<START> ' + answers_with_tags[i] + ' <END>')

# Tokenization
tokenizer = Tokenizer()
tokenizer.fit_on_texts(questions + answers)
VOCAB_SIZE = len(tokenizer.word_index) + 1

from gensim.models import Word2Vec

vocab = []
for word in tokenizer.word_index:
    vocab.append(word)

def tokenize(sentences):
    tokens_list = []
    vocabulary = []
    for sentence in sentences:
        sentence = sentence.lower()
        sentence = re.sub('[^a-zA-Z]', ' ', sentence)
        tokens = sentence.split()
        vocabulary += tokens
        tokens_list.append(tokens)
    return tokens_list , vocabulary

tokenized_questions = tokenizer.texts_to_sequences(questions)
maxlen_questions = max([len(x) for x in tokenized_questions])
padded_questions = pad_sequences(tokenized_questions , maxlen=maxlen_questions , padding='post')
encoder_input_data = np.array(padded_questions)

print(encoder_input_data.shape)

tokenized_answers = tokenizer.texts_to_sequences(answers)
maxlen_answers = max([len(x) for x in tokenized_answers])
padded_answers = pad_sequences(tokenized_answers , maxlen=maxlen_answers , padding='post')
decoder_input_data = np.array(padded_answers)

print(decoder_input_data.shape)

tokenized_answers = tokenizer.texts_to_sequences(answers)
for i in range(len(tokenized_answers)) :
    tokenized_answers[i] = tokenized_answers[i][1:]
padded_answers = pad_sequences(tokenized_answers , maxlen=maxlen_answers , padding='post')
onehot_answers = utils.to_categorical(padded_answers , VOCAB_SIZE)
decoder_output_data = np.array(onehot_answers)

print(decoder_output_data.shape)

encoder_inputs = tf.keras.layers.Input(shape=(maxlen_questions ,))
encoder_embedding = tf.keras.layers.Embedding(VOCAB_SIZE, 200 , mask_zero=True) (encoder_inputs)
encoder_outputs , state_h , state_c = tf.keras.layers.LSTM(200 , return_state=True)(encoder_embedding)
encoder_states = [ state_h , state_c ]

decoder_inputs = tf.keras.layers.Input(shape=(maxlen_answers , ))
decoder_embedding = tf.keras.layers.Embedding(VOCAB_SIZE, 200 , mask_zero=True) (decoder_inputs)
decoder_lstm = tf.keras.layers.LSTM(200 , return_state=True , return_sequences=True)
decoder_outputs , _ , _ = decoder_lstm (decoder_embedding , initial_state=encoder_states)
decoder_dense = tf.keras.layers.Dense(VOCAB_SIZE , activation=tf.keras.activations.softmax) 
output = decoder_dense (decoder_outputs)

model = tf.keras.models.Model([encoder_inputs, decoder_inputs], output)
model.compile(optimizer=tf.keras.optimizers.RMSprop(), loss='categorical_crossentropy')

model.summary()

model.fit([encoder_input_data , decoder_input_data], decoder_output_data, batch_size=32, epochs=150)


model.save("s2s_model.keras")

metadata = {
    "tokenizer": tokenizer,
    "maxlen_questions": maxlen_questions,
    "maxlen_answers": maxlen_answers
}

with open('tokenizer.pkl', 'wb') as file:
    pickle.dump(metadata, file)
    
print("Modelo guardado como 's2s_model.keras'.")
