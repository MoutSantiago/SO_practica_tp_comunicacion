"""
Ejercicio 3 - Servidor TCP (comunicación confiable)
----------------------------------------------------------------
TCP garantiza entrega en orden y sin pérdidas a nivel de transporte
(retransmisiones, control de flujo, etc. los maneja el sistema
operativo). Acá solo manejamos bien la conexión: accept(), recv()
en bucle hasta que el cliente cierra o escribe 'salir'.

Uso:
    python3 servidor_tcp.py [puerto]
"""

import socket
import sys

HOST = "0.0.0.0"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


def atender_cliente(conn, addr):
    print(f"[+] Conexión establecida con {addr}")
    with conn:
        while True:
            data = conn.recv(4096)
            if not data:
                # el cliente cerró la conexión (recv devuelve b'')
                print(f"[-] {addr} cerró la conexión")
                break

            mensaje = data.decode("utf-8")
            print(f"[{addr}] {mensaje}")

            if mensaje.lower() == "salir":
                print(f"[-] {addr} pidió terminar")
                break

            respuesta = f"Eco: {mensaje}"
            conn.sendall(respuesta.encode("utf-8"))


def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen(5)
    print(f"[Servidor TCP] escuchando en {HOST}:{PORT}")

    try:
        while True:
            conn, addr = servidor.accept()
            atender_cliente(conn, addr)
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        servidor.close()


if __name__ == "__main__":
    main()
