backend
-------
* adjust solubility ML model `backend/SolProp_ML-main`
* adjust genetic algorithm model `backend/genetic_algorithm`
* connect prices/CAS database
* adjust reactivity ML model `backend/RegioML-main`
* adjust synthetic accessibility `backend/genetic_algorithm/sascorer.py`. (https://jcheminf.biomedcentral.com/articles/10.1186/1758-2946-1-8) This is a simple score for SA but if we have CAS number, we assume it is synthesizable, otherwise we need to do retrosynthesis to show different options how can be synthesized and give prices/CAS for the reactants (maybe we add this as a button in the table to perform retrosynthesis)
* CO2 (LCA) to be done in the future (probably commercial database with different scenarios)

frontend
--------
* adjust colors for properties for different thresholds
* move the input settings and add temperature for each of the 3 categories


general
--------
focus first on API unit cleaning agent