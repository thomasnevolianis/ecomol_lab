import os
import numpy as np
from rdkit import Chem
import lightgbm as lgb
from backend.regio_ml.DescriptorCreator.PrepAndCalcDescriptor import EASMolPreparation
import backend.regio_ml.DescriptorCreator.molecule_svg as molsvg

def get_reactivity_label(smiles, name='test_mol'):
    model_path = 'backend/regio_ml/models/LGBM_measured_allData_final_model.txt'
    reg_model_path = 'backend/regio_ml/models/LGBM_regressor_GFN1_allData_final_model.txt'

    if not os.path.exists(model_path) or not os.path.exists(reg_model_path):
        print(os.getcwd())
        print(model_path)
        print(reg_model_path)
        raise FileNotFoundError("Model file not found. Please check the path.")

    predictor = EASMolPreparation()
    des = ('GraphChargeShell', {'charge_type': 'cm5', 'n_shells': 5, 'use_cip_sort': True})
    final_model = lgb.Booster(model_file=model_path)
    
    canonical_smiles = Chem.MolToSmiles(Chem.MolFromSmiles(smiles), isomericSmiles=True)
    cm5_list = predictor.calc_CM5_charges(canonical_smiles, name=name, optimize=False, save_output=False)
    atom_indices, descriptor_vector = predictor.create_descriptor_vector(des[0], **des[1])

    pred_proba = final_model.predict(descriptor_vector, num_iteration=final_model.best_iteration)

    final_model_reg = lgb.Booster(model_file=reg_model_path)
    PA_preds = final_model_reg.predict(descriptor_vector, num_iteration=final_model_reg.best_iteration)
    max_PA = np.max(PA_preds)

    if max_PA >= 100-2: # kcal/mol
        reactivity_label = 'High'
    elif max_PA <= 70+2: # kcal/mol
        reactivity_label = 'Low'
    else:
        reactivity_label = 'Medium'

    return reactivity_label
