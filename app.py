from flask import Flask, render_template
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# ============================================================
# CONSTANTES ITU-T G.694.1
# ============================================================
C = 2.99792458e8      # m/s
F_REF = 193.1         # THz
DELTA_F = 0.0125      # THz (12.5 GHz)

# Rango ilustrativo (C + L)
F_MIN = 184.5000
F_MAX = 195.9375


# ============================================================
# FUNCIONES
# ============================================================
def frecuencia_a_lambda_nm(f_thz):
    return (C / (f_thz * 1e12)) * 1e9


def generar_tablas_dwdm():
    tablas = {
        "12.5 GHz": [],
        "25 GHz": [],
        "50 GHz": [],
        "100 GHz": []
    }

    n_min = int(round((F_MIN - F_REF) / DELTA_F))
    n_max = int(round((F_MAX - F_REF) / DELTA_F))

    for n in range(n_min, n_max + 1):
        f = round(F_REF + n * DELTA_F, 4)
        lambda_nm = round(frecuencia_a_lambda_nm(f), 4)

        fila = {
            "n": n,
            "f": f,
            "lambda": lambda_nm
        }

        tablas["12.5 GHz"].append(fila)

        if n % 2 == 0:
            tablas["25 GHz"].append(fila)

        if n % 4 == 0:
            tablas["50 GHz"].append(fila)

        if n % 8 == 0:
            tablas["100 GHz"].append(fila)

    return tablas


def generar_graficos(tablas):
    os.makedirs("static", exist_ok=True)

    for nombre, filas in tablas.items():
        n_vals = [f["n"] for f in filas]
        f_vals = [f["f"] for f in filas]

        plt.figure(figsize=(9, 4))
        plt.stem(n_vals, f_vals, basefmt=" ")
        plt.xlabel("Índice n")
        plt.ylabel("Frecuencia central (THz)")
        plt.title(f"Rejilla DWDM – Espaciamiento {nombre}")
        plt.grid(True)

        nombre_archivo = nombre.replace(" ", "_").replace(".", "")
        plt.savefig(f"static/grafico_{nombre_archivo}.png", dpi=150)
        plt.close()


# ============================================================
# RUTA PRINCIPAL
# ============================================================
@app.route("/")
def index():
    tablas = generar_tablas_dwdm()
    generar_graficos(tablas)
    return render_template("index.html", tablas=tablas)


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
