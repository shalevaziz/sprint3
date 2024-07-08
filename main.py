import os
import cv2
import time
import qrcode
from PIL import Image
import base64
import numpy as np

def show_qrs(qrs, time_to_show=3):
    for i in qrs:
        i.get_image().resize((1000,1000)).show()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(time_to_show)
    
def generate_qr_code_from_file(bytes):
    # Read the file contents
    """with open(file_path, 'rb') as file:
        file_content = file.read()"""
    # name = get_file_name(file_path)
    
    # Convert binary content to a base64 encoded string
    base64_content = base64.b64encode(bytes).decode('utf-8')
    
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data to the instance
    qr.add_data(base64_content)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill='black', back_color='white')
    return img

def split_file_into_packets(filename, file_path):
    # Open the file in bytes mode
    with open(file_path, 'rb') as file:
        file_content = file.read()
    
    # Get the total size of the file
    file_size = len(file_content)
    
    # Calculate the number of packets needed
    packet_size = 256  # Change this to your desired packet size
    num_packets = (file_size + packet_size - 1) // packet_size  # ceil(file_size / packet_size)
    
    packets = []

    # Create the header with filename and number of packets
    header = f"{filename}:{num_packets}".encode('utf-8').ljust(50, b'\0')  # Pad header to a fixed length
    packets.append(header)
    
    # Create packets
    for i in range(num_packets):
        start = i * packet_size
        end = min(start + packet_size, file_size)
        data = file_content[start:end]
        
        # Add padding to the last packet
        if len(data) < packet_size:
            data = data.ljust(packet_size, b'\0')
        
        # Add the header to the packet
        packet = data
        packets.append(packet)
    
    return packets

# Function to save the packets to a new file for demonstration
def save_packets(packets, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for idx, packet in enumerate(packets):
        output_filename = os.path.join(output_dir, f"packet_{idx+1}")
        with open(output_filename, 'wb') as output_file:
            output_file.write(packet)
            
def read_packets(input_dir):
    # List all packet files in the directory and sort them
    packet_files = sorted(os.listdir(input_dir))
    
    packets = []
    for packet_file in packet_files:
        packet_path = os.path.join(input_dir, packet_file)
        with open(packet_path, 'rb') as file:
            packet = file.read()
            packets.append(packet)
    
    return packets

def reconstruct_file(packets, output_filename):
    # Initialize an empty byte array for the file content
    file_content = bytes()
    
    header = packets[0].rstrip(b'\0').decode('utf-8')
    filename, num_packets = header.split(':')
    num_packets = int(num_packets)
    
    for i in range(1, num_packets+1):
        packet = packets[i]
        file_content += packet
    
    file_content = file_content.rstrip(b'\0')
    # Write the reconstructed file content to the output file
    with open(output_filename, 'wb') as output_file:
        output_file.write(file_content)

# Example usage

# Example usage
all_packets = []
for filename in os.listdir('top_secret'):
    packets = split_file_into_packets(filename, os.path.join('top_secret', filename))
    all_packets += packets
# add a header to the packets
header = "".encode('utf-8').ljust(50, b'\0')  # Pad header to a fixed length
packets.append(header)
qrs = [generate_qr_code_from_file(packet) for packet in packets]
show_qrs(qrs)
print(len(packets))
"""save_packets(packets, 'output_packets')
packets = read_packets('output_packets')"""
