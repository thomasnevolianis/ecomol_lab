from rdkit import Chem
from rdkit.Chem import Draw
import base64
from io import BytesIO

# Function to convert SMILES to image
def smiles_to_image(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is not None:
        img = Draw.MolToImage(mol)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return "data:image/png;base64," + img_str
    return None


def get_color_for_property(value, is_good_lower=True):
    threshold = 0.5  # Example threshold, can be adjusted
    if is_good_lower:
        return "green" if value < threshold else "red"
    else:
        return "green" if value > threshold else "red"
    