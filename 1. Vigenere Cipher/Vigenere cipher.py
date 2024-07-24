from collections import Counter

# Function to read a file and remove all non-alphabetic characters, converting the rest to lowercase
def textstrip(filename):
    '''This takes the file and converts it to a string with all the spaces and other
    special characters removed. What remains is only the lower case letters,
    retain only the lowercase letters!'''
    with open(filename, 'r') as file:
        text = file.read()  # Read the file contents
    cleaned_text = ''.join(filter(str.isalpha, text)).lower()  # Keep only alphabetic characters and convert to lowercase
    return cleaned_text

# Function to count the frequency of each letter in a string
def letter_distribution(s):
    '''Consider the string s which comprises of only lowercase letters. Count
    the number of occurrences of each letter and return a dictionary'''
    distribution = Counter(s)  # Count the occurrences of each character
    return dict(distribution)  # Convert Counter object to dictionary

# Function to encrypt a string using a substitution dictionary
def substitution_encrypt(s, d):
    '''Encrypt the contents of s by using the dictionary d which comprises of
    the substitutions for the 26 letters. Return the resulting string'''
    encrypted = ''.join(d.get(char,char) for char in s)  # Replace each character with its substitution
    return encrypted

# Function to decrypt a string using a substitution dictionary
def substitution_decrypt(s, d):
    '''Decrypt the contents of s by using the dictionary d which comprises of
    the substitutions for the 26 letters. Return the resulting string'''
    reverse_d = {v: k for k, v in d.items()}  # Reverse the substitution dictionary
    decrypted = ''.join(reverse_d.get(char, char) for char in s)  # Replace each character with its original
    return decrypted

def cryptanalyse_substitution(s):
    '''Given that the string s is given to us and it is known that it was encrypted using some substitution cipher, predict the d'''
    # Frequency analysis based on typical English letter frequencies
    english_freq = 'etaoinshrdlcumwfgypbvkjxqz'
    s_freq = Counter(s)
    # Sort characters by frequency in the encrypted string
    sorted_s = [item[0] for item in s_freq.most_common()]
    
    # Create a dictionary to map the encrypted characters to the most common English characters
    substitution_dict = {enc_char: eng_char for enc_char, eng_char in zip(sorted_s, english_freq)}
    
    return substitution_dict,sorted_s

# Function to encrypt a string using the Vigenère cipher
def vigenere_encrypt(s, password):
    '''Encrypt the string s based on the password the Vigenere cipher way and
    return the resulting string'''
    encrypted = []
    password = (password * ((len(s) // len(password)) + 1))[:len(s)]
    for i, char in enumerate(s):
        if char.isalpha():
            shift = ord(password[i % len(password)]) - ord('a')  # Calculate the shift
            if char.islower():
                encrypted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))  # Apply the shift
            else:
                encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))  # Apply the shift for uppercase
            encrypted.append(encrypted_char)
        else:
            encrypted.append(char)  # Keep non-alphabetic characters unchanged
    return ''.join(encrypted)

# Function to decrypt a string using the Vigenère cipher
def vigenere_decrypt(s, password):
    '''Decrypt the string s based on the password the Vigenere cipher way and
    return the resulting string'''
    decrypted = []
    password = (password * ((len(s) // len(password)) + 1))[:len(s)]
    
    for i, char in enumerate(s):
        if char.isalpha():
            shift = ord(password[i]) - ord('a') if password[i].islower() else ord(password[i]) - ord('A')  # Calculate the shift based on password character case
            if char.islower():
                decrypted_char = chr((ord(char) - ord('a') - shift + 26) % 26 + ord('a'))  # Reverse the shift for lowercase
            else:
                decrypted_char = chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A'))  # Reverse the shift for uppercase
            decrypted.append(decrypted_char)
        else:
            decrypted.append(char)  # Keep non-alphabetic characters unchanged
            
    return ''.join(decrypted)

# Function to find the length of the Vigenère cipher password
def cryptanalyse_vigenere_findlength(s):
    '''Given just the string s, find out the length of the password using which
    some text has resulted in the string s. We just need to return the number k'''
    
    def calculate_collisions(text, shift):
        collisions = 0
        for i in range(len(text) - shift):
            if text[i] == text[i + shift]:
                collisions += 1
        return collisions

    max_length = min(len(s)//3 ,20)  # Adaptive upper bound for potential key lengths, ensuring we check reasonable lengths
    collision_counts = []

    for length in range(1, max_length + 1):
        collision_count = calculate_collisions(s, length)
        collision_counts.append(collision_count)

    # The key length with the highest number of collisions is likely the correct one
    return collision_counts.index(max(collision_counts)) + 1



# Function to find the Vigenère cipher password given the length
# Function to find the Vigenère cipher password given the length
def cryptanalyse_vigenere_afterlength(s, k):
    '''Given the string s which is known to be Vigenère encrypted with a
    password of length k, find out what is the password'''
    columns = ['' for _ in range(k)]
    for i in range(len(s)):
        columns[i % k] += s[i]  # Split text into k columns
    
    password = ''
    for col in columns:
        freq = letter_distribution(col)
        most_common = max(freq, key=freq.get)  # Find most common letter
        # Assuming 'e' is the most common letter in English text
        shift = (ord(most_common.upper()) - ord('E')) % 26
        key_char = chr(shift + ord('A'))
        password += key_char
    
    return password


# Function to cryptanalyse the Vigenère cipher
def cryptanalyse_vigenere(s):
    '''Given the string s cryptanalyse vigenere, output the password as well as
    the plaintext'''
    length = cryptanalyse_vigenere_findlength(s)
    password = cryptanalyse_vigenere_afterlength(s, length)
    plaintext = vigenere_decrypt(s, password)
    return password, plaintext

def rotate_compare(s, r):
    '''This rotates the string s by r places and compares s(0) with s(r) and returns the proportion of collisions'''
    rotated_s = s[r:] + s[:r]
    collisions = sum(1 for i in range(len(s)) if s[i] == rotated_s[i])
    return collisions/len(s)

# Example usage
if __name__ == "__main__":
    # File path (replace with your file path)
    # file_path=input("Enter the path of the file to encrypt: ")
    file_path = r"C:\Users\Dell\Downloads\less_text.txt"
    
    # Strip text from file
    stripped_text = textstrip(file_path)
    # print("Stripped Text:", stripped_text)
    
    
    # Letter distribution
    distribution = letter_distribution(stripped_text)
    # print("Letter Distribution:", distribution)
    
    # Example substitution dictionary (a simple shift for demonstration)
    # substitution_dict = {chr(i): chr((i - 97 + 5) % 26 + 97) for i in range(97, 123)}
    # # print("Substitution Dictionary:", substitution_dict)
    
    # # Encrypt using substitution cipher
    # encrypted_text = substitution_encrypt(stripped_text, substitution_dict)
    # # print("Encrypted Text:", encrypted_text)
    
    # # Decrypt using substitution cipher
    # decrypted_text = substitution_decrypt(encrypted_text, substitution_dict)
    # # print("Decrypted Text:", decrypted_text)

    # substitution_dict, sorted_s=cryptanalyse_substitution(encrypted_text)
    # print("Substitution Recovered dict: ", substitution_dict)
    # print("Sorted ", sorted_s)

    
    # Example Vigenère password
    # vigenere_password=input("Enter the password for encryption: ")
    vigenere_password = 'helloworld'
    
    # Encrypt using Vigenère cipher
    vigenere_encrypted_text = vigenere_encrypt(stripped_text, vigenere_password)
    # print("Vigenère Encrypted Text:", vigenere_encrypted_text)
    
    # Decrypt using Vigenère cipher
    # vigenere_decrypted_text = vigenere_decrypt(vigenere_encrypted_text, vigenere_password)
    # print("Vigenère Decrypted Text:", vigenere_decrypted_text)

    #Saving the decrypted file to the user given location 
    # output_filename = input("Enter the path to save output file: ")
    # with open(output_filename, 'w', encoding='utf-8') as file:
    #     file.write(decrypted_text)
    # print(f"Decrypted text has been saved to {output_filename}")
    
    # Cryptanalysis of Vigenère cipher
    password, plaintext = cryptanalyse_vigenere(vigenere_encrypted_text)
    print("length: ", cryptanalyse_vigenere_findlength(vigenere_encrypted_text))
    print("Predicted Password:", password)
    print("Recovered Plaintext:", plaintext)

    # proportion_collision=rotate_compare(stripped_text,10)
    # print("Proportion of Collisions: ", proportion_collision)
