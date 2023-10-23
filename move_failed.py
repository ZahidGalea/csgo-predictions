import shutil

if __name__ == "__main__":
    file = open("data/.log")
    data = file.read()
    file.close()
    data = data.split("\n")
    for row in data:
        if "Failed to upload" in row:
            file = row.split("/")[-1]
            ruta_origen = f"data/processed/matches/{file}"
            ruta_destino = f"data/matches/{file}"
            shutil.move(ruta_origen, ruta_destino)
            print(file)
