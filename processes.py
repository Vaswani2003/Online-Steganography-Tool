import streamlit as st
import funcs as fn
from funcs import Extraction, Embedding
import numpy as np
import cv2 


st.markdown("<h1 style='text-align: center;' >Secret Cipher<br>Online Steganography Tool</h1>", unsafe_allow_html=True)

current_voice_line = fn.get_voice_line()

st.write(f"<h3 style='text-align: center;'> {current_voice_line}</h3>", unsafe_allow_html=1)

st.header('Encryption')

encryption_uploaded_file = st.file_uploader("Upload image", type=['jpg', 'jpeg'], key='en')

message = st.text_input("Enter text to encrypt")

secret_key = st.text_input("Enter key")

Encrypt_btn = st.button("Encrypt")


if Encrypt_btn:
    if encryption_uploaded_file is None:
        st.text("Please select a file first")
    else:
        file_bytes = np.asarray(bytearray(encryption_uploaded_file.read()), dtype=np.uint8)
        cover_image = cv2.imdecode(file_bytes, 1)
        
        Encryption_tool = Embedding(cover_image,message,secret_key)

        stegno_image, psnr, snr = Encryption_tool.embed()

        st.write("PSNR:", psnr)
        st.write("SNR:", snr)

        st.image(stegno_image, caption='Stego Image', use_column_width=True)

        _, stegno_image_buffer = cv2.imencode(".jpg", stegno_image)
        stegno_image_bytes = stegno_image_buffer.tobytes()

        encrypted_image_filename = "encrypted_image.jpg"
        st.download_button(
            label="Download Encrypted Image",
            data=stegno_image_bytes,
            file_name=encrypted_image_filename,
            mime="image/jpeg"
        )

st.header('Decryption')

decryption_uploaded_file = st.file_uploader("Upload image", type=['jpg', 'jpeg'], key='de')

decryption_key = st.text_input('Enter numeric key')

Decrypt_button = st.button("Decrypt")

st.text('Decrypted Text')

if Decrypt_button:
    if decryption_uploaded_file is None:
        st.text("Please select a file first")
    else:
        file_bytes = np.asarray(bytearray(decryption_uploaded_file.read()), dtype=np.uint8)
        stego_image = cv2.imdecode(file_bytes, 1)

        Decryption_tool = Extraction(stego_image,decryption_key)

        message = Decryption_tool.extract()

        st.write(message)
        
