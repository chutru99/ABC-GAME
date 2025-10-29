import pickle

# Nombre del archivo original
ARCHIVO_TEXTO = "listado-general.txt"
ARCHIVO_BINARIO = "palabras.pkl"

# Leer el archivo de texto
with open(ARCHIVO_TEXTO, "r", encoding="utf-8") as f:
    palabras = [line.strip().lower() for line in f if line.strip()]

print(f"Se cargaron {len(palabras):,} palabras del archivo de texto.")

# Guardar en formato binario (pickle)
with open(ARCHIVO_BINARIO, "wb") as f:
    pickle.dump(palabras, f)

print(f"Archivo binario '{ARCHIVO_BINARIO}' creado correctamente.")
