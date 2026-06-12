import sys

router_ip = sys.argv[1]
router_puerto = int(sys.argv[2])
router_rutas = sys.argv[3]

print(f"Router IP: {router_ip}")
print(f"Router Puerto: {router_puerto}")
print(f"Router Rutas: {router_rutas}")

import socket
 
# Socket no orientado a conexión
dgram_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dgram_socket.bind((router_ip, router_puerto))

# Recibir mensajes. Este método nos entrega el mensaje junto a la dirección de origen del mensaje
message, address = dgram_socket.recvfrom(1024)

# Enviar mensajes. Este método debe especificar la dirección a la que se va a enviar el mensaje
dgram_socket.sendto(message, address)

ip_bytes = b""
for i in router_ip.split("."):
    byte = int(i).to_bytes(1, "big")
    ip_bytes += byte

puerto_bytes = router_puerto.to_bytes(2, "big")

mensaje_bytes = message.encode()
paquete = ip_bytes + puerto_bytes + mensaje_bytes
