import { ref } from 'vue';
import { getModel, getTokenizer, getResponsesMap } from '../helpers/modelService'
import * as tf from '@tensorflow/tfjs';

export const useChat = () => {
  const messages = ref([]);

  const predict = async (input) => {
    const model = getModel();
    const tokenizer = getTokenizer();
    const responsesMap = getResponsesMap();

    if (!model || !tokenizer || !responsesMap) {
      console.error('Modelo o tokenizer o responsesMap no están cargados.');
      return;
    }
    const wordIndex = JSON.parse(tokenizer['config']['word_index']);

    const cleanedInput = input.toLowerCase();
    const sequenceInput = textToSequences([cleanedInput], wordIndex);
    const paddedInput = tf.pad(
      tf.tensor2d(sequenceInput),
      [[0, 0], [0, Math.max(0, 5. - sequenceInput[0].length)]]
    );

    const prediction = model.predict(paddedInput);
    console.log(prediction);
    const predictedIndex = prediction.argMax(1).dataSync()[0];
    const predictedTag = Object.keys(responsesMap)[predictedIndex];
    const responses = responsesMap[predictedTag];
    return responses[Math.floor(Math.random() * responses.length)] || "No entendí la pregunta.";
  };

  const cleanText = (input) => {
    return input
      .toLowerCase()
      .replace(/[^\w\s]/gi, '');
  };

  const textToSequences = (input, wordIndex) => {
    return input.map((text) =>
      text.split(' ').map((word) => wordIndex[word] || 0)
    );
  };

  const getHerResponse = async (text) => {
    const response = await predict(text);
    const data = { answer: response };
    return data;
  };

  const onMessage = async (text) => {
    if (text.length === 0) return;

    // Add user's message
    messages.value.push({
      id: new Date().getTime(),
      itsMine: true,
      message: text,
    });

    // Fetch response from the API
    const { answer } = await getHerResponse(text);

    // Add the response message
    messages.value.push({
      id: new Date().getTime(),
      itsMine: false,
      message: answer,
    });
  };

  return {
    // Properties
    messages,
    // Methods
    onMessage,
  };
};
