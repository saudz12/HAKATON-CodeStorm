import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-courses',
  //standalone: true,
  imports: [CommonModule],
  templateUrl: './courses.component.html',
  styleUrls: ['./courses.component.scss']
})

export class CoursesComponent {
  courses = [
    {
      id: 1,
      title: 'Matematică 1',
      description: 'Curs de matematică pentru inginerie',
      image: 'assets/images/math-course.jpg',
      files: [
        { name: 'Cursul 1', path: 'assets/docs/math1.pdf' },
        { name: 'Cursul 2', path: 'assets/docs/math2.pdf' }
      ]
    },
    {
      id: 2,
      title: 'Fizică',
      description: 'Curs de fizică generală',
      image: 'assets/images/physics-course.jpg',
      files: [
        { name: 'Cursul 1', path: 'assets/docs/physics-course1.pdf' },
        { name: 'Cursul 2', path: 'assets/docs/physics-course2.pdf' }
      ]
    }
    //mai multe cursuri
  ];

  selectedCourse: any = null;
  constructor(private router: Router) {}
  
  openCourse(course: any) {
    //console.log('Înscriere pentru:', course.title);
    //this.router.navigate(['/courses', course.id]);
    this.selectedCourse=course;
  }
}
