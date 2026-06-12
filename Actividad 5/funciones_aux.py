def parse_packet(IP_packet: bytes) -> dict:
    # Extraer la dirección IP de destino del paquete
    destination_ip_bytes = IP_packet[0:4]

    # Extraer el puerto de destino del paquete
    destination_port_bytes = IP_packet[4:6]

    #Extraer el mensaje del paquete
    message_bytes = IP_packet[6:]

    #Lo pasamos a una estructura de tipo diccionario, con la ip de destino en string, el puerto de destino como entero y el mensaje como string
    packet_info = {
        "destination_ip": destination_ip_bytes,
        "destination_port": destination_port_bytes,
        "message": message_bytes
    }
    return packet_info

def create_packet(parsed_IP_packet: dict) -> bytes:
    # Convertir la dirección IP de destino a bytes
    destination_ip_bytes = parsed_IP_packet["destination_ip"]

    # Convertir el puerto de destino a bytes
    destination_port_bytes = parsed_IP_packet["destination_port"]

    # Obtener el mensaje en bytes
    message_bytes = parsed_IP_packet["message"]

    # Crear el paquete concatenando los bytes de la dirección IP, el puerto y el mensaje
    packet = destination_ip_bytes + destination_port_bytes + message_bytes

    return packet

#Test de las funciones
if __name__ == "__main__":
    # Creamos un paquete de ejemplo en bytes
    router_ip = "127.0.0.1"
    router_puerto = 8882
    message = "Hello, World!"
    example_packet = "127.0.0.1/24 8882 8882 127.0.0.1 8882"
    ip_bytes = b""
    
    for i in router_ip.split("."):
        byte = int(i).to_bytes(1, "big")
        ip_bytes += byte

    puerto_bytes = router_puerto.to_bytes(2, "big")

    mensaje_bytes = message.encode()
    paquete = ip_bytes + puerto_bytes + mensaje_bytes

    #Parseamos el mensaje
    parsed_IP_packet = parse_packet(paquete)
    IP_packet_v2 = create_packet(parsed_IP_packet)
    print("IP_packet_v1 == IP_packet_v2 ? {}".format(paquete == IP_packet_v2))