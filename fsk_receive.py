import winsound
from fsk_constants import *
import numpy as np
import pyaudio
import scipy.fftpack

# Constants
RATE = 44100  # Sampling rate in Hz
CHUNK = int(RATE * 0.25)  # Size of audio chunk (20ms window)

def find_closest_multiple_10(frequency):
    return round(frequency / 10) * 10

def receive():
    data=[]
    for d in data:
        #play the frequency for the duration
        frequency=RANGE_L+d*BIN_SIZE
        winsound.Beep(frequency, DURATION*1000)
    print("Broadcasting data:", data)


def process_audio(data):
    # Perform Fourier Transform
    fft_result = scipy.fftpack.fft(data)
    freqs = np.fft.fftfreq(len(fft_result), 1 / RATE)
    
    # Get positive frequencies and their magnitudes
    positive_freqs = freqs[:len(freqs) // 2]
    magnitudes = np.abs(fft_result[:len(fft_result) // 2])
    
    # Find the frequency with the highest magnitude
    peak_freq = positive_freqs[np.argmax(magnitudes)]
    closest_freq = find_closest_multiple_10(peak_freq)
    
    return peak_freq, closest_freq

    

def receive():
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Listening...")

    try:
        while True:
            data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
            peak_freq, closest_freq = process_audio(data)
            print(f"Dominant Frequency: {peak_freq:.2f} Hz, Closest Multiple of 10: {closest_freq} Hz")
    
    except KeyboardInterrupt:
        print("Stopping...")
    
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

def main():
    receive()


if __name__=="__main__":
    main()