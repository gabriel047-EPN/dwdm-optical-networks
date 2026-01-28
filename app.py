from flask import Flask, render_template

app = Flask(__name__)

# ============================================================
# CONSTANTES ITU-T G.694.1
# ============================================================
C = 2.99792458e8      # Velocidad de la luz en el vacío (m/s)
F_REF = 193.1         # Frecuencia de referencia ITU (THz)
DELTA_F = 0.0125      # Granularidad mínima (THz = 12.5 GHz)

# Rango ilustrativo (bandas C + L)
# NOTA: Los extremos son ilustrativos, no normativos
F_MIN = 184.5000
F_MAX = 195.9375


# ============================================================
# FUNCIONES
# ============================================================
def frecuencia_a_lambda_nm(f_thz):
    """
    Convierte una frecuencia en THz a una longitud de onda
    aproximada en nanómetros (nm).
    """
    return (C / (f_thz * 1e12)) * 1e9


def generar_tablas_dwdm():
    """
    Genera tablas DWDM separadas por espaciamiento de canal
    conforme a la recomendación ITU-T G.694.1.

    Cada canal se representa como un diccionario para facilitar
    su uso en plantillas HTML (Jinja2).
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

        frecuencia = round(F_REF + n * DELTA_F, 4)
        longitud_onda = round(frecuencia_a_lambda_nm(frecuencia), 4)

        canal = {
            "n": n,
            "frecuencia": frecuencia,
            "longitud_onda": longitud_onda
        }

        # Grid base de 12.5 GHz (todos los canales)
        tablas["12.5 GHz"].append(canal)

        # Subgrids según ITU-T G.694.1
        if n % 2 == 0:
            tablas["25 GHz"].append(canal)

        if n % 4 == 0:
            tablas["50 GHz"].append(canal)

        if n % 8 == 0:
            tablas["100 GHz"].append(canal)

    return tablas


# ============================================================
# RUTA PRINCIPAL
# ============================================================
@app.route("/")
def index():
    tablas = generar_tablas_dwdm()
    return render_template("index.html", tablas=tablas)


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)
