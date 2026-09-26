"""
Ejercicio 2 - Proceso B: quien responde la petición
----------------------------------------------------------------
Escucha en SU propio puerto (distinto al de A) y va avanzando el
protocolo según los mensajes que recibe de cada dirección (ip, puerto).
Guarda el estado de cada "conversación" en un diccionario, así puede
atender a varios procesos A al mismo tiempo.

Uso:
    python3 proceso_b.py --puerto_local 7000
"""

import argparse
import socket

# Estado por cada dirección (ip, puerto) de origen: qué protocolo pidió
# y qué contenido tenía la petición original.
estado = {}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--puerto_local", type=int, default=7000)
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", args.puerto_local))
    print(f"[Proceso B] escuchando en puerto {args.puerto_local}\n")

    while True:
        data, addr = sock.recvfrom(4096)
        msg = data.decode()

        if msg.startswith("REQ:"):
            _, vias, contenido = msg.split(":", 2)
            vias = int(vias)
            print(f"A({addr}) -> B : REQ ({vias} vías) contenido='{contenido}'")

            if vias == 2:
                # sin pasos intermedios: respondemos directo
                respuesta = f"RESP:{contenido.upper()}"
                sock.sendto(respuesta.encode(), addr)
                print(f"B -> A({addr}) : {respuesta}")
            else:
                # guardamos el estado y mandamos el ACK
                estado[addr] = {"vias": vias, "contenido": contenido}
                sock.sendto(b"ACK:recibido", addr)
                print(f"B -> A({addr}) : ACK:recibido")

        elif msg == "CONFIRM":
            info = estado.get(addr)
            if info:
                respuesta = f"RESP:{info['contenido'].upper()}"
                sock.sendto(respuesta.encode(), addr)
                print(f"A({addr}) -> B : CONFIRM")
                print(f"B -> A({addr}) : {respuesta}")

        elif msg == "ACK_FINAL":
            print(f"A({addr}) -> B : ACK_FINAL  (protocolo de 4 vías completo)\n")
            estado.pop(addr, None)


if __name__ == "__main__":
    main()
