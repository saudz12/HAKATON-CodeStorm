import { Component, OnInit } from '@angular/core';
import { ChatService } from '../../services/chat.service';  // Importă serviciul ChatService
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CardComponent } from 'src/app/theme/shared/components/card/card.component';

@Component({
  selector: 'app-sample-page',
  imports: [CommonModule, CardComponent, FormsModule],
  templateUrl: './sample-page.component.html',
  styleUrls: ['./sample-page.component.scss']
  
})
export class ChatComponent implements OnInit {
  isTextboxVisible = false;
  toggleTextbox()
   {this.isTextboxVisible = !this.isTextboxVisible;}

  message = '';
  messages: string[] = [];

  constructor(private chatService: ChatService) {}  // Injectează ChatService, nu HttpClient

  ngOnInit(): void {
    this.loadMessages(); // Preluarea mesajelor la inițializarea componentei
  }

  loadMessages(): void {
    this.chatService.getMessages().subscribe({
      next: (data) => this.messages = data,  // Salvarea mesajelor
      error: (err) => console.error('Eroare la preluarea mesajelor:', err)
    });
  }

  sendMessage(): void {
    if (this.message.trim()) {
      // Adaugă mesajul în lista de mesaje local
      this.messages.push(this.message);

      // Trimite mesajul către API-ul Flask folosind ChatService 
      this.chatService.sendMessage(this.message, 102, 2).subscribe(
        (response) => {
          console.log('Mesaj trimis cu succes către API:', response);
          this.messages.push(response.ai_response)
        },
        (error) => {
          console.error('Eroare la trimiterea mesajului:', error);
        }
      );

      // Resetează input-ul
      this.message = '';
    }
  }

  sendMessage1(mode:string ): void 
  {
    this.chatService.sendMessage(mode, 102, 2).subscribe(
      (response) => {
        console.log('Mesaj trimis cu succes către API:', response);
        // this.messages.push(response.ai_response)
      },
      (error) => {
        console.error('Eroare la trimiterea mesajului:', error);
      }
    );
  }
}
