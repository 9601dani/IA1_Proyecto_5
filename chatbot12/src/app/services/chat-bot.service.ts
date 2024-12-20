import { Injectable } from '@angular/core';
import * as tf from '@tensorflow/tfjs';


@Injectable({
  providedIn: 'root'
})
export class ChatBotService {

  private model: tf.LayersModel | null = null;
  private tokenizer: any = null;
  private responsesMap: { [key: string]: string[] } | null = null;

  constructor() { }

  async loadModel() {

    if (!this.model || !this.tokenizer || !this.responsesMap) {
      try {
        // Cargar el modelo
        this.model = await tf.loadLayersModel('assets/intents_model/model.json');

        const tokenizerResponse = await fetch('assets/intents_model/chatbot_tokenizer.json');
        this.tokenizer = await tokenizerResponse.json();

        const intentsResponse = await fetch('assets/intents_model/data-programming.json');
        const intentsData: any[] = await intentsResponse.json();

        // Crear el mapa de respuestas
        this.responsesMap = {};
        intentsData.forEach((intent) => {
          this.responsesMap![intent.input] = intent.output;
        });

        console.log('Modelo, tokenizer y respuestas cargados correctamente.');
      } catch (error) {
        console.error('Error al cargar el modelo o tokenizer:', error);
      }
    }
  }

  async predict(input: string): Promise<string> {
    if (!this.model || !this.tokenizer || !this.responsesMap) {
      throw new Error('El modelo, tokenizer o mapa de respuestas no están cargados.');
    }

    // Procesar texto de entrada
    const cleanedInput = this.cleanText(input);

    // Convertir texto en secuencias
    const wordIndex = this.tokenizer['config']['word_index'];
    const sequenceInput = this.textToSequences([cleanedInput], wordIndex);

    // Realizar padding
    const maxLength = this.tokenizer['max_length'] || 20; // Valor predeterminado si no está definido
    const paddedInput = this.padSequences(sequenceInput, maxLength);

    // Crear tensor a partir de la secuencia
    const tensorInput = tf.tensor2d(paddedInput);

    // Realizar predicción
    const prediction = this.model.predict(tensorInput) as tf.Tensor<tf.Rank>;
    const predictedIndex = (await prediction.argMax(1).data())[0];

    // Obtener el tag predicho y la respuesta correspondiente
    const predictedTag = Object.keys(this.responsesMap)[predictedIndex];
    const responses = this.responsesMap[predictedTag];
    return responses[Math.floor(Math.random() * responses.length)] || 'No entendí la pregunta.';
  }

  // Método para limpiar texto de entrada
  private cleanText(input: string): string {
    return input.toLowerCase().replace(/[^\w\s]/gi, '');
  }

  // Método para convertir texto en secuencias
  private textToSequences(input: string[], wordIndex: { [key: string]: number }): number[][] {
    return input.map((text) =>
      text.split(' ').map((word) => wordIndex[word] || 0)
    );
  }

  // Método para realizar padding de secuencias
  private padSequences(sequences: number[][], maxLength: number): number[][] {
    return sequences.map((seq) => {
      const padding = Array(Math.max(0, maxLength - seq.length)).fill(0);
      return seq.concat(padding).slice(0, maxLength);
    });
  }
}
