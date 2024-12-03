"""
Classifies: CHEBI:22707 benzenetriol
"""
from rdkit import Chem

def is_benzenetriol(smiles: str):
    """
    Determines if a molecule is a benzenetriol (a benzene ring with three hydroxy groups).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a benzenetriol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Generate the aromatic ring information
    rings = mol.GetRingInfo()

    # Check for at least one 6-membered ring
    if not any(len(ring) == 6 for ring in rings.AtomRings()):
        return False, "No 6-membered rings found"

    # Find all aromatic 6-membered rings
    aromatic_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings.append(ring)

    if not aromatic_rings:
        return False, "No aromatic 6-membered rings found"

    # Check if all carbons in the aromatic ring are carbon
    for ring in aromatic_rings:
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        if not all(atom.GetSymbol() == 'C' for atom in atoms):
            return False, "Ring contains non-carbon atoms"

    # Check for exactly three hydroxy groups (-OH) attached to the benzene ring
    ring_atoms = set(aromatic_rings[0])
    hydroxy_count = 0

    for atom_idx in ring_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 1:
                hydroxy_count += 1

    if hydroxy_count == 3:
        return True, "Molecule is a benzenetriol"
    else:
        return False, f"Molecule has {hydroxy_count} hydroxy groups, not 3"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22707',
                          'name': 'benzenetriol',
                          'definition': 'A triol in which three hydroxy groups '
                                        'are substituted onto a benzene ring.',
                          'parents': ['CHEBI:27136', 'CHEBI:33853']},
    'config': {   'llm_model_name': 'lbl/gpt-4o',
                  'accuracy_threshold': 0.95,
                  'max_attempts': 5,
                  'max_negative': 20,
                  'test_proportion': 0.1},
    'attempt': 0,
    'success': True,
    'best': True,
    'error': '',
    'stdout': '',
    'num_true_positives': 7,
    'num_false_positives': 0,
    'num_true_negatives': 14,
    'num_false_negatives': 7,
    'precision': 1.0,
    'recall': 0.5,
    'f1': 0.6666666666666666,
    'accuracy': None}