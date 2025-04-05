import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-courses',
  //standalone: true,
  imports: [CommonModule],
  templateUrl: './courses.component.html',
  styleUrls: ['./courses.component.scss']
})

export class CoursesComponent {
onAddCourse() {

}
  courses:any[]=
  [
    {
      courseName:'Matematică',
      description:'',
      pdfs:[{path:'./assets/docs/Algebra.pdf', name:'Algebra'},{path:'./assets/docs/ComplexNumbers.pdf', name:'Complex Numbers'}, {path:'./assets/docs/Geometry.pdf', name:'Geometry'}]
    },
    {
      courseName:'Informatică',
      description:'',
      pdfs:[{path:'./assets/docs/DataStructure.pdf', name:'Data Structures'}, {path:'./assets/docs/LiniarRegression.pdf', name:'Liniar Regression'}, {path:'./assets/docs/Sorting.pdf', name:'Sorting'}]
    },
    {
      courseName:'Fizică',
      description:'',
      image:'',
      pdfs:['','']
    },
  ];
  
  userType:string='';

  selectedCourse: any = null;
  constructor(private router: Router, private http:HttpClient) {}
  
  openCourse(course: any) {
    //console.log('Înscriere pentru:', course.title);
    //this.router.navigate(['/courses', course.id]);
    this.selectedCourse=course;
  }

  // ngOnInit():void{
  //   this.http.get<any>('http://127.0.0.1:5000/dashboard/courses').subscribe({
	// 		next: (response) => {
	// 			console.log('Date cursuri:', response);
	// 			this.courses = response.courses; // ia din răspunsul JSON
	// 		},
	// 		error: (err) => {
	// 			console.error('Eroare la încărcarea cursurilor:', err);
	// 		}
	// 	});
  // }
 
}
