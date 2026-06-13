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

    # Aquí se debería revisar el mensaje recibido, parsearlo, revisar las rutas y enviar el mensaje al siguiente salto si es necesario.
    parsed_message = parse_packet(message)

    destination_address = (".".join(map(str, parsed_message["destination_ip"])),int.from_bytes(parsed_message["destination_port"], "big"))
    
    #Si el mensaje tiene como destino este router, lo imprimimos y no lo reenviamos a ningún otro router
    if destination_address[0] == router_ip and destination_address[1] == router_puerto:
        print("Mensaje recibido con destino a este router: {}".format(parsed_message["message"]))
        continue
    
    #Si no entonces chequeamos las rutas para ver si hay una ruta que coincida con la dirección de destino del mensaje
    next_hop = check_routes(router_rutas, destination_address)

    if next_hop is not None:
        next_hop_ip, next_hop_port = next_hop
        new_packet = create_packet(parsed_message)
        dgram_socket.sendto(new_packet, (next_hop_ip, next_hop_port))
        print(f"Redirigiendo paquete {new_packet} con destino final {destination_address} hacia {next_hop}")
    else:
        print(f"No hay rutas hacia {destination_address} para el paquete con mensaje: {parsed_message['message']}")


