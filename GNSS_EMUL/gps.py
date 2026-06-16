import socket
import struct
# 1. Crea il socket UDP (SOCK_DGRAM)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Definisci la destinazione (IP e Porta del server che riceve)
DESTINAZIONE = ('127.0.0.1', 11111)
messaggio = struct.pack('>3i', 0xFFC01, 0xFFFFF48, 0xFFF49) 
while(True):
   client_socket.sendto(messaggio, DESTINAZIONE)

