"""
Ejercicio 3 - Cliente TCP (comunicación confiable)
----------------------------------------------------------------
Uso:
    python3 cliente_tcp.py <ip_servidor> [puerto]
"""

import socket
import sys

SERVER_IP = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
SERVER_PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8000


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    print(f"Conectado a {SERVER_IP}:{SERVER_PORT}")

    try:
        while True:
            mensaje = input("Mensaje > ")
            sock.sendall(mensaje.encode("utf-8"))

            if mensaje.lower() == "salir":
                break

            data = sock.recv(4096)
            if not data:
                print("El servidor cerró la conexión.")
                break
            print("Respuesta:", data.decode("utf-8"))
    finally:
        sock.close()


if __name__ == "__main__":
    main()
