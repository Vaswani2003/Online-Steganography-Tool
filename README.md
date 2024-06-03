# Secret Cipher: Online Steganography Tool

Welcome to the Secret Cipher: Online Steganography Tool! This repository contains the source code for a web application that allows users to encrypt and decrypt messages within images using steganography techniques. The app is built using Streamlit, making it easy to run and interact with.

## Features

- **Message Encoding**: Hide a secret message within an image using a custom steganography algorithm.
- **Message Decoding**: Extract a hidden message from an image.
- **QR Code Generation**: (Coming soon) Generate and embed QR codes for additional information.
- **Random Voice Lines**: Enjoy random Cypher voice lines from Valorant for a fun user experience.

## Technologies Used

- **Frontend**: Streamlit for building the interactive web interface.
- **Backend**: Python for encoding and decoding messages.
- **Libraries**: `random`, `png`, `base64` for various functionalities.

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/secret-cipher.git
    cd secret-cipher
    ```

2. **Install dependencies**:
    ```sh
    pip install streamlit pypng
    ```

3. **Run the application**:
    ```sh
    streamlit run app.py
    ```

## Usage

### Encryption

1. **Upload an Image**: Select a PNG image to use for hiding your message.
2. **Enter a Message**: Type the message you want to encrypt into the image.
3. **Encrypt**: Click the "Encrypt" button to hide the message within the image.
4. **Download**: Download the encrypted image for storage or sharing.

### Decryption

1. **Upload an Encrypted Image**: Select a PNG image that contains a hidden message.
2. **Decrypt**: Click the "Decrypt" button to extract the hidden message from the image.
3. **Read the Message**: The decrypted text will be displayed on the screen.

## Code Overview

### Key Functions

- **encode_message_as_bytestring(message)**: Converts a message into a binary string.
- **get_pixels_from_image(fname)**: Reads pixels from an uploaded image.
- **encode_pixels_with_message(pixels, bytestring)**: Encodes the message into the image pixels.
- **write_pixels_to_image(pixels, fname)**: Writes the encoded pixels to a new image file.
- **decode_pixels(pixels)**: Decodes the message from the image pixels.
- **decode_message_from_bytestring(bytestring)**: Converts the binary string back into readable text.

### Streamlit Interface

- **Encryption Section**: Allows users to upload an image and enter a message to be encrypted.
- **Decryption Section**: Allows users to upload an image and decrypt the hidden message.

## Contribution

Contributions are welcome! Feel free to fork this repository, make improvements, and submit pull requests. Whether it’s adding new features, fixing bugs, or improving documentation, your contributions are valuable.

Thank you for visiting the Secret Cipher: Online Steganography Tool repository! We hope this application helps you securely hide and reveal messages. Happy encrypting!
