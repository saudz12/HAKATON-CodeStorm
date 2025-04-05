// Angular import
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService} from 'src/app/demo/services/auth.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-auth-register',
  imports: [RouterModule, FormsModule, CommonModule],
  templateUrl: './auth-register.component.html',
  styleUrl: './auth-register.component.scss'
})
export class AuthRegisterComponent {
  firstName = '';
	lastName = '';
	company = '';
	email = '';
	password = '';
	errorMessage = '';
	successMessage = '';
	userType: string='';

  constructor(private authService: AuthService, private router: Router) {}
  onRegister(): void {
		const data = {
			firstName: this.firstName,
			lastName: this.lastName,
			company: this.company,
			email: this.email,
			password: this.password, 
			userType: this.userType
		};

		this.authService.register(data.email, data.password).subscribe({
			next: () => {
				this.successMessage = 'Cont creat cu succes!';
				this.router.navigate(['/login']);
			},
			error: (err) => {
				this.errorMessage = err.error.error || 'Eroare la înregistrare.';
			}
		});
	}
  SignUpOptions = [
    {
      image: 'assets/images/authentication/google.svg',
      name: 'Google'
    },
    {
      image: 'assets/images/authentication/twitter.svg',
      name: 'Twitter'
    },
    {
      image: 'assets/images/authentication/facebook.svg',
      name: 'Facebook'
    }
  ];
}
