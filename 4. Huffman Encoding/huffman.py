import heapq
from collections import Counter
import pickle

class HuffmanNode:
    def __init__(self, freq, data=None, left=None, right=None):
        self.freq = freq
        self.data = data
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def get_huffman_tree(byte_data):
    frequency = Counter(byte_data)
    heap = [HuffmanNode(freq=freq, data=byte) for byte, freq in frequency.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)
    
    return heap[0]

def get_codes(node, prefix="", code_map=None):
    if code_map is None:
        code_map = {}
    if node:
        if node.data is not None:
            code_map[node.data] = prefix
        get_codes(node.left, prefix + '0', code_map)
        get_codes(node.right, prefix + '1', code_map)
    return code_map

def compress(src, dst):
    with open(src, 'rb') as f:
        byte_data = f.read()
    # print(byte_data)
    huffman_tree = get_huffman_tree(byte_data)
    huffman_codes = get_codes(huffman_tree)
    # print(huffman_codes)
    
    encoded_data = ''.join(huffman_codes[byte] for byte in byte_data)
    # print(encoded_data)
    padding_length = 8 - len(encoded_data) % 8
    encoded_data += '0' * padding_length

    b = bytearray()
    for i in range(0, len(encoded_data), 8):
        byte = encoded_data[i:i+8]
        b.append(int(byte, 2))

    with open(dst, 'wb') as f:
        f.write(bytearray([padding_length]))
        pickle.dump(huffman_codes, f)  # Save Huffman codes before byte data
        f.write(bytes(b))  # Save byte data after Huffman codes

def decompress(src, dst):
    with open(src, 'rb') as f:
        padding_length = ord(f.read(1))
        huffman_codes = pickle.load(f)
        byte_data = f.read()
    
    binary_string = ''.join(f'{byte:08b}' for byte in byte_data)
    encoded_data = binary_string[:-padding_length]
    
    reversed_codes = {v: k for k, v in huffman_codes.items()}
    decoded_data = bytearray()
    
    code = ''
    for bit in encoded_data:
        code += bit
        if code in reversed_codes:
            decoded_data.append(reversed_codes[code])
            code = ''
    
    with open(dst, 'wb') as f:
        f.write(decoded_data)

if __name__ == "__main__":
    compress(r"D:\AIVS-Projects\4. Huffman Encoding\text_project_Huffman.txt", r"D:\AIVS-Projects\4. Huffman Encoding\compress2.txt")
    decompress(r"D:\AIVS-Projects\4. Huffman Encoding\compress2.txt", r"D:\AIVS-Projects\4. Huffman Encoding\sample_back_text.txt")
