// angular import
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

// project import

import { CardComponent } from 'src/app/theme/shared/components/card/card.component';

@Component({
  selector: 'app-sample-page',
  imports: [CommonModule, CardComponent, FormsModule],
  templateUrl: './sample-page.component.html',
  styleUrls: ['./sample-page.component.scss']
})
export class ChatComponent 
{
  message='';
  messages: string[] = [];
  sendMessage() 
  {
    if(this.message.trim()){
      this.messages.push(this.message);
      this.message = '';
    }
  }
}
