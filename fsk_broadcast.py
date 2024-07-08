import winsound
from fsk_constants import *

def broadcast(data):
    print("Broadcasting data:", data)
    for d in data:
        #play the frequency for the duration
        frequency=RANGE_L+d*BIN_SIZE
        winsound.Beep(frequency, DURATION*1000)
    


def main():
    data=[i for i in range(256)]
    broadcast(data)

if __name__=="__main__":
    main()
    

