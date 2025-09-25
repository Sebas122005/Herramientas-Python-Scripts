#!/usr/bin/env python3
"""
hasher_interactivo.py
Programa interactivo que genera hashes (md5, sha1, sha256, sha512).
Guarda todos los resultados en un archivo JSONL (un JSON por línea).
"""

import hashlib
import sys
import json
from datetime import datetime
from pathlib import Path

CHUNK_SIZE = 8 * 1024  # 8 KB

ALGORITHMS = {
    "1": ("md5", hashlib.md5),
    "2": ("sha1", hashlib.sha1),
    "3": ("sha256", hashlib.sha256),
    "4": ("sha512", hashlib.sha512),
}

LOG_FILE = Path("hashes.jsonl")


def hash_file(path: Path, algo_constructor):
    h = algo_constructor()
    with path.open("rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            h.update(chunk)
    return h.hexdigest(), path.stat().st_size


def hash_string(s: str, algo_constructor):
    h = algo_constructor()
    h.update(s.encode("utf-8"))
    return h.hexdigest(), len(s)


def hash_stdin(algo_constructor):
    h = algo_constructor()
    size = 0
    while chunk := sys.stdin.buffer.read(CHUNK_SIZE):
        size += len(chunk)
        h.update(chunk)
    return h.hexdigest(), size


def save_record(record: dict):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    print("=== Generador de Hashes (interactivo) ===\n")
    print("Selecciona el tipo de entrada:")
    print("1) String")
    print("2) Archivo")
    print("3) STDIN (pegar datos con pipe)\n")

    tipo_op = input("Opción (1-3): ").strip()

    if tipo_op == "1":
        dato = input("Ingresa el texto a hashear: ")
        tipo = "string"
        etiqueta = input("Etiqueta opcional (Enter para usar inicio del texto): ").strip() or dato[:64]
        source = dato
    elif tipo_op == "2":
        ruta = input("Ruta al archivo: ").strip()
        path = Path(ruta)
        if not path.exists():
            print("❌ Archivo no encontrado.")
            return
        tipo = "file"
        etiqueta = input("Etiqueta opcional (Enter para usar nombre del archivo): ").strip() or path.name
        source = path
    elif tipo_op == "3":
        print("Espera datos desde STDIN (ejemplo: cat archivo.txt | python3 hasher_interactivo.py)")
        tipo = "stdin"
        etiqueta = input("Etiqueta opcional (Enter para usar 'stdin-data'): ").strip() or "stdin-data"
        source = None
    else:
        print("❌ Opción inválida.")
        return

    print("\nSelecciona algoritmo de hash:")
    for k, (name, _) in ALGORITHMS.items():
        print(f"{k}) {name}")
    algo_op = input("Opción (1-4): ").strip()

    if algo_op not in ALGORITHMS:
        print("❌ Algoritmo inválido.")
        return

    algoritmo, constructor = ALGORITHMS[algo_op]

    if tipo == "string":
        digest, size = hash_string(source, constructor)
    elif tipo == "file":
        digest, size = hash_file(source, constructor)
    else:  # stdin
        digest, size = hash_stdin(constructor)

    record = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tipo": tipo,
        "etiqueta": etiqueta,
        "algoritmo": algoritmo,
        "digest": digest,
        "size": size,
    }

    save_record(record)

    print("\n✅ Hash generado y registrado en 'hashes.jsonl':\n")
    print(json.dumps(record, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
