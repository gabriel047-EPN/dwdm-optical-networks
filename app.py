from flask import Flask, render_template
import os

app = Flask(__name__)

# ============================================================
# CONSTANTES ITU-T G.694.1
# ============================================================
C = 2.99792458e8      # Velocidad de la luz en el vacío (m/s)
F_REF = 193.1         # Frecuencia de referencia (THz)
DELTA_F = 0.0125      # Granularidad mínima (THz = 12.5 GHz)

# Rango ilustrativo (Bandas C + L)
F_MIN = 184.5
F_MAX = 195.9375


# ============================================================
# FUNCIONES DE CÁLCULO
# ============================================================
def frecuencia_a_lambda_nm(f_thz):
    """
    Convierte frecuencia (THz) a longitud de onda aproximada (nm)
    """
    return (C / (f_thz * 1e12)) * 1e9


def generar_tablas_dwdm():
    """
    Genera tablas DWDM separadas por espaciamiento de canal,
    siguiendo la recomendación ITU-T G.694.1.
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

        fila = {
            "n": n,
            "f": f,
            "lambda": lambda_nm
        }

        # Grid base (12.5 GHz)
        tablas["12.5 GHz"].append(fila)

        # Subgrids
        if n % 2 == 0:
            tablas["25 GHz"].append(fila)

        if n % 4 == 0:
            tablas["50 GHz"].append(fila)

        if n % 8 == 0:
            tablas["100 GHz"].append(fila)

    return tablas


def generar_flexible_grid(spacing_ghz):
    """
    Genera bloques espectrales tipo 'flexible grid'
    para representación gráfica ITU-T.
    """
    spacing_thz = spacing_ghz / 1000
    bloques = []

    n_min = int((193.0 - F_REF) / DELTA_F)
    n_max = int((193.35 - F_REF) / DELTA_F)

    for n in range(n_min, n_max + 1):
        f_c = F_REF + n * DELTA_F

        if abs((f_c - F_REF) / spacing_thz -
               round((f_c - F_REF) / spacing_thz)) < 1e-6:
            bloques.append({
                "n": n,
                "f": round(f_c, 5),
                "inicio": round(f_c - spacing_thz / 2, 5),
                "fin": round(f_c + spacing_thz / 2, 5)
            })

    return bloques


# ============================================================
# RUTA PRINCIPAL
# ============================================================
@app.route("/")
def index():
    tablas = generar_tablas_dwdm()
    flexible = {
        "50 GHz": generar_flexible_grid(50),
        "75 GHz": generar_flexible_grid(75)
    }
    return render_template("index.html",
                           tablas=tablas,
                           flexible=flexible)


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


