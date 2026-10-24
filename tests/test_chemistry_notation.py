"""Pure finite formula/equation parsing, independent of unreviewed chemistry."""
import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_notation import formula, equation


@pytest.mark.parametrize('value,expected',[
    ('H₂O',('H2O',{'H':2,'O':1})),('Ca(OH)2',('Ca(OH)2',{'Ca':1,'O':2,'H':2})),
    ('Ca3(PO4)2',('Ca3(PO4)2',{'Ca':3,'P':2,'O':8})),('Na1Cl1',('NaCl',{'Na':1,'Cl':1})),
    ('H g',('Hg',{'Hg':1})),('C',('C',{'C':1}))])
def test_only_syntactic_formula_counts_are_computed(value,expected):
    assert formula(value)==expected


@pytest.mark.parametrize('value',[
    'h2O','H²O','H0O','H02O','2H2O','Ca(OH2','Ca)OH(', '()', '(H999)999',
    '((((H)2)2)2)2','H2O;print(1)','__import__("os")','[Na+]','H₂O⁺',
    'H1000', 'x'*81, '<script>',True,{}])
def test_formula_parser_rejects_case_syntax_charge_execution_and_bounds(value):
    with pytest.raises(ValueError):formula(value)


@pytest.mark.parametrize('value',[
    '2H2+O2=2H2O','O₂ + 2H₂ → 2H₂O','4H2+2O2->4H2O',
    'H2+H2+O2=2H2O'])
def test_balanced_equivalent_equation_terms_order_and_integer_scale(value):
    sides,atoms,key=equation(value)
    assert atoms[0]==atoms[1]=={'H':4,'O':2} or value.startswith('4')
    assert key==equation('2H2+O2=2H2O')[2]
    assert grade_answer({'kind':'chemical_equation','expected':'2H2+O2=2H2O'},{'value':value})=='correct'


@pytest.mark.parametrize('value,code',[
    ('H2+O2=H2O','atom_imbalance'),('2H2+O2=2H2O2','incorrect_species'),
    ('2H2O=2H2+O2','incorrect_species'),('h2+O2=H2O','invalid_answer'),
    ('H2+O2==H2O','invalid_answer'),('0H2+O2=H2O','invalid_answer'),
    ('0.5H2+O2=H2O','invalid_answer'),('H2+O2=H2O+','invalid_answer'),
    ('1000H2+O2=H2O','invalid_answer'),('H2+O2→H2O;alert(1)','invalid_answer'),
    ('','answer_required')])
def test_equation_feedback_distinguishes_wrong_species_and_atom_imbalance(value,code):
    assert grade_answer({'kind':'chemical_equation','expected':'2H2+O2=2H2O'},{'value':value})==code


def test_formulas_never_accept_an_unreviewed_isomer_by_atom_counts_alone():
    spec={'kind':'chemical_formula','expected':'CH3CH2OH','aliases':[]}
    assert grade_answer(spec,{'value':'CH₃CH₂OH'})=='correct'
    assert grade_answer(spec,{'value':'CH3OCH3'})=='incorrect'
    assert grade_answer({'kind':'chemical_formula','expected':'HgO'}, {'value':'HGO'})=='incorrect'
