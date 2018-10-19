def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ''
    shift = []
    for i in range(len(keyword)):
        if keyword[i].isupper():
            shift.append(ord(keyword[i]) - 65)
        elif keyword[i].islower():
            shift.append(ord(keyword[i]) - 97)
        else:
            print('ОШИБКА(введена не буква)')
    if len(plaintext) > len(shift):
        shift *= len(plaintext) // len(shift) + 1
    for i in range(len(plaintext)):
        if plaintext[i].islower():
            if ord(plaintext[i]) + shift[i] > 122:
                ciphertext += chr(ord(plaintext[i]) + shift[i] - 26)
            else:
                ciphertext += chr(ord(plaintext[i]) + shift[i])
        elif plaintext[i].isupper():
            if ord(plaintext[i]) + shift[i] > 90:
                ciphertext += chr(ord(plaintext[i]) + shift[i] - 26)
            else:
                ciphertext += chr(ord(plaintext[i]) + shift[i])
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ''
    shift = []
    for i in range(len(keyword)):
        if keyword[i].isupper():
            shift.append(ord(keyword[i]) - 65)
        elif keyword[i].islower():
            shift.append(ord(keyword[i]) - 97)
        else:
            print('ОШИБКА(введена не буква)')
    if len(ciphertext) > len(shift):
        shift *= len(ciphertext) // len(shift) + 1
    for i in range(len(ciphertext)):
        if ciphertext[i].islower():
            if ord(ciphertext[i]) + shift[i] < 97:
                plaintext += chr(ord(ciphertext[i]) - shift[i] + 26)
            else:
                plaintext += chr(ord(ciphertext[i]) - shift[i])
        elif ciphertext[i].isupper():
            if ord(ciphertext[i]) - shift[i] < 65:
                plaintext += chr(ord(ciphertext[i]) - shift[i] + 26)
            else:
                plaintext += chr(ord(ciphertext[i]) - shift[i])
        else:
            plaintext += ciphertext[i]
    return plaintext
