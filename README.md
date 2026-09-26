# TP2 - Sockets: Datagramas, Protocolo Petición-Respuesta y TCP Confiable

Trabajo práctico de Sistemas Operativos / Redes. Implementación de comunicación
entre procesos usando la interfaz de sockets de Python (módulo `socket`), sin
dependencias externas.

## Requisitos

- Python 3.8 o superior (no requiere instalar ninguna librería adicional).
- Dos terminales (o dos computadoras en la misma red) para probar cada ejercicio.

Verificar la versión instalada:

```bash
python3 --version
```

## Estructura del repositorio

```
.
├── 1_udp_datagramas/
│   ├── servidor_udp.py
│   └── cliente_udp.py
├── 2_protocolo_peticion_respuesta/
│   ├── proceso_a.py
│   └── proceso_b.py
├── 3_tcp_confiable/
│   ├── servidor_tcp.py
│   └── cliente_tcp.py
└── README.md
```

---

## Ejercicio 1 — Sockets UDP (datagramas)

Comunicación de mensajes de texto entre dos procesos usando `SOCK_DGRAM` (UDP),
sin conexión previa.

**Ejecución (misma máquina):**

Terminal 1:
```bash
cd 1_udp_datagramas
python3 servidor_udp.py
```

Terminal 2:
```bash
cd 1_udp_datagramas
python3 cliente_udp.py 127.0.0.1
```

**Ejecución entre dos computadoras:**

En la máquina servidor, averiguar la IP de red:
```bash
ip addr show
```

En la máquina cliente:
```bash
python3 cliente_udp.py <IP_DEL_SERVIDOR>
```

Ambas máquinas deben estar en la misma red (mismo wifi/switch), o conectadas
mediante una VPN tipo Tailscale si están en redes distintas.

Escribir `salir` en el cliente para terminar la conversación.

---

## Ejercicio 2 — Protocolo petición-respuesta (2, 3 y 4 vías)

Dos procesos (A y B) se comunican por UDP, cada uno escuchando en **su propio
puerto**. El Proceso A inicia la petición; el Proceso B responde siguiendo el
protocolo indicado.

| Protocolo | Secuencia de mensajes                          |
|-----------|--------------------------------------------------|
| 2 vías    | `REQ → RESP`                                      |
| 3 vías    | `REQ → ACK → CONFIRM → RESP`                      |
| 4 vías    | `REQ → ACK → CONFIRM → RESP → ACK_FINAL`          |

**Ejecución:**

Terminal 1 (Proceso B, arranca primero y queda escuchando):
```bash
cd 2_protocolo_peticion_respuesta
python3 proceso_b.py --puerto_local 7000
```

Terminal 2 (Proceso A):
```bash
python3 proceso_a.py --vias 2 --puerto_local 6000 --ip_destino 127.0.0.1 --puerto_destino 7000
python3 proceso_a.py --vias 3 --puerto_local 6001 --ip_destino 127.0.0.1 --puerto_destino 7000
python3 proceso_a.py --vias 4 --puerto_local 6002 --ip_destino 127.0.0.1 --puerto_destino 7000
```

Cada ejecución pide el contenido de la petición por consola. La consola del
Proceso B muestra en tiempo real cada mensaje intercambiado según el protocolo
elegido.

**Argumentos disponibles (`proceso_a.py`):**

| Argumento           | Descripción                                    | Default     |
|---------------------|-------------------------------------------------|-------------|
| `--puerto_local`     | Puerto donde este proceso escucha respuestas    | `6000`      |
| `--ip_destino`       | IP del Proceso B                                | `127.0.0.1` |
| `--puerto_destino`   | Puerto donde escucha el Proceso B                | `7000`      |
| `--vias`             | Cantidad de vías del protocolo (`2`, `3` o `4`) | `2`         |

---

## Ejercicio 3 — Comunicación confiable con TCP

Servidor y cliente sobre `SOCK_STREAM` (TCP). El servidor acepta conexiones y
responde con un eco de cada mensaje recibido.

**Ejecución (misma máquina):**

Terminal 1:
```bash
cd 3_tcp_confiable
python3 servidor_tcp.py
```

Terminal 2:
```bash
cd 3_tcp_confiable
python3 cliente_tcp.py 127.0.0.1
```

Escribir `salir` en el cliente para cerrar la conexión prolijamente.

---

## Solución de problemas

**`OSError: [Errno 98] Address already in use`**
El puerto quedó ocupado por una ejecución anterior. Identificar el proceso y
matarlo, o usar otro puerto:
```bash
sudo ss -tulpn | grep <puerto>
kill <PID>
```
o directamente correr el script pasando otro número de puerto por argumento.

**`Connection refused` (TCP)**
El servidor no está corriendo, o la IP/puerto indicados están mal.

**No conecta entre dos computadoras**
Verificar que ambas estén en la misma red y que no haya un firewall
(`ufw`/`firewalld`) bloqueando el puerto en la máquina servidor.

## Autor

Santiago — Sistemas Operativos, TP2.
