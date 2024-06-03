import streamlit as st
import random
import png
import base64
import methods


def encode_message_as_bytestring(message: str):
    b64 = message.encode("utf8")
    bytes_ = base64.encodebytes(b64)
    bytestring = "".join(["{:08b}".format(x) for x in bytes_])

    bytestring += "0101001001010101001101010100010101010100001100000101101001001110010100100101011001001110010101000101000101010101011001000100011000001010"
    return bytestring

def get_pixels_from_image(fname):
    img = png.Reader(fname).read()
    pixels = list(img[2])
    return pixels

def encode_pixels_with_message(pixels, bytestring):
    enc_pixels = []
    string_i = 0

    for row in pixels:
        enc_row = []
        for i, char in enumerate(row):
            if string_i >= len(bytestring):
                pixel = row[i]
            else:
                if row[i] % 2 != int(bytestring[string_i]):
                    if row[i] == 0:
                        pixel = 1
                    else:
                        pixel = row[i] - 1
                else:
                    pixel = row[i]
            enc_row.append(pixel)
            string_i += 1

        enc_pixels.append(enc_row)
    return enc_pixels

def write_pixels_to_image(pixels, fname):
    png.from_array(pixels, 'RGB').save(fname)

def decode_pixels(pixels):
    bytestring = []
    for row in pixels:
        for c in row:
            bytestring.append(str(c % 2))
    bytestring = ''.join(bytestring)
    message = decode_message_from_bytestring(bytestring)
    return message

def decode_message_from_bytestring(bytestring):
    ENDOFMESSAGE = "0101001001010101001101010100010101010100001100000101101001001110010100100101011001001110010101000101000101010101011001000100011000001010"
    bytestring = bytestring.split(ENDOFMESSAGE)[0]
    message = int(bytestring, 2).to_bytes(len(bytestring) // 8, byteorder='big')
    message = base64.decodebytes(message).decode("utf8")
    return message

def get_voice_line():
    cypher_voice_lines = ['Nothing stays hidden from me.',
                          'Where is everyone hiding?',
                          "I know exactly where you are!",
                          "Nobody escapes me. But they'll try.",
                          "If they try something, I'll see it."]
    return random.choice(cypher_voice_lines)

st.markdown("<h1 style='text-align: center;' >Secret Cipher<br>Online Steganography Tool</h1>", unsafe_allow_html=True)

current_voice_line = get_voice_line()

st.write(f"<h3 style='text-align: center;'> {current_voice_line}</h3>", unsafe_allow_html=True)

# Encryption Section

st.header('Encryption')

encryption_uploaded_file = st.file_uploader("Upload image", type=['png'], key='en')

message = st.text_input("Enter text to encrypt")

Encrypt_btn = st.button("Encrypt")

if Encrypt_btn:
    if encryption_uploaded_file is None:
        st.text("Please select a file first")
    elif message == "":
        st.text("Please enter a message to encrypt")
    else:

        bytestring = encode_message_as_bytestring(message)

        pixels = get_pixels_from_image(encryption_uploaded_file)

        enc_pixels = encode_pixels_with_message(pixels, bytestring)

        encrypted_image_path = "encrypted_image.png"
        write_pixels_to_image(enc_pixels, encrypted_image_path)
        st.success("Encryption successful.")

        with open(encrypted_image_path, "rb") as file:
            bytes_ = file.read()

        st.download_button(
            label="Download encrypted image",
            data=bytes_,
            file_name='encrypted_image.png',
            mime='image/png')


st.header('Decryption')

decryption_uploaded_file = st.file_uploader("Upload image", type=['png'], key='de')

Decrypt_button = st.button("Decrypt")

st.text('Decrypted Text')

if Decrypt_button:
    if decryption_uploaded_file is None:
        st.text("Please select a file first")
    else:
        pixels = get_pixels_from_image(decryption_uploaded_file)
        decrypted_message = decode_pixels(pixels)
        st.write(decrypted_message)
