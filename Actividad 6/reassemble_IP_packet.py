from funciones_aux import create_packet, parse_packet

def reassemble_IP_packet(fragment_list: list[bytes]):
    if len(fragment_list) == 1:
        parsed = parse_packet(fragment_list[0])
        if parsed["flag"] == 0:
            return fragment_list[0]
        else:
            return None

    ordered_list = sorted(
        fragment_list,
        key=lambda f: int.from_bytes(parse_packet(f)["offset"], "big")
    )
    
    mensaje = b""
    for fragment in ordered_list:
        mensaje += parse_packet(fragment)["message"]

    #Tomamos el header del primer fragmento
    reassemble_packet = parse_packet(ordered_list[0])

    #Mutamos el header
    reassemble_packet["offset"] = int(0).to_bytes(2,"big")
    reassemble_packet["flag"] = int(0).to_bytes(1,"big")
    reassemble_packet["size"] = (15 + len(mensaje)).to_bytes(4,"big")
    reassemble_packet["message"] = mensaje

    return create_packet(reassemble_packet)
