from flask import Flask, render_template
import os

app = Flask(__name__)

# ============================================================
# CONSTANTES DWDM – ITU-T G.694.1
# ============================================================
C = 2.99792458e8      # Velocidad de la luz (m/s)
F_REF = 193.1         # Frecuencia de referencia (THz)
DELTA_F = 0.0125      # Granularidad mínima (THz = 12.5 GHz)

F_MIN = 184.5000
F_MAX = 195.9375


# ============================================================
# FUNCIONES DWDM
# ============================================================
def frecuencia_a_lambda_nm(f_thz):
    """Convierte frecuencia (THz) a longitud de onda (nm)"""
    return (C / (f_thz * 1e12)) * 1e9


def generar_tabla_itu():
    """
    Genera la tabla ITU-T G.694.1 (tipo Tabla 1)
    basada en el grid mínimo de 12.5 GHz
    """
    tabla = []

    n_min = int(round((F_MIN - F_REF) / DELTA_F))
    n_max = int(round((F_MAX - F_REF) / DELTA_F))

    for n in range(n_min, n_max + 1):
        f = round(F_REF + n * DELTA_F, 4)

        fila = {
            "f_12": f,
            "f_25": f if n % 2 == 0 else None,
            "f_50": f if n % 4 == 0 else None,
            "f_100": f if n % 8 == 0 else None,
            "lambda_nm": round(frecuencia_a_lambda_nm(f), 4)
        }

        tabla.append(fila)

    return tabla


# ============================================================
# RUTA WEB PRINCIPAL
# ============================================================
@app.route("/")
def index():
    tabla_dwdm = generar_tabla_itu()
    return render_template("index.html", tabla=tabla_dwdm)


# ============================================================
# EJECUCIÓN
# ============================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)

