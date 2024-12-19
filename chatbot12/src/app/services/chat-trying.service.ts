import { Injectable } from '@angular/core';
import { trainModel, predictResponse } from '../helpers/chatbot-training';

@Injectable({
  providedIn: 'root',
})
export class ChatbotTryingService {
  async trainChatbot(): Promise<void> {
   const item = localStorage.getItem('tensorflowjs_models/chatbot-model/info');
   if(JSON.parse(item) !== null) {
      console.log('Modelo ya entrenado');
      return;
   }
  console.log('Entrenando modelo...');
  await trainModel();
  }

  async getResponse(input: string): Promise<string> {
    return await predictResponse(input);
  }
}
