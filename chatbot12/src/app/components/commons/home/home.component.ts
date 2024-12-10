import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { ChatBotService } from '../../../services/chat-bot.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  userInput!: string;
  messages: { sender: string; text: string }[] = [];

  @ViewChild('chatMessages') chatMessages!: ElementRef;

  constructor(private chatbotService: ChatBotService) {}

  async ngOnInit() {
    await this.chatbotService.loadModel();
  }

  async sendMessage() {
    if (this.userInput.trim() === '') return;

    this.messages.push({ sender: 'user', text: this.userInput });

    const userMessage = this.userInput;
    const data = await this.chatbotService.decodeSequence(this.userInput);
    console.log(data)

    this.userInput = '';

    this.messages.push({ sender: 'bot', text: data });
  }

  generateBotResponse(userMessage: string): string {
    if (userMessage.toLowerCase().includes('hola')) {
      return '¡Hola! ¿En qué puedo ayudarte?';
    } else if (userMessage.toLowerCase().includes('adiós')) {
      return '¡Hasta luego! Que tengas un buen día.';
    } else {
      return 'Lo siento, no entiendo tu mensaje. ¿Podrías ser más específico?';
    }
  }

  scrollToBottom() {
    setTimeout(() => {
      if (this.chatMessages) {
        this.chatMessages.nativeElement.scrollTop = this.chatMessages.nativeElement.scrollHeight;
      }
    }, 200);
  }
}
