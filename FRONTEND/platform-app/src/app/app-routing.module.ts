// angular import
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// Project import
import { AdminComponent } from './theme/layouts/admin-layout/admin-layout.component';
import { GuestLayoutComponent } from './theme/layouts/guest-layout/guest-layout.component';

const routes: Routes = [
  
    // Ruta implicita redirectioneaza catre login
  { path: '', redirectTo: '/login', pathMatch: 'full' },

  // Rutele pentru utilizatorii neautentificati (login, register)
  {
    path: '',
    component: GuestLayoutComponent,
    children: [
      {
        path: 'login',
        loadComponent: () =>
          import('./demo/dashboard/default/login.component').then((c) => c.AuthLoginComponent
          )
      },
      {
        path: 'register',
        loadComponent: () =>
          import('./demo/pages/authentication/auth-register/auth-register.component').then(
            (c) => c.AuthRegisterComponent
          )
      }
    ]
  },

  // Rutele pentru zona dashboard (accesibile dupa login)
  {
    path: 'dashboard',
    component: AdminComponent,
    children: [
      // Pagina principala de dashboard – portalul unde utilizatorul alege intre cursuri si chat
      {
        path: '',
        loadComponent: () =>
          import('./demo/begin/dashboard.component').then((c) => c.DashboardComponent)
      },
      // Ruta pentru pagina de cursuri
      {
        path: 'courses',
        loadComponent: () =>
          import('./demo/pages/authentication/courses/courses.component').then((c) => c.CoursesComponent
          )
      },
      // Ruta pentru pagina de chat
      {
        path: 'chat',
        loadComponent: () =>
          import('./demo/others/sample-page/sample-page.component').then(
            (c) => c.ChatComponent
          )
      }
    ]
  },

  // Ruta wildcard duce catre login
  //{ path: '**', redirectTo: '/login' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
