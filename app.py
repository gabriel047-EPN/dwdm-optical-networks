from flask import Flask, render_template
import os

app = Flask(__name__)

# ============================================================
# CONSTANTES ITU-T G.694.1
# ============================================================
C = 2.99792458e8      # m/s
F_REF = 193.1         # THz
DELTA_F = 0.0125      # THz (12.5 GHz)

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


# ============================================================
# RUTA WEB
# ============================================================
@app.route("/")
def index():
    tablas = generar_tablas_dwdm()
    return render_template("index.html", tablas=tablas)


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
