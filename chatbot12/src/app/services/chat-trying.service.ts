import { Injectable } from '@angular/core';
import { trainModel, predictResponse } from '../helpers/chatbot-training';

@Injectable({
  providedIn: 'root',
})
export class ChatbotTryingService {
  async trainChatbot(): Promise<void> {
    await trainModel();
  }

  async getResponse(input: string): Promise<string> {
    return await predictResponse(input);
  }
}
