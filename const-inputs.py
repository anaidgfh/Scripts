""" 10 de Febrero de 2025  """
""" Dra. Anaid Flores, anaidgfh@gmail.com  """
""" ORCID: https://orcid.org/0000-0001-7243-3962 """
""" GITHUB: https://github.com/anaidgfh """
""" Programa que construye los inputs para realizar cálculos SAPT-DFT en Psi4"""
""" Necesitas una lista con los nombres de los monómeros (lista_monomeros.dat), las coordenadas de los monómeros deben estar en formato xyz"""
""" Por ejemplo:"""
""" Ammonia"""
""" Water"""
""" Necesitas una lista con los nombres de los dímeros (lista_dimeros.dat)"""
""" Por ejemplo:"""
""" Ammonia Water"""
""" Necesitas una tabla con los valores del grac_shift para cada monómero según la metodología que hayas utilizado (grac_shift.dat)"""
""" Dentro del codigo puedes cambiar la configuración de tu input para el SAPT-DFT"""
""" El codigo lee los archivos de entrada y genera una carpeta con todos los inputs solicitados según la metodología que escojas"""
""" """

import itertools
import os

def read_xyz(filename):
    """Reads an XYZ file and returns a list of atomic coordinates."""
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines[2:]  # Skip first two lines (number of atoms and comment)

def read_monomers(filename):
    """Reads a file with a list of monomers."""
    with open(filename, 'r') as f:
        monomers = f.read().splitlines()
    return monomers

def read_dimers(filename):
    """Reads a file with pairs of dimers."""
    with open(filename, 'r') as f:
        dimers = [tuple(line.split()) for line in f.read().splitlines()]
    return dimers

def read_shifts(filename):
    """Reads the shifts from a file."""
    shifts = {}
    with open(filename, 'r') as f:
        for line in f.read().splitlines():
            parts = line.split()
            monomer = parts[0]
            # Los desplazamientos para los diferentes funcionales y bases
            shifts[monomer] = {
                "B3LYP_aug-cc-pVDZ": float(parts[1]),
                "B3LYP_aug-cc-pVTZ": float(parts[2]),
                "PBE0_aug-cc-pVDZ": float(parts[3]),
                "PBE0_aug-cc-pVTZ": float(parts[4]),
                "wB97X_aug-cc-pVDZ": float(parts[5]),
                "wB97X_aug-cc-pVTZ": float(parts[6])
            }
    return shifts

def generate_psi4_input(monomer1, monomer2, coords1, coords2, shift_a, shift_b, functional, basis, output_dir):
    """Generates a Psi4 input file for a given dimer configuration."""
    input_filename = f"{output_dir}/{monomer1}_{monomer2}_{functional}_{basis}.inp"
    with open(input_filename, 'w') as f:
        f.write("memory 9000 mb\n\n")
        f.write("molecule {\n")
        f.write("0 1\n")
        f.writelines(coords1)
        f.write(" --\n")
        f.write("0 1\n")
        f.writelines(coords2)
        f.write("}\n\n")
        f.write(f"set basis {basis}\n\n")
        f.write("set {\n")
        f.write(f" sapt_dft_grac_shift_a  {shift_a}\n")
        f.write(f" sapt_dft_grac_shift_b  {shift_b}\n")
        f.write(f" sapt_dft_functional {functional}\n")
        f.write("}\n\n")
        f.write("energy('sapt(dft)')\n")

def main():
    # Leer archivos de entrada
    monomers = read_monomers("lista-monomeros.dat")
    dimers = read_dimers("lista-dimeros.dat")
    shifts_data = read_shifts("grac-shift.dat")

    functionals = ["B3LYP", "PBE0", "wB97X"]
    bases = ["aug-cc-pVDZ", "aug-cc-pVTZ"]

    output_dir = "psi4_inputs"
    os.makedirs(output_dir, exist_ok=True)

    # Iterar sobre los dimers
    for (mon1, mon2) in dimers:
        coords1 = read_xyz(f"{mon1}.xyz")  # Leer las coordenadas del primer monómero
        coords2 = read_xyz(f"{mon2}.xyz")  # Leer las coordenadas del segundo monómero

        # Iterar sobre las combinaciones de functionals y bases
        for functional, basis in itertools.product(functionals, bases):
            # Crear la clave para acceder a los desplazamientos
            key = f"{functional}_{basis}"
            shift_a = shifts_data[mon1][key]  # Obtener desplazamiento del monómero 1
            shift_b = shifts_data[mon2][key]  # Obtener desplazamiento del monómero 2
            generate_psi4_input(mon1, mon2, coords1, coords2, shift_a, shift_b, functional, basis, output_dir)

if __name__ == "__main__":
    main()
