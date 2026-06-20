from funciones_aux import create_packet, parse_packet

def fragment_IP_packet(IP_packet: bytes, mtu: int):
    size_ip_packet = len(IP_packet)
    if size_ip_packet <= mtu:
        return [IP_packet]
    parsed_packet = parse_packet(IP_packet)
    headers = IP_packet[:15]
    payload = IP_packet[15:]
    largo_fragmentos = mtu - len(headers)
    fragments = []
    #Este for es el encargado de generar los fragmentos con los headers actualizados
    for i in range(0,len(payload), largo_fragmentos):
        trozo = payload[i:i+largo_fragmentos]
        
        #Creamos los nuevos campos de cada fragmento
        new_size = (len(headers) + len(trozo)).to_bytes(4,"big")
        if i + largo_fragmentos >= len(payload):
            new_flag = int(0).to_bytes(1,"big")
        else:
            new_flag = int(1).to_bytes(1, "big")
        new_offset = i.to_bytes(2, "big")

        #Creamos una estructura de paquete ip parseado
        packet_info = {
        "destination_ip": parsed_packet["destination_ip"],
        "destination_port": parsed_packet["destination_port"],
        "ttl": parsed_packet["ttl"],
        "id": parsed_packet["id"],
        "offset": new_offset,
        "size": new_size,
        "flag": new_flag,
        "message": trozo
        }
        
        #Finalmente creamos un paquete de tipo ip con la funcion auxiliar
        fragment = create_packet(packet_info)
        #Lo añadimos en la lista de fragmentos
        fragments.append(fragment)
    return fragments
        