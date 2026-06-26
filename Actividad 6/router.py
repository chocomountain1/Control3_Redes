import sys
from funciones_aux import parse_packet, create_packet
from checkear_rutas import check_routes
from fragment_IP_packet import fragment_IP_packet
from reassemble_IP_packet import reassemble_IP_packet
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


#Diccionario que guarda los mensajes recibidos por este router
fragmentos = {}


# Recibir mensajes. Este método nos entrega el mensaje junto a la dirección de origen del mensaje, además que escucha de forma bloqueante por defecto
while True:
    print("Router escuchando en {}:{}".format(router_ip, router_puerto))
    message, address = dgram_socket.recvfrom(1024)

    # Aquí se debería revisar el mensaje recibido, parsearlo, revisar las rutas y enviar el mensaje al siguiente salto si es necesario.
    parsed_message = parse_packet(message)

    if int.from_bytes(parsed_message["ttl"], "big") <= 0:
        print(f"Se recibió paquete {parsed_message} con TTL 0")
        continue

    destination_address = (".".join(map(str, parsed_message["destination_ip"])),int.from_bytes(parsed_message["destination_port"], "big"))
    
    #Si el mensaje tiene como destino este router, lo imprimimos y no lo reenviamos a ningún otro router
    if destination_address[0] == router_ip and destination_address[1] == router_puerto:
        print("Mensaje recibido con destino a este router: {}".format(parsed_message["message"]))
        id = int.from_bytes(parsed_message["id"], "big")
        if id not in fragmentos:
            fragmentos[id] = []
        fragmentos[id].append(create_packet(parsed_message))

        packet = reassemble_IP_packet(fragmentos[id])

        if packet is not None:
            print(parse_packet(packet)["message"])
            del fragmentos[id]
        continue
    
    #Si no entonces chequeamos las rutas para ver si hay una ruta que coincida con la dirección de destino del mensaje
    next_hop, mtu = check_routes(router_rutas, destination_address)

    if next_hop is not None:
        next_hop_ip, next_hop_port = next_hop
        #Antes de crear el nuevo paquete, debemos decrementar el ttl del mensaje en 1
        parsed_message["ttl"] = (int.from_bytes(parsed_message["ttl"], "big") - 1).to_bytes(1, "big")
        new_packet = create_packet(parsed_message)

        #Ahora como tenemos mtu vemos si es que es necesario fragmentar
        fragments = fragment_IP_packet(new_packet,mtu)

        for fragment in fragments:
            dgram_socket.sendto(fragment, (next_hop_ip, next_hop_port))
            print(f"Redirigiendo paquete {fragment} con destino final {destination_address} hacia {next_hop}")
    else:
        print(f"No hay rutas hacia {destination_address} para el paquete con mensaje: {parsed_message['message']}")


