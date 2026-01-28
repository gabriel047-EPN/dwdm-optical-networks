from flask import Flask, render_template
import math

app = Flask(__name__)

# ============================================================
# CONSTANTES ITU-T G.694.1
# ============================================================
C = 2.99792458e8      # Velocidad de la luz (m/s)
F_REF = 193.1         # Frecuencia de referencia (THz)
DELTA_F = 0.0125      # Granularidad mínima (THz)

# Rango ilustrativo (bandas C + L)
F_MIN = 184.5000
F_MAX = 195.9375


# ============================================================
# FUNCIONES
# ============================================================
def frecuencia_a_lambda_nm(f_thz):
    """Convierte frecuencia (THz) a longitud de onda aproximada (nm)"""
    return (C / (f_thz * 1e12)) * 1e9


def generar_tablas_dwmd():
    """
    Genera tablas DWDM separadas por espaciamiento
    conforme a ITU-T G.694.1
    """

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

        tablas["12.5 GHz"].append((n, f, lambda_nm))

        if n % 2 == 0:
            tablas["25 GHz"].append((n, f, lambda_nm))

        if n % 4 == 0:
            tablas["50 GHz"].append((n, f, lambda_nm))

        if n % 8 == 0:
            tablas["100 GHz"].append((n, f, lambda_nm))

    return tablas


# ============================================================
# RUTA WEB
# ============================================================
@app.route("/")
def index():
    tablas = generar_tablas_dwmd()
    return render_template("index.html", tablas=tablas)


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)

