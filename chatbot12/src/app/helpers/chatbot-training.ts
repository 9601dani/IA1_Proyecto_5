import * as tf from '@tensorflow/tfjs';

// Vocabulario controlado (palabras clave)
const vocabulary = ["hola", "cómo", "estás", "adiós", "gracias", "bien", "mal"];

// Preprocesar la entrada (convertir las palabras en un vector de 0s y 1s)
function preprocessInput(input: string): number[] {
  const words = input.toLowerCase().split(' '); // Convertir a minúsculas y dividir por palabras
  const vector = new Array(vocabulary.length).fill(0); // Inicializar el vector de 0s

  // Asignar 1 en las posiciones correspondientes del vocabulario
  words.forEach((word) => {
    const index = vocabulary.indexOf(word);
    if (index !== -1) {
      vector[index] = 1; // Marca 1 si la palabra está en el vocabulario
    }
  });

  return vector;
}
// Respuestas posibles
const responsesMap: { [key: number]: string } = {
  0: "¡Hola! ¿Cómo puedo ayudarte?",
  1: "Estoy bien, gracias por preguntar.",
  2: "¡Adiós! Que tengas un buen día.",
  3: "¡De nada! Siempre aquí para ayudarte.",
  4: "Me alegra escuchar que estás bien.",
  5: "Lamento escuchar que estás mal.",
};

// Crear el modelo
function createModel(): tf.Sequential {
  const model = tf.sequential();
  model.add(tf.layers.dense({ units: 16, activation: 'relu', inputShape: [vocabulary.length] })); // Capa densa de entrada
  model.add(tf.layers.dense({ units: 8, activation: 'relu' })); // Capa oculta
  model.add(tf.layers.dense({ units: Object.keys(responsesMap).length, activation: 'softmax' })); // Capa de salida con activación softmax

  model.compile({
    optimizer: 'adam',
    loss: 'categoricalCrossentropy',
    metrics: ['accuracy'],
  });

  return model;
}
async function trainModel(): Promise<void> {
  const model = createModel();

  // Datos de entrada (frases procesadas)
  const inputs = [
    preprocessInput("hola"),
    preprocessInput("cómo estás"),
    preprocessInput("adiós"),
    preprocessInput("gracias"),
    preprocessInput("estoy bien"),
    preprocessInput("estoy mal"),
  ];

  // Etiquetas correspondientes (en formato one-hot encoding)
  const labels = [
    [1, 0, 0, 0, 0, 0], // saludo
    [0, 1, 0, 0, 0, 0], // estado
    [0, 0, 1, 0, 0, 0], // despedida
    [0, 0, 0, 1, 0, 0], // gratitud
    [0, 0, 0, 0, 1, 0], // bien
    [0, 0, 0, 0, 0, 1], // mal
  ];

  const xs = tf.tensor2d(inputs);
  const ys = tf.tensor2d(labels);

  // Entrenar el modelo
  await model.fit(xs, ys, {
    epochs: 100, // Aumentar el número de epochs para mejorar el aprendizaje
    batchSize: 4,
  });

  // Guardar el modelo
  await model.save('localstorage://chatbot-model');
  console.log("Modelo entrenado y guardado.");
}
async function predictResponse(input: string): Promise<string> {
  // Cargar el modelo desde localStorage
  const model = await tf.loadLayersModel('localstorage://chatbot-model');

  // Preprocesar la entrada del usuario
  const processedInput = preprocessInput(input);
  const tensorInput = tf.tensor2d([processedInput], [1, vocabulary.length]);

  // Realizar la predicción
  const prediction = model.predict(tensorInput) as tf.Tensor;
  const predictedIndex = prediction.argMax(-1).dataSync()[0];

  return responsesMap[predictedIndex];
}
export {
  trainModel, predictResponse
}
