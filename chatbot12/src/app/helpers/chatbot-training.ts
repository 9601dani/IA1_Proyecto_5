import * as tf from '@tensorflow/tfjs';
import trainingData from './data-programming.json';

// Preprocesar la entrada
function preprocessInput(input: string, vocabulary: string[]): number[] {
  const words = input.toLowerCase().split(' ');
  const vector = new Array(vocabulary.length).fill(0);

  words.forEach((word) => {
    const index = vocabulary.indexOf(word);
    if (index !== -1) {
      vector[index] = 1;
    } else {
      console.warn(`Unknown word: ${word}`);
    }
  });

  return vector;
}

// Seleccionar respuesta al azar
function getRandomResponse(responses: string[]): string {
  const randomIndex = Math.floor(Math.random() * responses.length);
  return responses[randomIndex];
}

// Preprocesar el vocabulario
function generateVocabulary(data: { input: string; output: string[] }[]): string[] {
  const allWords = data
    .map((item) => item.input.toLowerCase().split(' '))
    .reduce((acc, words) => acc.concat(words), []);
  return Array.from(new Set(allWords));
}

// Crear el modelo
function createModel(vocabularyLength: number, outputLength: number): tf.Sequential {
  const model = tf.sequential();
  model.add(tf.layers.dense({ units: 16, activation: 'relu', inputShape: [vocabularyLength] }));
  model.add(tf.layers.dense({ units: 8, activation: 'relu' }));
  model.add(tf.layers.dense({ units: outputLength, activation: 'softmax' }));

  model.compile({
    optimizer: 'adam',
    loss: 'categoricalCrossentropy',
    metrics: ['accuracy'],
  });

  return model;
}

// Entrenar el modelo
async function trainModel(): Promise<void> {
  const vocabulary = generateVocabulary(trainingData);
  const model = createModel(vocabulary.length, trainingData.length);

  const inputs = trainingData.map((data) => preprocessInput(data.input, vocabulary));
  const labels = trainingData.map((_, i) => {
    const labelVector = new Array(trainingData.length).fill(0);
    labelVector[i] = 1;
    return labelVector;
  });

  // Convertir los datos a tensores
  const xs = tf.tensor2d(inputs);
  const ys = tf.tensor2d(labels);

  // Entrenar el modelo
  await model.fit(xs, ys, {
    epochs: 200,
    batchSize: 15,
    shuffle: true,
  });

  await model.save('localstorage://chatbot-model');
  console.log('Modelo entrenado y guardado.');
}

// Predecir la respuesta
async function predictResponse(input: string): Promise<string> {
  const vocabulary = generateVocabulary(trainingData);
  const model = await tf.loadLayersModel('localstorage://chatbot-model');

  const processedInput = preprocessInput(input, vocabulary);
  const tensorInput = tf.tensor2d([processedInput], [1, vocabulary.length]);

  const prediction = model.predict(tensorInput) as tf.Tensor;
  const predictedIndex = prediction.argMax(-1).dataSync()[0];

  const possibleResponses = trainingData[predictedIndex].output;
  return getRandomResponse(possibleResponses);
}

export {
  trainModel,
  predictResponse
};
