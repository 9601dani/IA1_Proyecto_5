import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { ChatBotService } from '../../../services/chat-bot.service';
import { ChatbotTryingService } from 'src/app/services/chat-trying.service';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  userInput!: string;
  messages: { sender: string; text: string }[] = [];
  modelSelectionForm: FormGroup;

  @ViewChild('chatMessages') chatMessages!: ElementRef;

  constructor(private chatbotService: ChatBotService, private chatTrying: ChatbotTryingService,private fb: FormBuilder) {}


  async ngOnInit() {
    this.modelSelectionForm = this.fb.group({
      model: ['sequence-to-sequence'] // Valor predeterminado
    });
    await this.chatbotService.loadModel();
    await this.chatTrying.trainChatbot()
  }

  async sendMessage() {
    if (this.userInput.trim() === '') return;
    const res = await this.chatTrying.getResponse(this.userInput)
    console.log( '-------',res  )
    this.messages.push({ sender: 'user', text: this.userInput });

    const { model } = this.modelSelectionForm.value;
    const userMessage = this.userInput;

    let data = '';

    if(model === 'sequence-to-sequence') {
      data = await this.chatbotService.decodeSequence(this.userInput);
    } else {
      // TODO: add intents model
    }

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