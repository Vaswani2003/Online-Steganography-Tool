import random
import numpy as np
import cv2

def get_voice_line():
    cypher_voice_lines = ['Nothing stays hidden from me.',
                          'Where is everyone hiding?',
                          "I know exactly where you are!",
                          "Nobody escapes me. But they'll try.",
                          "If they try something, I'll see it."]
    return random.choice(cypher_voice_lines)


# class Decryption:
#     def __init__(self, stego_image,key):
#         self.stego_image = stego_image
#         self.key = key
#         self.secret_message = None

#     def decrypt(self):
#         if self.key is None:
#             raise ValueError("Key is required for decryption")
        
#         secret_message = ''
#         average_key_value = self.calculate_average_key()

#         height, width, _ = self.stego_image.shape
#         position = average_key_value

#         while True:
#             character = ''

#             for i in range(8):
#                 x = position % width
#                 y = position // width

#                 if x >= width or y >= height:
#                     break

#                 pixel = self.stego_image[y, x]

#                 character += str(pixel[0] & 1)

#                 position += 1
                
#             if character == '':
#                 break

#             secret_message += chr(int(character, 2))

#             if secret_message[-3:]=='END':
#                 break

#         self.secret_message = secret_message

#         return self.secret_message
        
#     def calculate_average_key(self):
#         ascii_sum = sum(ord(char) for char in self.key)
#         return ascii_sum // len(self.key)

        
# class Encryption:
#     def __init__(self, uploaded_file, message, key):  # Step 1 --> Get the input cover image and secret message
#         self.cover_image = uploaded_file
#         self.message = message
#         self.key = key

#         self.stego_image = np.copy(uploaded_file)
#         self.average_key_value = None
#         self.psnr = None
#         self.snr = None

#     def encrypt(self):
#         self.average_key_value = self.calculate_average_key()
#         self.embed_secret_message()

#         self.psnr = cv2.PSNR(self.cover_image, self.stego_image)
#         self.calculate_snr()

#         return self.stego_image, self.psnr, self.snr


#     def calculate_average_key(self):
#         ascii_sum = sum(ord(char) for char in self.key)
#         return ascii_sum // len(self.key)
    
#     def embed_secret_message(self):
#         secret_message_in_binary_format = ''.join(format(ord(char), '08b') for char in self.message)

#         heigh, width, _ = self.cover_image.shape

#         position = self.average_key_value

#         for i, bit in enumerate(secret_message_in_binary_format):
#             x = position % width
#             y = position // width

#             pixel = self.stego_image[y, x]

#             if int(bit):
#                 self.stego_image[y, x][0] |= 1
#             else:
#                 self.stego_image[y, x][0] &= ~1

#             position += 1

#     def calculate_snr(self):
#         original_image = np.asarray(self.cover_image)
#         stego = np.asarray(self.stego_image)
    
#         signal_power = np.mean((original_image - np.mean(original_image)) ** 2)
#         noise_power = np.mean((original_image - stego) ** 2)

#         if noise_power == 0:
#             self.snr = np.inf
#         else:
#             self.snr = 10 * np.log10(signal_power / noise_power)
        

# import numpy as np
# import cv2

class Embedding:
    def __init__(self, cover_image, secret_message, stego_key):
        self.cover_image = cover_image
        self.secret_message = secret_message
        self.stego_key = stego_key
        self.stego_image = np.copy(cover_image)
        self.average_key_value = None
        self.psnr = None
        self.snr = None

    def embed(self):
        self.calculate_average_key()

        # Convert secret message to binary
        secret_message_binary = ''.join(format(ord(char), '08b') for char in self.secret_message)

        position = self.average_key_value

        # Embed each bit of secret message into LSB of cover image
        for bit in secret_message_binary:
            x = position % self.cover_image.shape[1]
            y = position // self.cover_image.shape[1]

            # Embed bit into LSB of red channel
            self.stego_image[y, x, 0] = (self.stego_image[y, x, 0] & 254) | int(bit)

            position += 1

        # Insert end character
        end_character = 'END'
        for char in end_character:
            x = position % self.cover_image.shape[1]
            y = position // self.cover_image.shape[1]

            # Embed character into LSB of red channel
            char_binary = format(ord(char), '08b')
            for bit in char_binary:
                self.stego_image[y, x, 0] = (self.stego_image[y, x, 0] & 254) | int(bit)

                position += 1

        # Calculate PSNR and SNR
        self.psnr = cv2.PSNR(self.cover_image, self.stego_image)
        self.calculate_snr()

        return self.stego_image, self.psnr, self.snr

    def calculate_average_key(self):
        ascii_sum = sum(ord(char) for char in self.stego_key)
        self.average_key_value = ascii_sum // len(self.stego_key)

    def calculate_snr(self):
        original_image = np.asarray(self.cover_image)
        stego = np.asarray(self.stego_image)
    
        signal_power = np.mean((original_image - np.mean(original_image)) ** 2)
        noise_power = np.mean((original_image - stego) ** 2)

        if noise_power == 0:
            self.snr = np.inf
        else:
            self.snr = 10 * np.log10(signal_power / noise_power)


class Extraction:
    def __init__(self, stego_image, stego_key):
        self.stego_image = stego_image
        self.stego_key = stego_key
        self.secret_message = None
        self.average_key_value = None

    def extract(self):
        self.calculate_average_key()

        position = self.average_key_value
        extracted_bits = ''
        height, width, _ = self.stego_image.shape

        while position < height * width * 3:
            x = position % self.stego_image.shape[1]
            y = position // self.stego_image.shape[1]

            if y >= height:
                break

            # Extract LSB of red channel
            extracted_bits += str(self.stego_image[y, x, 0] & 1)

            position += 1

            # Check for end character
            if len(extracted_bits) >= 24 and extracted_bits[-24:] == ''.join(format(ord(char), '08b') for char in 'END'):
                break

        # Convert extracted bits to characters
        self.secret_message = ''.join(chr(int(extracted_bits[i:i+8], 2)) for i in range(0, len(extracted_bits)-24, 8))

        return self.secret_message


    def calculate_average_key(self):
        ascii_sum = sum(ord(char) for char in self.stego_key)
        self.average_key_value = ascii_sum // len(self.stego_key)
