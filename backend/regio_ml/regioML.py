import numpy as np
import argparse

from rdkit import Chem
import lightgbm as lgb

# from DescriptorCreator.find_atoms import find_identical_atoms
from DescriptorCreator.PrepAndCalcDescriptor import EASMolPreparation
import DescriptorCreator.molecule_svg as molsvg


def parse_args():
    """
    Argument parser so this can be run from the command line
    """
    parser = argparse.ArgumentParser(description='Run regioselectivity predictions from the command line')
    parser.add_argument('-s', '--smiles', default='c1(ccno1)C',
                        help='SMILES input for regioselectivity predictions')
    parser.add_argument('-n', '--name', default='test_mol', help='The name of the molecule')
    parser.add_argument('-m', '--model', default='models/LGBM_measured_allData_final_model.txt',
                        help='Path to the model')
    parser.add_argument('-o', '--observed', default=None, help='Measured/observed reactive sites')
    return parser.parse_args()


# For command line use
if __name__ == "__main__":
    args = parse_args()

    predictor = EASMolPreparation()
    des =('GraphChargeShell', {'charge_type': 'cm5', 'n_shells': 5, 'use_cip_sort': True})
    final_model = lgb.Booster(model_file=args.model)
    
    smiles = Chem.MolToSmiles(Chem.MolFromSmiles(args.smiles), isomericSmiles=True) # canonicalize input smiles
    cm5_list = predictor.calc_CM5_charges(smiles, name=args.name, optimize=False, save_output=True)
    atom_indices, descriptor_vector = predictor.create_descriptor_vector(des[0], **des[1])

    pred_proba = final_model.predict(descriptor_vector, num_iteration=final_model.best_iteration)
    pred = np.rint(pred_proba)

    print('SMILES:', smiles)
    print('Atom indices:', atom_indices)
    print('Pred. probabilities:', pred_proba)
    print('Predictions:', pred)

    # atom_reactive = [bool(x) for x in pred]
    # reactive_sites = np.array(atom_indices)[atom_reactive].tolist()
    # reactive_sites = find_identical_atoms(predictor.rdkit_mol, reactive_sites)
    # labels = [int(1) if site in reactive_sites else int(0) for site in range(len(cm5_list))]
    # print('labels:', labels)


    # Apply regression model
    final_model_reg = lgb.Booster(model_file='models/LGBM_regressor_GFN1_allData_final_model.txt')
    PA_preds = final_model_reg.predict(descriptor_vector, num_iteration=final_model_reg.best_iteration)
    max_PA = np.max(PA_preds)
    if max_PA >= 100-2: #kcal/mol
        reactivity_label = 'High reactivity'
    elif max_PA <= 70+2: #kcal/mol
        reactivity_label = 'Low reactivity'
    else:
        reactivity_label = 'Medium reactivity'

    print('Proton affinities:', list(map(int, PA_preds)))
    
    # Draw molecule
    result_svg = molsvg.generate_structure(smiles, [smiles], [reactivity_label], [pred_proba.tolist()], [atom_indices], args.observed)
    print(reactivity_label)
    f_draw = open(f'{args.name}.svg','w')
    f_draw.write(result_svg)
    f_draw.close()
    print(f'Molecule drawing with predictions saved as: {args.name}.svg')
