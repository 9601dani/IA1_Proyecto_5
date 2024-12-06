import { CommonModule } from '@angular/common';
import { Component, ElementRef, ViewChild} from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {

  userInput!: string
  messages: { sender: string; text: string }[] = [];


  @ViewChild('chatMessages') chatMessages!: ElementRef;

  sendMessage() {
    if (this.userInput.trim() === '') return;

    this.messages.push({ sender: 'user', text: this.userInput });

    const userMessage = this.userInput;
    this.userInput = '';

    setTimeout(() => {
      this.messages.push({ sender: 'bot', text: this.generateBotResponse(userMessage) });
      this.scrollToBottom();
    }, 1000);
  }

  generateBotResponse(userMessage: string): string {

    /*
    * Aqui ya iria la logica para llamar al metodo muchades
    */
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
