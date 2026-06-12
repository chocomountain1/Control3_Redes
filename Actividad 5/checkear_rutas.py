# Función para revisar las rutas en el archivo de rutas y determinar si la dirección de destino coincide con alguna ruta, devolviendo la dirección del siguiente salto si es así.
# Se espera que el address de destiono tenga el formato (IP, puerto) con la IP en formato string y sin la mascara de subred y el puerto como entero.
def check_routes(routes_file_name: str, destination_address: tuple[str, int]) -> tuple[str, int] |None:
    with open(routes_file_name, "r") as routes_file:
        for line in routes_file:
            #Cada línea del archivo de rutas debiese tener el formato: "destination_ip/subnet_mask next_hop_port next_hop_ip next_hop_port_2"
            route_info = line.strip().split()
            if len(route_info) != 5:
                continue
            
            destination_ip, destination_port_i, destination_port_f, next_hop_ip, next_hop_port = route_info
            destination_ip = destination_ip.split("/")[0] #Obtenemos la dirección IP sin la mascara de subred
            destination_port_i = int(destination_port_i)
            destination_port_f = int(destination_port_f)
            next_hop_port = int(next_hop_port)

            # Verificar si la dirección de destino coincide con la ruta y si el puerto de destino está dentro del rango especificado por la ruta
            if destination_address[0] == destination_ip and destination_port_i <= destination_address[1] <= destination_port_f:
                return (next_hop_ip, next_hop_port)

    return None

