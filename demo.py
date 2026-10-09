#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo para cliente: levanta server.py en modo DEMO (noindex) en un puerto libre
y expone el sitio por HTTPS con un quick tunnel de Cloudflare.
- La URL pública queda en demo-url.txt y se imprime en consola.
- Si el túnel se cae, se reinicia automáticamente.
Uso:  python demo.py        (o doble clic en demo-server.bat)
"""
import os
import re
import socket
import subprocess
import sys
import threading
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
CLOUDFLARED = os.path.join(ROOT, "tools", "cloudflared.exe")
URL_FILE = os.path.join(ROOT, "demo-url.txt")
BASE_PORT = int(os.environ.get("PORT", "8090"))
MAX_PORT_TRIES = 40


def free_port(start):
    for p in range(start, start + MAX_PORT_TRIES):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("0.0.0.0", p))
                return p
            except OSError:
                continue
    raise RuntimeError("No hay puertos libres cercanos a %d" % start)


def run_server(port):
    env = dict(os.environ, DEMO="1", PORT=str(port))
    return subprocess.Popen([sys.executable, os.path.join(ROOT, "server.py")], env=env)


def tunnel_loop(port, stop_event):
    """Mantiene vivo el quick tunnel; escribe la URL en demo-url.txt."""
    while not stop_event.is_set():
        try:
            proc = subprocess.Popen(
                [CLOUDFLARED, "tunnel", "--url", f"http://localhost:{port}", "--no-autoupdate"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors="replace",
            )
            url_found = False
            for line in proc.stdout:
                m = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", line)
                if m and not url_found:
                    url_found = True
                    url = m.group(0)
                    with open(URL_FILE, "w") as f:
                        f.write(url)
                    print("\n" + "=" * 60)
                    print("DEMO LISTA — comparte esta URL con el cliente:")
                    print("  " + url)
                    print("=" * 60 + "\n")
                if stop_event.is_set():
                    break
            proc.terminate()
        except Exception as e:
            print("[tunnel] error:", e)
        if not stop_event.is_set():
            print("[tunnel] se cayó; reiniciando en 5 s…")
            time.sleep(5)


def main():
    if not os.path.isfile(CLOUDFLARED):
        print("Falta tools/cloudflared.exe — cópialo desde otro proyecto (Roque/tools).")
        sys.exit(1)
    port = free_port(BASE_PORT)
    print(f"Servidor local: http://localhost:{port} (modo DEMO, noindex)")
    server = run_server(port)
    stop_event = threading.Event()
    t = threading.Thread(target=tunnel_loop, args=(port, stop_event), daemon=True)
    t.start()
    try:
        while server.poll() is None:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        stop_event.set()
        server.terminate()
        if os.path.exists(URL_FILE):
            os.remove(URL_FILE)
        print("Demo detenida. La URL anterior ya no funciona.")


if __name__ == "__main__":
    main()
