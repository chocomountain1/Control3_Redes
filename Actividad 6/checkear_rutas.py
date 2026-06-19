# Memoria global para el round-robin entre las rutas posibles
# La clave se basa en la tabla de rutas y en la dirección de destino solicitada
_ROUND_ROBIN_STATE: dict[tuple[str, str, int], int] = {}


def _matching_routes(routes_file_name: str, destination_address: tuple[str, int]) -> list[tuple[str, int]]:
    matches = []

    with open(routes_file_name, "r", encoding="utf-8") as routes_file:
        for line in routes_file:
            route_info = line.strip().split()
            if len(route_info) != 6:
                continue

            destination_ip, destination_port_i, destination_port_f, next_hop_ip, next_hop_port, mtu = route_info
            destination_ip = destination_ip.split("/")[0]
            destination_port_i = int(destination_port_i)
            destination_port_f = int(destination_port_f)
            next_hop_port = int(next_hop_port)
            mtu = int(mtu)

            if destination_address[0] == destination_ip and destination_port_i <= destination_address[1] <= destination_port_f:
                matches.append((next_hop_ip, next_hop_port))

    return (matches, mtu)


def check_routes(routes_file_name: str, destination_address: tuple[str, int]) -> tuple[str, int] | None:
    """Devuelve una ruta candidata usando round-robin sobre todas las coincidencias válidas."""
    matches, mtu = _matching_routes(routes_file_name, destination_address)
    if not matches:
        return None

    state_key = (routes_file_name, destination_address[0], destination_address[1])
    current_index = _ROUND_ROBIN_STATE.get(state_key, 0)
    next_hop = matches[current_index % len(matches)]
    _ROUND_ROBIN_STATE[state_key] = (current_index + 1) % len(matches)

    return (next_hop, mtu)

