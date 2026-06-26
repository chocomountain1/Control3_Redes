import sys
import socket

IP_router_final = sys.argv[1]
puerto_router_final = int(sys.argv[2])
ttl = int(sys.argv[3])
id = int(sys.argv[4])
offset = int(sys.argv[5])
tamaño = int(sys.argv[6])
flag = int(sys.argv[7])
IP_router_envio = sys.argv[8]
puerto_router_envio = int(sys.argv[9])
mensaje = sys.argv[10] #Asumimos que es un string

#Creamos el paquete con la información del mensaje
ip_bytes = b""
for i in IP_router_final.split("."):
    byte = int(i).to_bytes(1, "big")
    ip_bytes += byte

puerto_bytes = puerto_router_final.to_bytes(2, "big")
ttl_bytes = ttl.to_bytes(1, "big")
id_bytes = id.to_bytes(2, "big")
offset_bytes = offset.to_bytes(2, "big")
tamaño_bytes = tamaño.to_bytes(4, "big")
flag_bytes = flag.to_bytes(1, "big")
mensaje_bytes = mensaje.encode()

paquete = ip_bytes + puerto_bytes + ttl_bytes + id_bytes + offset_bytes + tamaño_bytes + flag_bytes + mensaje_bytes

#Finalmente mandamos el mensaje al router de envío

dgram_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dgram_socket.sendto(paquete, (IP_router_envio, puerto_router_envio))