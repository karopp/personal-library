import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import {MatCardModule} from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import {MatToolbarModule} from '@angular/material/toolbar';
import { Firestore } from '@angular/fire/firestore';
import { collection, query, getDocs} from "firebase/firestore";




interface Book {
  image_url: String;
  title: String;
  author: String;
  link: String;
  review: Number;
  details: String;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, MatCardModule, MatIconModule, MatToolbarModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  appTitle = 'PERSONAL LIBRARY';
  firestore = inject(Firestore);
  bookList: Book[] = [];

  constructor() {
    getDocs(query(collection(this.firestore, "books")
    )).then((querySnapshot) => {
      querySnapshot.forEach((doc) => {
        this.bookList.push(doc.data() as Book)
      })
    });
  }

}
