import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http'; // importă HttpClient
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CardComponent } from 'src/app/theme/shared/components/card/card.component';

@Component({
  selector: 'app-sample-page',
  imports: [CommonModule, CardComponent, FormsModule],
  templateUrl: './sample-page.component.html',
  styleUrls: ['./sample-page.component.scss']
})
export class ChatComponent {
  message = '';
  messages: string[] = [];

  // Injectează HttpClient
  constructor(private http: HttpClient) {}

  sendMessage() {
    if (this.message.trim()) {
      // Adaugă mesajul în lista de mesaje
      this.messages.push(this.message);

      // Trimite mesajul către API-ul Flask
      this.http.post('http://127.0.0.1:5000/sample-page', { chat: this.message })
        .subscribe(
          response => {
            console.log('Mesaj trimis cu succes către API:', response);
          },
          error => {
            console.error('Eroare la trimiterea mesajului:', error);
          }
        );

      // Resetează textbox-ul
      this.message = '';
    }
  }
}
