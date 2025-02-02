# Photos App - Encrypted Media Viewer

Table of Contents
* ### Overview

* ### Features

* ### Prerequisites

* ### Installation

* ### Usage

* ### Encryption Method

* ### Security Considerations

* ### Customization

* ### Troubleshooting

* ### Contributing

* ### License

* ### Acknowledgements

## Overview
Photos App is a secure and intuitive application designed for viewing encrypted images and videos. Built with Python and Tkinter, it provides an elegant interface that decrypts and displays media files on-the-fly without leaving decrypted copies on disk. This ensures your sensitive media remains confidential and secure during viewing.

## Features
Secure Decryption: Utilizes SHA-256 hashing for key derivation and decrypts media in memory.

Multiple Media Formats: Supports various image formats (PNG, JPEG, BMP, GIF) and video formats (MP4, AVI, MKV, MOV).

User-Friendly Interface: Features a polished GUI with navigation controls and customizable themes.

In-Memory Video Playback: Plays videos directly from memory without writing temporary files to disk.

Responsive Design: Ensures smooth navigation and media viewing experience.

## Prerequisites
* Python 3.x
* pip (Python package installer)

## Installation
1. Clone the Repository
   git clone https://github.com/Salahkarrar/photos-app.git
   cd photos-app
2. Create a Virtual Environment (Optional but Recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
3. Install Dependencies
   pip install ttkthemes pillow numpy opencv-python-headless imageio imageio-ffmpeg
4. Download Arrow Icon Images
   * Create an img directory in the project root.
   * Place prev_arrow.png and next_arrow.png images in the img directory.
   * Ensure the images are appropriately sized and have transparent backgrounds.
## Usage
1. Run the Application
   * python photos_app.py
2. Enter Decryption Key
   * Upon launch, enter your decryption key in the provided input field.
   * Click Submit Key and Browse Folder.

3. Select Encrypted Media Folder
   * A file dialog will appear. Navigate to the folder containing your encrypted media files.
   * Select the folder to load the media into the app.
4. Navigate Media Files
   * Use the left and right arrow buttons to navigate through your media.
   * Images are displayed directly.
   * Videos play within the application without saving decrypted copies to disk.

## Encryption Method
The application expects media files encrypted with a simple XOR cipher using a key derived from a SHA-256 hash of your decryption key.

## Security Considerations
* In-Memory Decryption: Media files are decrypted in memory, and no decrypted copies are written to disk.
* Key Security: Keep your decryption key confidential. Anyone with access to both the encrypted files and the key can decrypt and view your media.
* No Permanent Storage: The application does not store keys or decrypted media.

## License
This project is licensed under the <ins>*SalahKarrar*</ins> License.

## Acknowledgements
* Tkinter for the GUI framework.
* ttkthemes for providing customizable themes.
* Pillow (PIL) for image processing capabilities.
* NumPy and OpenCV for numerical computations and video processing.
* imageio and imageio-ffmpeg for video reading and streaming.

