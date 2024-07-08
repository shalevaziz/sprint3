import os

TOP_SECRET_FOLDER_PATH = r'C:\Users\Public\Documents\top_secret'
TOP_SECRET_FOLDER_PATH = 'top_secret'
top_secret_files = os.listdir(TOP_SECRET_FOLDER_PATH)

def split_to_channels(data, num_channels = 2):
    # Split the data into num_channels channels
    splitted_data = []
    for i in range(0,len(data),num_channels):
        splitted_data.append(data[i:i+num_channels])
    
    last = data[len(data)//num_channels*num_channels:]
    if len(last) != 0:
        last += [None] * (num_channels - len(last))
        
        splitted_data.append(last)
        
    return splitted_data

def read_files(top_secret_path):
    files_bytes = []
    for file in top_secret_files:
        with open(os.path.join(TOP_SECRET_FOLDER_PATH, file), 'rb') as f:
            data = f.read()
            # convert each byte to an integer
            data = [int(byte) for byte in data]
            files_bytes.append(data)
    
    return files_bytes            


def decrypt_file(data:list[list[int]]) -> bytes:
    # Decrypt the data
    file_bytes = b''
    decrypted_data = []
    for i, packet in enumerate(data):
        for j, byte in enumerate(packet):
            if byte is None:
                continue
            decrypted_data.append(byte.to_bytes(1, 'big'))
    
    return b''.join(decrypted_data)
        

def main():
    files_bytes = read_files(TOP_SECRET_FOLDER_PATH)
    for file in files_bytes:
        splitted_data = split_to_channels(file)
        decrypted_data = decrypt_file(splitted_data)
        with open('decrypted_file.txt', 'wb') as f:
            f.write(decrypted_data)
        print(decrypted_data)
    

if __name__ == '__main__':
    main()