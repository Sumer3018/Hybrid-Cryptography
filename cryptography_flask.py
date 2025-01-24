import random
import string
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def generate_shift_key(plain_text):
    keys = []
    words = plain_text.split()
    for word in words:
        length = len(word)
        max_key_length = length ** length
        key = random.randint(0, max_key_length)
        keys.append(key)
    return keys

def shift_cipher_encrypt(word, key):
    cipher_text = ""
    for char in word:
        if char.isalpha():
            if char.islower():
                shifted = chr(((ord(char) - ord('a') + key) % 26) + ord('a'))
            else:
                shifted = chr(((ord(char) - ord('A') + key) % 26) + ord('A'))
        else:
            shifted = char
        cipher_text += shifted
    return cipher_text

def shift_cipher_decrypt(word, key):
    cipher_text = ""
    for char in word:
        if char.isalpha():
            if char.islower():
                shifted = chr(((ord(char) - ord('a') - key) % 26) + ord('a'))
            else:
                shifted = chr(((ord(char) - ord('A') - key) % 26) + ord('A'))
        else:
            shifted = char
        cipher_text += shifted
    return cipher_text

def generate_vigenere_key(word):
    key_length = len(word)
    key = ''.join(random.choice(string.ascii_letters) for _ in range(key_length))
    return key

def vigenere_cipher_encrypt(word, key):
    cipher_text = ""
    for i, char in enumerate(word):
        if char.isalpha():
            shift = ord(key[i % len(key)]) - (ord('a') if char.islower() else ord('A'))
            if char.islower():
                shifted = chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
            else:
                shifted = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
        else:
            shifted = char
        cipher_text += shifted
    return cipher_text

def vigenere_cipher_decrypt(word, key):
    decrypted_text = ""
    for i, char in enumerate(word):
        if char.isalpha():
            shift = ord(key[i % len(key)]) - (ord('a') if char.islower() else ord('A'))
            if char.islower():
                shifted = chr(((ord(char) - ord('a') - shift) % 26) + ord('a'))
            else:
                shifted = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
        else:
            shifted = char
        decrypted_text += shifted
    return decrypted_text

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        plain_text = request.json.get('plain_text')

        # Shift cipher
        shift_keys = generate_shift_key(plain_text)
        cipher_text1 = ""
        words = plain_text.split()
        for i, word in enumerate(words):
            cipher_text1 += shift_cipher_encrypt(word, shift_keys[i]) + " "

        cipher_text1 = cipher_text1.strip()

        # Vigenère cipher
        vigenere_keys = [generate_vigenere_key(word) for word in cipher_text1.split()]
        cipher_text2 = ""
        cipher_text1_words = cipher_text1.split()
        for i, word in enumerate(cipher_text1_words):
            cipher_text2 += vigenere_cipher_encrypt(word, vigenere_keys[i]) + " "

        cipher_text2 = cipher_text2.strip()

        # Decrypting the Vigenère cipher to get back to Cipher Text 1
        decrypted_text1 = ""
        cipher_text2_words = cipher_text2.split()
        for i, word in enumerate(cipher_text2_words):
            decrypted_text1 += vigenere_cipher_decrypt(word, vigenere_keys[i]) + " "

        decrypted_text1 = decrypted_text1.strip()

        # Decrypting the shift cipher to get back to the plain text
        decrypted_text2 = ""
        decrypted_text1_words = decrypted_text1.split()
        for i, word in enumerate(decrypted_text1_words):
            decrypted_text2 += shift_cipher_decrypt(word, shift_keys[i]) + " "

        decrypted_text2 = decrypted_text2.strip()

        # Prepare the response JSON
        response_data = {
            'plain_text': plain_text,
            'shift_key': shift_keys,
            'cipher_text1': cipher_text1,
            'vigenere_key': vigenere_keys,
            'cipher_text2': cipher_text2,
            'decrypted_text2': decrypted_text2
        }

        return jsonify(response_data)

    return render_template('index.html')

@app.route('/result')
def result():
    plain_text = request.args.get('plain_text')
    shift_key = request.args.get('shift_key')
    cipher_text1 = request.args.get('cipher_text1')
    vigenere_key = request.args.get('vigenere_key')
    cipher_text2 = request.args.get('cipher_text2')
    decrypted_text2 = request.args.get('decrypted_text2')
    return render_template('result.html', plain_text=plain_text, shift_key=shift_key,
                           cipher_text1=cipher_text1, vigenere_key=vigenere_key,
                           cipher_text2=cipher_text2, decrypted_text2=decrypted_text2)

if __name__ == '__main__':
    app.run(debug=True)
