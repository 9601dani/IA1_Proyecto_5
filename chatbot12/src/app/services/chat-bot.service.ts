import { Injectable } from '@angular/core';
import * as tf from '@tensorflow/tfjs';


@Injectable({
  providedIn: 'root'
})
export class ChatBotService {

  encoderModel: tf.LayersModel;
  decoderModel: tf.LayersModel;
  tokenizer: any;
  maxLenAnswers: number;
  maxLenQuestions: number;

  constructor() { }

  async loadModel() {

    this.encoderModel = await tf.loadLayersModel('/assets/encoder/model.json');
    this.decoderModel = await tf.loadLayersModel('/assets/decoder/model.json');

    const tokenizerData = await fetch('/assets/tokenizer.json').then(m => m.json());
    this.tokenizer = tokenizerData.tokenizer;
    this.maxLenAnswers = tokenizerData.maxlen_answers;
    this.maxLenQuestions = tokenizerData.maxlen_questions;
  }

  async createEncoderModel(model: tf.LayersModel): Promise<tf.LayersModel> {
    const encoderInputs = model.input;

    const lstmLayer = model.getLayer(null, 4);
    const lstmOutputs = lstmLayer.output as tf.SymbolicTensor | tf.SymbolicTensor[];

    if (Array.isArray(lstmOutputs)) {
      const [encoderOutputs, stateH, stateC] = lstmOutputs;

      const encoderModel = tf.model({
        inputs: encoderInputs,
        outputs: [stateH, stateC],
      });

      return encoderModel;
    } else {
      throw new Error('La capa LSTM no devolvió múltiples salidas.');
    }
  }

  async createDecoderModel(model: tf.LayersModel): Promise<tf.LayersModel> {
    const decoderInputs = tf.input({ shape: [null], name: "decoder_inputs" }); // input_1 en Python

    const decoderStateInputH = tf.input({ shape: [200], name: "input_3" }); // h del estado inicial
    const decoderStateInputC = tf.input({ shape: [200], name: "input_4" }); // c del estado inicial
    const decoderStatesInputs = [decoderStateInputH, decoderStateInputC];

    const decoderEmbeddingLayer = model.getLayer(null, 3); // Embedding layer
    const decoderEmbedding = decoderEmbeddingLayer.apply(decoderInputs) as tf.SymbolicTensor;

    const decoderLstmLayer = model.getLayer(null, 5); // LSTM layer
    const lstmOutputs = decoderLstmLayer.apply([decoderEmbedding, ...decoderStatesInputs]) as tf.SymbolicTensor[];

    const [decoderOutputs, stateH, stateC] = lstmOutputs;

    const decoderDenseLayer = model.getLayer(null, 6); // Dense layer
    const decoderOutputsFinal = decoderDenseLayer.apply(decoderOutputs) as tf.SymbolicTensor;

    const decoderStates = [stateH, stateC];

    const decoderModel = tf.model({
      inputs: [decoderInputs, ...decoderStatesInputs], // Entradas: secuencia y estados iniciales
      outputs: [decoderOutputsFinal, ...decoderStates], // Salidas: predicciones y nuevos estados
    });

    return decoderModel;
  }

  preprocessInput(inputSentence: string): tf.Tensor2D {
    const tokens = inputSentence.toLowerCase().split(' ');

    const tokensList = tokens.map(word => this.tokenizer.word_index[word] || 0);

    const paddedTokens = new Array(this.maxLenQuestions).fill(0);
    tokensList.slice(0, this.maxLenQuestions).forEach((token, index) => {
      paddedTokens[index] = token;
    });

    return tf.tensor2d([paddedTokens], [1, this.maxLenQuestions]);
  }

  async decodeSequence(sentence: string): Promise<string> {
    const inputTensor = this.preprocessInput(sentence);

    const statesValues = this.encoderModel.predict(inputTensor) as tf.Tensor[];


    let emptyTargetSeq = tf.tensor2d([[this.tokenizer.word_index['start']]], [1, 1]);

    let paddedTargetSeq = tf.pad(emptyTargetSeq, [[0, 0], [0, this.maxLenAnswers - emptyTargetSeq.shape[1]]], 0);

    let stopCondition = false;
    let decodedTranslation = '';

    while (!stopCondition) {
      console.log('first padded ->', paddedTargetSeq)
      const [decOutputs, stateH, stateC] = this.decoderModel.predict([paddedTargetSeq, ...statesValues]) as tf.Tensor2D[];

      console.log('decoutputs ----->', decOutputs, stateH, stateC);
      const sampledWordIndexArray = await decOutputs.argMax(-1).data();
      console.log('array -------->', sampledWordIndexArray)
      const sampledWordIndex = sampledWordIndexArray[0];

      // Buscar la palabra correspondiente al índice más probable
      let sampledWord = null;
      for (const [word, index] of Object.entries(this.tokenizer.word_index)) {
        if (sampledWordIndex === index) {
          decodedTranslation += ` ${word}`;
          sampledWord = word;
          break; // Salir del bucle cuando se encuentra la palabra
        }
      }
      console.log('sampled_word ->', sampledWord);

      // Verificar la condición de parada
      if (sampledWord === 'end' || decodedTranslation.split(' ').length > this.maxLenAnswers || sampledWordIndex === 0) {
        stopCondition = true;
      }

      // Actualizar la secuencia de entrada del decodificador
      emptyTargetSeq.dispose(); // Liberar el tensor anterior
      emptyTargetSeq = tf.tensor2d([[sampledWordIndex]], [1, 1], 'int32');
      paddedTargetSeq.dispose(); // Liberar el tensor anterior
      paddedTargetSeq = tf.pad(emptyTargetSeq, [[0, 0], [0, this.maxLenAnswers - emptyTargetSeq.shape[1]]], 0);

      // Actualizar los estados del decodificador
      statesValues[0].dispose();
      statesValues[1].dispose();
      statesValues[0] = stateH;
      statesValues[1] = stateC;

      // Liberar tensores temporales
      decOutputs.dispose();
    }

    return decodedTranslation.replace(' end', '').trim();
  }
}
