from funciones_aux import create_packet, parse_packet

def reassemble_IP_packet(fragment_list: list[bytes]):

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
    reassemble_packet["size"] = (16 + len(mensaje)).to_bytes(4,"big")
    reassemble_packet["message"] = mensaje

    #Esto es solo para discriminar si es momento de printear o no el reensamblaje
    ultimo = ordered_list[-1]

    ultimo_offset = int.from_bytes(parse_packet(ultimo)["offset"], "big")
    ultimo_size = len(parse_packet(ultimo)["message"])

    expected_size = ultimo_offset + ultimo_size

    expected_offset = 0

    for fragment in ordered_list:
        p = parse_packet(fragment)

        offset = int.from_bytes(p["offset"], "big")

        if offset != expected_offset:
            return None

        expected_offset += len(p["message"])

    if expected_offset != expected_size:
        return None
    return create_packet(reassemble_packet)
