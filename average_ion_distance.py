import random
import numpy as np
from pymatgen.core.structure import Structure

def random_double_lanthanide_substitution(structure, lanthanide_element_1, concentration_1, lanthanide_element_2, concentration_2):
    modified_structure = structure.copy()
    num_sites = len(modified_structure.sites)
    print({num_sites})
    # Calculate the number of substitutions for each lanthanide element
    num_substitutions_1 = int(num_sites * concentration_1)
    num_substitutions_2 = int(num_sites * concentration_2)
    
    # Create separate lists of Y site indices for each lanthanide element
    y_indices_1 = [i for i, site in enumerate(modified_structure.sites) if site.specie.name == "Y"]
    y_indices_2 = [i for i, site in enumerate(modified_structure.sites) if site.specie.name == "Y"]
    
    # Perform random substitution for the first lanthanide element
    for _ in range(num_substitutions_1):
        index_to_replace = random.choice(y_indices_1)
        modified_structure.replace(index_to_replace, lanthanide_element_1)
        y_indices_1.remove(index_to_replace)
    
    # Perform random substitution for the second lanthanide element
    for _ in range(num_substitutions_2):
        index_to_replace = random.choice(y_indices_2)
        modified_structure.replace(index_to_replace, lanthanide_element_2)
        y_indices_2.remove(index_to_replace)
    
    return modified_structure

def calculate_mean_distance(structure, element_1, element_2):
    element_1_positions = []
    element_2_positions = []

    for site in structure.sites:
        if site.specie.name == element_1:
            element_1_positions.append(site.coords)
        elif site.specie.name == element_2:
            element_2_positions.append(site.coords)

    if not element_1_positions or not element_2_positions:
        return None  # One or both elements not found in the structure

    distances = []
    for pos_1 in element_1_positions:
        for pos_2 in element_2_positions:
            distance = np.linalg.norm(np.array(pos_1) - np.array(pos_2))
            distances.append(distance)

    mean_distance = np.mean(distances)
    return mean_distance

def main():
    # Load the CIF file from your local file system
    cif_file_path = ".cif"  # Add file path
    structure = Structure.from_file(cif_file_path)

    # Duplicate the unit cell
    repetitions = [30, 30, 30]  # Adjust the repetition as needed
    structure.make_supercell(repetitions)

    # Define the Lanthanide elements and concentrations for substitution
    lanthanide_element_1 = "Tm"  # Change to your first desired lanthanide
    concentration_1 = 0.01  # Concentration for the first lanthanide
    
    lanthanide_element_2 = "Nd"  # Change to your second desired lanthanide
    concentration_2 = 0.001  # Concentration for the second lanthanide
    
    # Perform random double lanthanide substitution with different concentrations
    modified_structure = random_double_lanthanide_substitution(structure, lanthanide_element_1, concentration_1, lanthanide_element_2, concentration_2)

    # Calculate the mean distance between the substituted lanthanides
    mean_dist = calculate_mean_distance(modified_structure, lanthanide_element_1, lanthanide_element_2)

    

    if mean_dist is not None:
        print(f"Mean distance between {lanthanide_element_1} and {lanthanide_element_2}: {mean_dist:.2f} Ångstroms")
    else:
        print("One or both lanthanides not found in the structure.")

if __name__ == "__main__":
    main()
