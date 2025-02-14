""" 10 de Febrero de 2025  """
""" Dra. Anaid Flores, anaidgfh@gmail.com  """
""" ORCID: https://orcid.org/0000-0001-7243-3962 """
""" GITHUB: https://github.com/anaidgfh """
""" Programa que obtiene el valor del RMSD, el MAD y el max(MAD) de un conjunto de datos acomodados por columnas."""
""" """


import numpy as np
import pandas as pd

def load_data(file_path):
    """Carga los datos del archivo y los convierte en un DataFrame."""
    df = pd.read_csv(file_path, delimiter="\t", decimal=",", header=None)
    
    # Renombrar las columnas
    columns = ["Archivo", "BD", "BT", "PD", "PT", "wD", "wT", "CCSD(T)"]
    df.columns = columns

    # Convertir valores a tipo numérico
    for col in columns[1:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

def compute_metrics(df):
    """Calcula RMSD, MAD y max(MAD) comparando los métodos con CCSD(T)."""
    methods = ["BD", "BT", "PD", "PT", "wD", "wT"]
    cc_ref = df["CCSD(T)"]

    results = {}

    for method in methods:
        diff = df[method] - cc_ref  # Diferencia con CCSD(T)
        
        rmsd = np.sqrt(np.mean(diff**2))  # RMSD
        mad = np.mean(np.abs(diff))  # MAD
        max_mad = np.max(np.abs(diff))  # Máximo MAD
        
        results[method] = {"RMSD": rmsd, "MAD": mad, "Max MAD": max_mad}

    return results

def save_results(results, output_file):
    """Guarda los resultados en un archivo de texto."""
    with open(output_file, "w") as f:
        f.write("Comparación de métodos con CCSD(T):\n")
        for method, metrics in results.items():
            f.write(f"\nMétodo: {method}\n")
            f.write(f"  RMSD: {metrics['RMSD']:.4f} kcal/mol\n")
            f.write(f"  MAD: {metrics['MAD']:.4f} kcal/mol\n")
            f.write(f"  Max MAD: {metrics['Max MAD']:.4f} kcal/mol\n")

def main(file_path, output_file):
    df = load_data(file_path)
    results = compute_metrics(df)
    save_results(results, output_file)

# Ejemplo de uso
file_path = "datos_energias.dat"  # Reemplaza con el nombre de tu archivo
output_file = "resultados.txt"  # Nombre del archivo de salida
main(file_path, output_file)

print(f"Los resultados han sido guardados en '{output_file}'.")

