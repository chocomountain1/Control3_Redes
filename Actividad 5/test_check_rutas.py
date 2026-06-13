from checkear_rutas import check_routes

print (check_routes("rutas_R1.txt", ("127.0.0.1", 8882))) # ('127.0.0.1', 8882)
print (check_routes("rutas_R1.txt", ("127.0.0.1", 8884))) # None
print (check_routes("rutas_R2.txt", ("127.0.0.1", 8881))) # ('127.0.0.1', 8881)
print (check_routes("rutas_R2.txt", ("127.0.0.1", 8883))) # ('127.0.0.1', 8883)
print (check_routes("rutas_R2.txt", ("127.0.0.1", 8884))) # None
print (check_routes("rutas_R3.txt", ("127.0.0.1", 8882))) # ('127.0.0.1', 8882)