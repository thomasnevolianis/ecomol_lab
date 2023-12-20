import random
from backend.genetic_algorithm.sa import calculateSAForSmiles
from backend.regio_ml.reactivity_ml import get_reactivity_label
from backend.cas.get_cas import get_cas
from backend.price.get_price import get_price
from backend.co2.get_co2 import get_co2

def process_results():
    """
    Simulates running a machine learning model.
    Returns molecules with their properties.
    """
    # Read SMILES from a .smi file TODO adjust this so it comes from a design
    with open("backend/genetic_algorithm/ZINC_first_1000.smi", "r") as file:
        smiles_list = file.read().splitlines()

    # Simulating molecules with properties
    molecules = []
    for smiles in smiles_list:
        molecule = {
            "smiles": smiles,
            "solubility": round(random.random(),1),  # Random property value
            "score": random.randint(0, 100),  # Initial random score
            "reactivity": 1, #get_reactivity_label(smiles),
            "synthetic_accessibility": calculateSAForSmiles(smiles),
            # TODO adjust to database and if it does not exist set it to "-"
            "cas": get_cas(smiles),
            # TODO adjust to database and if it does not exist set it to "-"
            "price_euro": get_price(smiles),  # Price in euro
            # TODO adjust to database and if it does not exist set it to "-"
            "co2_kg": get_co2(smiles)
        }
        molecules.append(molecule)

    # Normalize solubility scores and adjust scores with a weighted system
    max_solubility = max(mol["solubility"] for mol in molecules)
    min_solubility = min(mol["solubility"] for mol in molecules)
    for mol in molecules:
        normalized_solubility = (mol["solubility"] - min_solubility) / (max_solubility - min_solubility)
        weighted_score = 0.5 * mol["score"] + 0.5 * (normalized_solubility * 100)
        mol["score"] = round(weighted_score, 2)

    return molecules
