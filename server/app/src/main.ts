import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';
import { GalleryComponent } from './app/gallery/gallery.component';

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));
