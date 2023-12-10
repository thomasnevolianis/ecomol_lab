import random

def process_results():
    """
    Simulates running a machine learning model.
    Returns molecules with their properties.
    """
    # Simulated properties for each molecule
    reactivity_options = ["Low", "Medium", "High"]

    # Simulating molecules with random properties
    molecules = []
    for smiles in ["C1=CC=CC=C1", "C1CC1", "C1=CN=CN1", "C1CCOC1", "C1COCO1", "C1CC2CC1C2", "C1=CC=CC=C1", "C1CC1", "C1=CN=CN1", "C1CCOC1", "C1COCO1", "C1CC2CC1C2"]:
        molecule = {
            "smiles": smiles,
            "solubility": random.random(),  # Random property value
            "score": random.randint(0, 100),  # Score from 0 to 100
            "reactivity": random.choice(reactivity_options),  # Random reactivity
            "synthetic_accessibility": "CAS" + str(random.randint(10000, 99999)),  # Simulated CAS number
            "price_euro": round(random.uniform(10, 100), 2),  # Price in euro
            "co2_kg": round(random.uniform(0.1, 10.0), 2)  # CO2 per kg
        }
        molecules.append(molecule)

    return molecules
