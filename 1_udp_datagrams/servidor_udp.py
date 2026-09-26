"""
Ejercicio 1 - Servidor UDP (interfaz de sockets con datagramas)
----------------------------------------------------------------
Envía y recibe mensajes de texto usando sockets UDP (SOCK_DGRAM).
No hay conexión: cada mensaje viaja como un datagrama independiente.

Uso:
    python3 servidor_udp.py [puerto]

Por defecto escucha en el puerto 5000 en todas las interfaces.
"""

import socket
import sys

HOST = "0.0.0.0"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5000


def main():
    # AF_INET      -> IPv4
    # SOCK_DGRAM   -> UDP (datagramas, sin conexión)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[Servidor UDP] escuchando en {HOST}:{PORT}")
    print("Escribí 'salir' para terminar la conversación con un cliente.\n")

    while True:
        # recvfrom devuelve los datos Y la dirección (ip, puerto) del remitente
        data, addr = sock.recvfrom(4096)
        mensaje = data.decode("utf-8")
        print(f"[{addr[0]}:{addr[1]}] dice: {mensaje}")

        if mensaje.lower() == "salir":
            print("El cliente terminó la conversación.\n")
            continue

        respuesta = input("Tu respuesta > ")
        sock.sendto(respuesta.encode("utf-8"), addr)


if __name__ == "__main__":
    main()
