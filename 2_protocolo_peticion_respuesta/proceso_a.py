"""
Ejercicio 2 - Proceso A: quien inicia la petición
----------------------------------------------------------------
Cada proceso usa un socket UDP propio, con SU puerto de escucha
(para recibir) distinto del puerto del otro proceso (al que envía).

Formato de mensajes:
    REQ:<vias>:<contenido>   -> pide algo, indicando el protocolo (2/3/4)
    CONFIRM                  -> confirma que recibió el ACK
    ACK_FINAL                -> confirma que recibió la respuesta final

Protocolos:
    2 vías:  REQ -> RESP
    3 vías:  REQ -> ACK -> CONFIRM -> RESP
    4 vías:  REQ -> ACK -> CONFIRM -> RESP -> ACK_FINAL

Uso:
    python3 proceso_a.py --vias 3 --puerto_local 6000 \\
            --ip_destino 127.0.0.1 --puerto_destino 7000
"""

import argparse
import socket


def protocolo_2vias(sock, destino, contenido):
    print("A -> B : REQ")
    sock.sendto(f"REQ:2:{contenido}".encode(), destino)

    data, _ = sock.recvfrom(4096)
    print(f"B -> A : {data.decode()}   (respuesta final)")


def protocolo_3vias(sock, destino, contenido):
    print("A -> B : REQ")
    sock.sendto(f"REQ:3:{contenido}".encode(), destino)

    data, _ = sock.recvfrom(4096)
    print(f"B -> A : {data.decode()}   (ACK)")

    print("A -> B : CONFIRM")
    sock.sendto(b"CONFIRM", destino)

    data, _ = sock.recvfrom(4096)
    print(f"B -> A : {data.decode()}   (respuesta final)")


def protocolo_4vias(sock, destino, contenido):
    print("A -> B : REQ")
    sock.sendto(f"REQ:4:{contenido}".encode(), destino)

    data, _ = sock.recvfrom(4096)
    print(f"B -> A : {data.decode()}   (ACK)")

    print("A -> B : CONFIRM")
    sock.sendto(b"CONFIRM", destino)

    data, _ = sock.recvfrom(4096)
    print(f"B -> A : {data.decode()}   (respuesta final)")

    print("A -> B : ACK_FINAL")
    sock.sendto(b"ACK_FINAL", destino)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--puerto_local", type=int, default=6000,
                         help="puerto donde ESTE proceso escucha respuestas")
    parser.add_argument("--ip_destino", default="127.0.0.1",
                         help="IP del proceso B")
    parser.add_argument("--puerto_destino", type=int, default=7000,
                         help="puerto donde escucha el proceso B")
    parser.add_argument("--vias", type=int, choices=[2, 3, 4], default=2)
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", args.puerto_local))
    destino = (args.ip_destino, args.puerto_destino)

    contenido = input("Contenido de la petición > ")

    if args.vias == 2:
        protocolo_2vias(sock, destino, contenido)
    elif args.vias == 3:
        protocolo_3vias(sock, destino, contenido)
    else:
        protocolo_4vias(sock, destino, contenido)


if __name__ == "__main__":
    main()
