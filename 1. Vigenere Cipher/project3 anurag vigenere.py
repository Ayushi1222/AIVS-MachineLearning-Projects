import string
from collections import Counter

def textstrip(filename):
    '''This takes the file and converts it to a string with all the spaces and other
    special characters removed. What remains is only the lower case letters,
    retain only the lowercase letters!
    '''
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read().lower()
    return ''.join(filter(str.isalpha, text))

def letter_distribution(s):
    '''Consider the string s which comprises of only lowercase letters. Count
    the number of occurrences of each letter and return a dictionary'''
    return dict(Counter(s))

def substitution_encrypt(s, d):
    '''Encrypt the contents of s by using the dictionary d which comprises of
    the substitutions for the 26 letters. Return the resulting string'''
    return ''.join(d[char] if char in d else char for char in s)

def substitution_decrypt(s, d):
    '''Decrypt the contents of s by using the dictionary d which comprises of
    the substitutions for the 26 letters. Return the resulting string'''
    inverse_d = {v: k for k, v in d.items()}
    return ''.join(inverse_d[char] if char in inverse_d else char for char in s)

def cryptanalyse_substitution(s):
    '''Given that the string s is given to us and it is known that it was
    encrypted using some substitution cipher, predict the d'''
    # This is a placeholder for an actual cryptanalysis method which can be complex.
    # For demonstration, assuming a simple frequency analysis approach.
    frequency_order = 'etaoinshrdlcumwfgypbvkjxqz'
    freq_dist = letter_distribution(s)
    sorted_chars = sorted(freq_dist, key=freq_dist.get, reverse=True)
    d = {char: freq_char for char, freq_char in zip(sorted_chars, frequency_order)}
    return d

def vigenere_encrypt(s, password):
    '''Encrypt the string s based on the password the vigenere cipher way and
    return the resulting string'''
    password = password.lower()
    key_indices = [ord(char) - ord('a') for char in password]
    key_length = len(key_indices)
    encrypted = []

    for i, char in enumerate(s):
        if char.isalpha():
            offset = ord('a')
            char_code = ord(char) - offset
            key_code = key_indices[i % key_length]
            encrypted_char = chr((char_code + key_code) % 26 + offset)
            encrypted.append(encrypted_char)
        else:
            encrypted.append(char)

    return ''.join(encrypted)

def vigenere_decrypt(s, password):
    '''Decrypt the string s based on the password the vigenere cipher way and
    return the resulting string'''
    password = password.lower()
    key_indices = [ord(char) - ord('a') for char in password]
    key_length = len(key_indices)
    decrypted = []

    for i, char in enumerate(s):
        if char.isalpha():
            offset = ord('a')
            char_code = ord(char) - offset
            key_code = key_indices[i % key_length]
            decrypted_char = chr((char_code - key_code + 26) % 26 + offset)
            decrypted.append(decrypted_char)
        else:
            decrypted.append(char)

    return ''.join(decrypted)

def rotate_compare(s, r):
    '''This rotates the string s by r places and compares s(0) with s(r) and
    returns the proportion of collisions'''
    rotated_s = s[r:] + s[:r]
    collisions = sum(1 for a, b in zip(s, rotated_s) if a == b)
    return collisions / len(s)

def cryptanalyse_vigenere_afterlength(s, k):
    '''Given the string s which is known to be vigenere encrypted with a
    password of length k, find out what is the password'''
    columns = ['' for _ in range(k)]
    for i, char in enumerate(s):
        columns[i % k] += char

    password = ''
    frequency_order = 'etaoinshrdlcumwfgypbvkjxqz'
    for col in columns:
        freq_dist = letter_distribution(col)
        sorted_chars = sorted(freq_dist, key=freq_dist.get, reverse=True)
        most_common_char = sorted_chars[0]
        key_char = chr((ord(most_common_char) - ord('e')) % 26 + ord('a'))
        password += key_char

    return password

def cryptanalyse_vigenere_findlength(s):
    '''Given just the string s, find out the length of the password using which
    some text has resulted in the string s. We just need to return the number
    k'''
    n = len(s)
    avg_collisions = []

    for k in range(1, 21):
        collisions = sum(rotate_compare(s, r) for r in range(k))
        avg_collisions.append((collisions / k, k))

    return max(avg_collisions)[1]

def cryptanalyse_vigenere(s):
    '''Given the string s cryptanalyse vigenere, output the password as well as
    the plaintext'''
    k = cryptanalyse_vigenere_findlength(s)
    password = cryptanalyse_vigenere_afterlength(s, k)
    plaintext = vigenere_decrypt(s, password)
    return password, plaintext

if __name__ == "__main__":
    import sys
    
    while True:
        print("Select an option:")
        print("1. Encrypt a text file using Vigenère Cipher")
        print("2. Decrypt an encrypted text file using Vigenère Cipher")
        #print("3. Cryptanalyse an encrypted text file and find the password and plaintext")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            filename = input("Enter the filename to encrypt: ")
            password = input("Enter the password for encryption: ")
            text = textstrip(filename)
            encrypted_text = vigenere_encrypt(text, password)
            output_filename = input("Enter the output filename: ")
            with open(output_filename, 'w', encoding='utf-8') as file:
                file.write(encrypted_text)
            print(f"Encrypted text has been saved to {output_filename}")
        
        elif choice == '2':
            filename = input("Enter the filename to decrypt: ")
            password = input("Enter the password for decryption: ")
            with open(filename, 'r', encoding='utf-8') as file:
                encrypted_text = file.read()
            decrypted_text = vigenere_decrypt(encrypted_text, password)
            output_filename = input("Enter the output filename: ")
            with open(output_filename, 'w', encoding='utf-8') as file:
                file.write(decrypted_text)
            print(f"Decrypted text has been saved to {output_filename}")
        
        
        #elif choice == '3':
            #filename = input("Enter the filename to cryptanalyse: ")
            #with open(filename, 'r', encoding='utf-8') as file:
                #encrypted_text = file.read()
            #password, plaintext = cryptanalyse_vigenere(encrypted_text)
            #print(f"Predicted password: {password}")
            #output_filename = input("Enter the output filename for plaintext: ")
            #with open(output_filename, 'w', encoding='utf-8') as file:
                ##file.write(plaintext)
            #print(f"Decrypted plaintext has been saved to {output_filename}")
        
        
        elif choice == '3':
            print("Exiting...")
            sys.exit()
        
        else:
            print("Invalid choice. Please select a valid option.")
