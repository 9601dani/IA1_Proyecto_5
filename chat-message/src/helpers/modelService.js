import * as tf from '@tensorflow/tfjs';

let model = null;
let tokenizer = null;
let responsesMap = null;

export async function loadModelAndTokenizer() {
    if (!model || !tokenizer || !responsesMap) {
        try {
            model = await tf.loadLayersModel('/src/intents_model/model.json');

            const response = await fetch('/src/intents_model/chatbot_tokenizer.json');
            tokenizer = await response.json();

            console.log('Modelo y tokenizer cargados correctamente.');
        } catch (error) {
            console.error('Error al cargar el modelo o tokenizer:', error);
        }
    }

    const response = await fetch('/src/intents_model/intents.json');
    const intentsData = await response.json();

    responsesMap = {};
    intentsData.intents.forEach((intent) => {
        responsesMap[intent.tag] = intent.responses;
    });


    return { model, tokenizer, responsesMap };
}

export function getModel() {
    return model;
}

export function getTokenizer() {
    return tokenizer;
}

export function getResponsesMap() {
    return responsesMap;
}
