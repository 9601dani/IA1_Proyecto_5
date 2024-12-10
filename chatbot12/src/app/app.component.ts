import { Component } from '@angular/core';
import { ChatBotService } from './services/chat-bot.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'chatbot12';

  constructor(private chatbotService: ChatBotService) {  }

}
