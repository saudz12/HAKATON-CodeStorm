import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private apiUrl = 'http://localhost:5000/api/sample-page'; // URL pentru preluarea mesajelor
  private sendMessageUrl = 'http://localhost:5000/sample-page'; // URL pentru trimiterea mesajului

  constructor(private http: HttpClient) {}

  // Metoda pentru preluarea mesajelor
  getMessages(): Observable<string[]> {
    return this.http.get<string[]>(this.apiUrl);
  }

  // Metoda pentru trimiterea mesajelor
  sendMessage(message: string, courseId:number, pdfId:number): Observable<any> {
    return this.http.post(this.sendMessageUrl, { chat: message, course_id: courseId, pdf_id:pdfId});
  }
}
