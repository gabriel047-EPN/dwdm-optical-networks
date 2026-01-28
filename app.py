# ============================================================
# ITU-T G.694.1 – DWDM
# TABLAS AGRUPADAS POR ESPACIAMIENTO DE CANAL
# ============================================================
#
# DESCRIPCIÓN GENERAL:
# --------------------
# Este programa implementa la rejilla DWDM definida en la
# recomendación ITU-T G.694.1, utilizando una granularidad
# mínima de 12.5 GHz anclada a la frecuencia de referencia
# de 193.1 THz.
#
# A partir del grid base de 12.5 GHz, se generan subconjuntos
# de canales que cumplen con espaciamientos mayores:
#
#  - 25  GHz  → canales con índice n par
#  - 50  GHz  → canales con índice n múltiplo de 4
#  - 100 GHz  → canales con índice n múltiplo de 8
#
# NOTA IMPORTANTE:
# ----------------
# Las longitudes de onda calculadas son APROXIMADAS.
# De acuerdo con la ITU-T, las especificaciones DWDM
# se definen con respecto a la frecuencia nominal central
# y no a la longitud de onda.
#
# ============================================================

# -----------------------------
# CONSTANTES FÍSICAS Y NORMATIVAS
# -----------------------------
C = 2.99792458e8      # Velocidad de la luz en el vacío (m/s)
F_REF = 193.1         # Frecuencia de referencia ITU (THz)
DELTA_F = 0.0125      # Granularidad mínima (THz = 12.5 GHz)

# Rango ilustrativo de frecuencias (Bandas C + L)
# NOTA: Los extremos son ilustrativos, no normativos
F_MIN = 184.5000
F_MAX = 195.9375


# -----------------------------
# FUNCIONES AUXILIARES
# -----------------------------
def frecuencia_a_lambda_nm(f_thz):
    """
    Convierte una frecuencia en THz a longitud de onda en nm.
    
    NOTA:
    -----
    Esta conversión se realiza usando la velocidad de la luz
    en el vacío. El resultado es una aproximación, tal como
    se presenta en las tablas de la ITU-T G.694.1.
    """
    return (C / (f_thz * 1e12)) * 1e9


def generar_tablas_por_espaciamiento():
    """
    Genera tablas DWDM independientes para cada espaciamiento
    de canal definido en la ITU-T G.694.1.

    TABLAS GENERADAS:
    -----------------
    - 12.5 GHz : Grid base (todos los canales)
    - 25  GHz  : Subconjunto del grid base
    - 50  GHz  : Subconjunto del grid base
    - 100 GHz  : Subconjunto del grid base

    NOTA:
    -----
    Todos los espaciamientos mayores se obtienen a partir
    del grid base de 12.5 GHz, seleccionando únicamente
    los canales que cumplen con la condición de índice n.
    """

    tablas = {
        "12.5 GHz": [],
        "25 GHz": [],
        "50 GHz": [],
        "100 GHz": []
    }

    # Cálculo del rango del índice n
    n_min = int(round((F_MIN - F_REF) / DELTA_F))
    n_max = int(round((F_MAX - F_REF) / DELTA_F))

    for n in range(n_min, n_max + 1):

        # Frecuencia nominal central (THz)
        f = round(F_REF + n * DELTA_F, 4)

        # Longitud de onda aproximada (nm)
        lambda_nm = round(frecuencia_a_lambda_nm(f), 4)

        # Grid base: siempre válido
        tablas["12.5 GHz"].append((n, f, lambda_nm))

        # Subgrids según ITU-T G.694.1
        if n % 2 == 0:
            tablas["25 GHz"].append((n, f, lambda_nm))

        if n % 4 == 0:
            tablas["50 GHz"].append((n, f, lambda_nm))

        if n % 8 == 0:
            tablas["100 GHz"].append((n, f, lambda_nm))

    return tablas


def imprimir_tabla(nombre, filas):
    """
    Imprime una tabla DWDM correspondiente a un
    espaciamiento de canal específico.
    """

    print("\n" + "=" * 65)
    print(f"TABLA DWDM – ESPACIAMIENTO {nombre}")
    print("=" * 65)
    print(f"{'n':>5} | {'Frecuencia nominal (THz)':>22} | {'Lambda aprox. (nm)':>20}")
    print("-" * 65)

    for n, f, lam in filas:
        print(f"{n:5d} | {f:22.4f} | {lam:20.4f}")


# -----------------------------
# EJECUCIÓN PRINCIPAL
# -----------------------------
if __name__ == "__main__":

    tablas = generar_tablas_por_espaciamiento()

    for nombre, filas in tablas.items():
        imprimir_tabla(nombre, filas)
