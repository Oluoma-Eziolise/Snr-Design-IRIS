import time
import array
import pulseio
import board
import adafruit_irremote
import os

#for use with circuitpython, not to be ran from IDE

# File to be transmitted
FILE_PATH = "/mnt/data/compressedImages.zip"
CHUNK_SIZE = 32  # Adjust as needed for reliable transmission

# IR Transmitter Setup
pulseout = pulseio.PulseOut(board.D6, frequency=38000, duty_cycle=2**15)
encoder = adafruit_irremote.GenericTransmit(header=[9000, 4500],
                                            one=[560, 1700],
                                            zero=[560, 560],
                                            trail=0)

# IR Receiver Setup
ir_receiver = pulseio.PulseIn(board.D5, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()

def send_chunk(data, chunk_id):
    """Encodes and sends a chunk of data."""
    encoded_chunk = [chunk_id] + list(data)
    pulse_array = array.array('H', encoder.encode(encoded_chunk))
    pulseout.send(pulse_array)
    print(f"Sent chunk {chunk_id}")
    time.sleep(0.5)

def receive_chunks():
    """Receives and reconstructs the file as received_file.zip."""
    received_data = {}
    while True:
        pulses = decoder.read_pulses(ir_receiver)
        try:
            decoded = decoder.decode_bits(pulses)
            chunk_id = decoded[0]
            data = bytes(decoded[1:])
            received_data[chunk_id] = data
            print(f"Received chunk {chunk_id}")
        except (adafruit_irremote.IRNECRepeatException, adafruit_irremote.IRDecodeException):
            pass
        ir_receiver.clear()
        if len(received_data) * CHUNK_SIZE >= os.path.getsize(FILE_PATH):
            break
    
    # Reassemble the file with the specified name
    with open("received_file.zip", "wb") as f:
        for i in sorted(received_data.keys()):
            f.write(received_data[i])
    print("File received and reassembled as received_file.zip.")

def transmit_file():
    """Reads and sends the file in chunks."""
    with open(FILE_PATH, "rb") as f:
        chunk_id = 0
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            send_chunk(chunk, chunk_id)
            chunk_id += 1
    print("File transmission complete.")

# Uncomment the appropriate function for sender or receiver
# transmit_file()  # Call this on the sending device
# receive_chunks()  # Call this on the receiving device
