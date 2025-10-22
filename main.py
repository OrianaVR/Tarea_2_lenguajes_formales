import sys

# --- Configuración y Utilidades ---

NUEVOS_NO_TERMINALES = list("ZYXWVUTRQPO NMLKJIHGFEDCB") 
indice_nuevo_nt = 0

def obtener_nuevo_nt():
    """Obtiene una nueva letra para un no terminal."""
    global indice_nuevo_nt
    try:
        nuevo_nt = NUEVOS_NO_TERMINALES[indice_nuevo_nt]
        indice_nuevo_nt += 1
        return nuevo_nt
    except IndexError:
        raise Exception("Se agotaron las letras mayúsculas disponibles para nuevos no terminales.")

def leer_linea_no_vacia():
    """Lee líneas de stdin, saltándose líneas vacías/solo espacios."""
    while True:
        linea = sys.stdin.readline()
        if not linea: return None
        linea = linea.strip()
        if linea: return linea

def parsear_produccion(linea):
    """Analiza una línea de producción."""
    try:
        nt, alternativas_str = linea.split("->", 1)
        nt = nt.strip()
        alternativas = alternativas_str.split()
        return nt, [alt.strip() for alt in alternativas]
    except ValueError:
        return None, []

def formatear_gramatica(producciones, orden_original_nts):
    """
    Formatea la gramática resultante, respetando el orden de los NTs originales.
    """
    
    # 1. Separar NTs originales de los nuevos
    originales = [nt for nt in orden_original_nts if nt in producciones]
    
    # CORRECCIÓN DEFINITIVA: Se usa 'orden_original_nts' en lugar del nombre incorrecto.
    nuevos = sorted([nt for nt in producciones.keys() if nt not in orden_original_nts])
    
    # 2. Orden de salida: Originales (en orden de aparición) + Nuevos (ordenados)
    orden_salida = originales + nuevos
    
    salida = []
    for nt in orden_salida:
        if nt in producciones: 
            prods = producciones[nt]
            if prods:
                alternativas_ordenadas = sorted(prods) 
                salida.append(f"{nt}-> {' '.join(alternativas_ordenadas)}")
    return "\n".join(salida)

# --- Algoritmos Centrales ---

def eliminar_recursividad_directa(A, producciones):
    """Aplica la regla A -> beta A', A' -> alpha A' | epsilon ('e')."""
    
    alphas = [p[len(A):].strip() for p in producciones if p.startswith(A)]
    betas = [p for p in producciones if not p.startswith(A)]

    if not alphas:
        return producciones, None

    A_prima = obtener_nuevo_nt()
    
    # A -> beta A' (Concatenación estricta)
    nuevas_A = [f"{beta}{A_prima}" for beta in betas]
    
    # A' -> alpha A' | epsilon ('e') (Concatenación estricta)
    nuevas_A_prima = [f"{alpha}{A_prima}" for alpha in alphas] + ["e"]
    
    return nuevas_A, (A_prima, nuevas_A_prima)

def eliminar_recursividad_izquierda(gramatica_P, no_terminales):
    """Algoritmo general para eliminar recursividad izquierda indirecta y directa."""
    
    P = gramatica_P.copy()
    N = no_terminales

    for i in range(len(N)):
        Ai = N[i]
        
        # 1. Sustitución (j < i)
        for j in range(i):
            Aj = N[j]
            nuevas_prods_Ai = []
            
            for prod_Ai in P.get(Ai, []):
                if prod_Ai.startswith(Aj):
                    gamma = prod_Ai[len(Aj):].strip()
                    
                    for prod_Aj in P.get(Aj, []):
                        # Concatenación estricta: delta + gamma
                        nueva_prod = f"{prod_Aj}{gamma}"
                        nuevas_prods_Ai.append(nueva_prod)
                else:
                    nuevas_prods_Ai.append(prod_Ai)
            
            P[Ai] = nuevas_prods_Ai

        # 2. Eliminar recursión directa de Ai
        nuevas_Ai, nueva_nt_tuple = eliminar_recursividad_directa(Ai, P.get(Ai, []))
        P[Ai] = nuevas_Ai
        
        # 3. Añadir el nuevo no terminal a la gramática
        if nueva_nt_tuple:
            A_prima, prods_A_prima = nueva_nt_tuple
            P[A_prima] = prods_A_prima

    return P

# --- Funciones Principales I/O ---

def procesar_caso():
    k_linea = leer_linea_no_vacia()
    if k_linea is None: return

    try: k = int(k_linea)
    except ValueError: return

    P = {}
    lista_no_terminales = [] 
    
    for _ in range(k):
        linea = leer_linea_no_vacia()
        if linea is None: break
            
        nt, alternativas = parsear_produccion(linea)
        if nt and alternativas:
            P[nt] = alternativas
            if nt not in lista_no_terminales:
                lista_no_terminales.append(nt)

    resultado_P = eliminar_recursividad_izquierda(P, lista_no_terminales.copy())
    
    # Se mantiene este salto de línea para tu separación visual durante las pruebas.
    print() 
    
    print(formatear_gramatica(resultado_P, lista_no_terminales))

def main():
    n_casos_linea = leer_linea_no_vacia()
    if n_casos_linea is None: return

    try: n_casos = int(n_casos_linea)
    except ValueError: return

    for i in range(n_casos):
        global indice_nuevo_nt
        indice_nuevo_nt = 0
        
        procesar_caso()
        
        if i < n_casos - 1:
            print()

if __name__ == "__main__":
    main()