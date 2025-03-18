import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-gallery',
  standalone: true,
  imports: [CommonModule],  // 👈 Import CommonModule for Angular directives
  templateUrl: './gallery.component.html',
  styleUrls: ['./gallery.component.css']
})
export class GalleryComponent implements OnInit {
  images: string[] = []; // Array to store image URLs

  private repoOwner = "Oluoma-Eziolise";  // Change this to your GitHub username
  private repoName = "Snr-Design-IRIS"; // Change this to your repo name
  private folderPath = "server/html/images"; // Change this to your image folder

  ngOnInit(): void {
    this.fetchImages();
  }

  fetchImages(): void {
    const apiUrl = `https://api.github.com/repos/${this.repoOwner}/${this.repoName}/contents/${this.folderPath}`;

    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        this.images = data
          .filter((file: any) => file.name.match(/\.(jpg|jpeg|png|gif|webp|svg)$/i))
          .map((file: any) => file.download_url);
      })
      .catch(error => console.error("Error fetching images:", error));
  }
}