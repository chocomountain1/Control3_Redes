import sys 

headers = sys.argv[1]
IP_router_inicical = sys.argv[2]
puerto_router_inicial = int(sys.argv[3])

#Ahora mandamos cada línea de headers al router inicial usando un socket UDP
import socket

with open(headers, "r", encoding="utf-8") as headers_file:
    for line in headers_file:
        destination_ip, destination_port, ttl, message = line.split(";")
        if not line:
            continue
        #Creamos el paquete con la información del mensaje
        ip_bytes = b""
        for i in destination_ip.split("."):
            byte = int(i).to_bytes(1, "big")
            ip_bytes += byte
        
        puerto_bytes = int(destination_port).to_bytes(2, "big")
        ttl_bytes = int(ttl).to_bytes(1, "big")
        message_bytes = message.encode()
        paquete = ip_bytes + puerto_bytes + ttl_bytes + message_bytes
        
        # Creamos un socket UDP
        dgram_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Enviamos el mensaje al router inicial
        dgram_socket.sendto(paquete, (IP_router_inicical, puerto_router_inicial))
        print(f"Mensaje enviado al router {IP_router_inicical}:{puerto_router_inicial} -> {line}")