## 10 de Febrero de 2025
## Dra. Anaid Flores, anaidgfh@gmail.com  ####
## ORCID: https://orcid.org/0000-0001-7243-3962  #### 
## GITHUB: https://github.com/anaidgfh  ####
## Script en bash que extrae los valores del homo y el lumo de los outputs de un cálculo DFT en ORCA ###
######################################################################################################


#!/bin/bash

# Lista de carpetas a recorrer (modifica según tu estructura)
carpetas=(/scratch/luis/test/basesADN-HBs/DFT/*/)

# Nombre del archivo CSV de salida
output_file="homo_lumo_results.csv"

# Crear el encabezado del archivo CSV
echo -n "Archivo" > "$output_file"
for carpeta in "${carpetas[@]}"; do
    echo -n ",${carpeta}_HOMO (eV),${carpeta}_LUMO (eV)" >> "$output_file"
done
echo "" >> "$output_file"

# Diccionario para almacenar resultados
declare -A homo_values
declare -A lumo_values

# Obtener una lista única de nombres de archivos (sin extensión)
declare -A unique_files
for carpeta in "${carpetas[@]}"; do
    for file in "$carpeta"/*.out; do
        if [[ -f "$file" ]]; then
            base_name=$(basename "$file" .out)
            unique_files["$base_name"]=1
        fi
    done
done

# Procesar cada archivo en cada carpeta
for carpeta in "${carpetas[@]}"; do
    for file in "$carpeta"/*.out; do
        if [[ -f "$file" ]]; then
            base_name=$(basename "$file" .out)
            homo_energy=""
            lumo_energy=""

            while read -r line; do
                occ=$(echo "$line" | awk '{print $2}')
                energy_ev=$(echo "$line" | awk '{print $4}')

                if [[ "$occ" == "2.0000" ]]; then
                    homo_energy=$energy_ev  # Última ocupada será el HOMO
                elif [[ "$occ" == "0.0000" && -z "$lumo_energy" ]]; then
                    lumo_energy=$energy_ev  # Primer desocupado será el LUMO
                    break
                fi
            done < <(grep -A 100 "ORBITAL ENERGIES" "$file" | tail -n +3)

            homo_values["$base_name,$carpeta"]=$homo_energy
            lumo_values["$base_name,$carpeta"]=$lumo_energy
        fi
    done
done

# Escribir los resultados en el CSV
for base_name in "${!unique_files[@]}"; do
    echo -n "$base_name" >> "$output_file"
    for carpeta in "${carpetas[@]}"; do
        homo="${homo_values["$base_name,$carpeta"]}"
        lumo="${lumo_values["$base_name,$carpeta"]}"
        echo -n ",${homo:-N/A},${lumo:-N/A}" >> "$output_file"
    done
    echo "" >> "$output_file"
done

echo "Proceso terminado. Resultados guardados en $output_file"
