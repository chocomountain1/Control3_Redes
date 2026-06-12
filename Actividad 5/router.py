import sys
from funciones_aux import parse_packet, create_packet
from checkear_rutas import check_routes
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

# Recibir mensajes. Este método nos entrega el mensaje junto a la dirección de origen del mensaje, además que escucha de forma bloqueante por defecto
while True:
    print("Router escuchando en {}:{}".format(router_ip, router_puerto))
    message, address = dgram_socket.recvfrom(1024)

    print("Mensaje recibido de {}: {}".format(address, message))
    # Aquí se debería revisar el mensaje recibido, parsearlo, revisar las rutas y enviar el mensaje al siguiente salto si es necesario.
    parsed_message = parse_packet(message)

    destination_address = (".".join(map(str, parsed_message["destination_ip"])),int.from_bytes(parsed_message["destination_port"], "big"))
    next_hop = check_routes(router_rutas, destination_address)

    if next_hop is not None:
        print("Enviando mensaje al siguiente salto: {}".format(next_hop))
        next_hop_ip, next_hop_port = next_hop
        new_packet = create_packet(parsed_message)
        dgram_socket.sendto(new_packet, (next_hop_ip, next_hop_port))
    else:
        print("No se encontró una ruta para el mensaje con destino {}:{}".format(destination_address[0], destination_address[1]))


