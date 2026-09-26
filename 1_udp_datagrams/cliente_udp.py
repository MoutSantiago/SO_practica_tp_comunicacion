"""
Ejercicio 1 - Cliente UDP (interfaz de sockets con datagramas)
----------------------------------------------------------------
Uso:
    python3 cliente_udp.py <ip_servidor> [puerto]

Si no se pasa IP, usa 127.0.0.1 (localhost). Para comunicar dos
computadoras distintas, reemplazá <ip_servidor> por la IP real de la
máquina donde corre servidor_udp.py (ej: 192.168.1.10).
"""

import socket
import sys

SERVER_IP = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
SERVER_PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5000


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destino = (SERVER_IP, SERVER_PORT)
    print(f"[Cliente UDP] enviando a {SERVER_IP}:{SERVER_PORT}")
    print("Escribí 'salir' para terminar.\n")

    while True:
        mensaje = input("Mensaje > ")
        sock.sendto(mensaje.encode("utf-8"), destino)

        if mensaje.lower() == "salir":
            break

        data, _ = sock.recvfrom(4096)
        print("Respuesta del servidor:", data.decode("utf-8"))


if __name__ == "__main__":
    main()
