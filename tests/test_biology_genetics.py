"""Independent probability checks for the reviewed textbook genetics exercises."""
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from itertools import product
from types import SimpleNamespace

import pytest

from services.curriculum_validation import load_documents, load_lesson_set, validate_lesson
from services.study import grade


def question(slug, number, grade=9):
    lesson = next(l for l in load_lesson_set() if l['key'] == f'biology-{grade}-{slug}-v1')
    return next(q for q in lesson['questions'] if q['key'] == f'{slug}-q{number}')


def offspring(parent1, parent2):
    """Enumerate equally likely gametes at independent diploid loci."""
    gametes1 = list(product(*parent1))
    gametes2 = list(product(*parent2))
    return Counter(
        tuple(''.join(sorted((a, b))) for a, b in zip(left, right))
        for left, right in product(gametes1, gametes2)
    )


def probability(distribution, condition):
    return Fraction(sum(n for genotype, n in distribution.items() if condition(genotype)), sum(distribution.values()))


@pytest.mark.parametrize('slug,number,parents,condition,population', [
    ('paragraph-48', 5, (('Aa',), ('Aa',)), lambda g: g == ('aa',), None),
    ('paragraph-50', 5, (('Aa', 'Bb'), ('Aa', 'Bb')), lambda g: g == ('aa', 'bb'), None),
    ('practical-1', 3, (('Aa', 'Bb'), ('Aa', 'Bb')), lambda g: 'A' in g[0] and 'B' in g[1], 320),
    ('practical-1', 4, (('Aa', 'Bb'), ('Aa', 'Bb')), lambda g: g == ('aa', 'bb'), 320),
    ('practical-1', 5, (('Aa', 'Bb', 'Cc'), ('aa', 'bb', 'cc')), lambda g: g == ('Aa', 'Bb', 'Cc'), None),
    ('practical-2', 2, (('Aa', 'Bb'), ('aa', 'bb')), lambda g: 'A' in g[0] and 'B' in g[1], None),
    ('practical-2', 5, (('Aa', 'Bb'), ('Aa', 'Bb')), lambda g: sum(c.isupper() for locus in g for c in locus) == 3, None),
])
def test_authored_probabilities_match_exhaustive_gamete_enumeration(slug, number, parents, condition, population):
    result = probability(offspring(*parents), condition)
    expected = str(result) if population is None else f'{int(result * population)} ta'
    assert question(slug, number)['correct_answer'] == expected


@pytest.mark.parametrize('slug,number,parents,condition', [
    ('paragraph-53', 4, (('Aa', 'Bb'), ('Aa', 'Bb')), lambda g: 'A' in g[0] and 'B' in g[1]),
    ('paragraph-53', 8, (('Ii', 'Cc'), ('Ii', 'Cc')), lambda g: 'I' in g[0] or g[1] == 'cc'),
    ('practical-2', 3, (('Ii', 'Cc'), ('ii', 'cc')), lambda g: 'I' in g[0] or g[1] == 'cc'),
])
def test_authored_complementary_and_inhibitor_ratios(slug, number, parents, condition):
    result = probability(offspring(*parents), condition)
    ratio = Fraction(result, 1 - result)
    assert question(slug, number)['correct_answer'] == f'{ratio.numerator}:{ratio.denominator}'


def test_lethal_genotype_is_excluded_only_from_survivor_denominator():
    distribution = offspring(('Aa',), ('Aa',))
    survivors = Counter({g: n for g, n in distribution.items() if g != ('AA',)})
    p = probability(survivors, lambda g: g == ('Aa',))
    assert p == Fraction(2, 3)
    assert question('paragraph-54', 7)['correct_answer'] == str(p)
    ratio = Fraction(p, 1 - p)
    assert question('paragraph-54', 6)['correct_answer'] == f'{ratio.numerator}:{ratio.denominator}'


def test_x_linked_conditional_risk_is_not_total_offspring_risk():
    # Mother's two X gametes crossed with father's X or Y gametes.
    combinations = list(product(('XH', 'Xh'), ('XH', 'Y')))
    sons = [pair for pair in combinations if pair[1] == 'Y']
    affected_sons = [pair for pair in sons if pair[0] == 'Xh']
    assert question('paragraph-57', 6)['correct_answer'] == str(Fraction(len(affected_sons), len(sons)))
    assert question('practical-3', 4)['correct_answer'] == str(Fraction(len(affected_sons), len(combinations)))


@pytest.mark.parametrize('damage', [None, 'duplicate', 'missing_format', 'unsupported'])
def test_genotype_options_are_case_sensitive_only_when_explicit(damage):
    lesson = deepcopy(next(l for l in load_lesson_set() if l['key'] == 'biology-9-paragraph-48-v1'))
    q = lesson['questions'][1]
    assert q['answer_format'] == 'genotype'
    if damage == 'duplicate':
        q['options'] = ['Aa', 'Aa', 'AA', 'aa']
    elif damage == 'missing_format':
        del q['answer_format']
    elif damage == 'unsupported':
        q['answer_format'] = 'ignore_case'
    if damage:
        with pytest.raises(ValueError):
            validate_lesson(load_documents()[0], lesson)
    else:
        validate_lesson(load_documents()[0], lesson)


def test_server_does_not_grade_aa_as_heterozygous_Aa():
    q = question('paragraph-48', 2)
    snapshot = SimpleNamespace(questions=[{'id': 1, 'options': q['options'], 'correct_answer': q['correct_answer']}])
    wrong, _ = grade(snapshot, [{'question_id': 1, 'user_answer': 'aa', 'is_correct': True}])
    correct, _ = grade(snapshot, [{'question_id': 1, 'answer_index': q['options'].index('Aa'), 'is_correct': False}])
    assert wrong[0]['is_correct'] is False
    assert correct[0]['is_correct'] is True


@pytest.mark.parametrize('paragraph,number,parents,condition,population', [
    (17, 4, (('Aa',), ('Aa',)), lambda g: g == ('Aa',), 240),
    (17, 7, (('Aa',), ('Aa',)), lambda g: g == ('Aa',), 200),
    (18, 3, (('Aa', 'Bb'), ('Aa', 'Bb')), lambda g: 'A' in g[0] and g[1] == 'bb', 320),
    (18, 7, (('Aa', 'Bb', 'Cc'), ('Aa', 'Bb', 'Cc')), lambda g: g == ('aa', 'bb', 'cc'), 640),
    (22, 2, (('Aa', 'Bb'), ('Aa', 'Bb')), lambda g: not ('A' in g[0] and 'B' in g[1]), 160),
    (22, 5, (('Cc', 'Ii'), ('Cc', 'Ii')), lambda g: 'C' in g[0] and g[1] == 'ii', 320),
    (22, 6, (('Aa', 'Ii'), ('Aa', 'Ii')), lambda g: 'I' in g[1], 160),
    (22, 8, (('Aa', 'Bb'), ('Aa', 'Bb')), lambda g: g == ('aa', 'bb'), 160),
])
def test_grade10_authored_counts_use_independent_model_not_copied_ratio(paragraph, number, parents, condition, population):
    result = probability(offspring(*parents), condition) * population
    assert result.denominator == 1
    assert question(f'paragraph-{paragraph}', number, grade=10)['correct_answer'] == str(result.numerator)


def test_grade10_additive_model_and_genotypic_class_counts():
    two = offspring(('Aa', 'Bb'), ('Aa', 'Bb'))
    middle = probability(two, lambda g: sum(c.isupper() for locus in g for c in locus) == 2)
    assert middle == Fraction(6, 16)
    assert question('paragraph-22', 7, grade=10)['correct_answer'] == '6/16'
    three = offspring(('Aa', 'Bb', 'Cc'), ('Aa', 'Bb', 'Cc'))
    assert question('paragraph-18', 6, grade=10)['correct_answer'] == 'Genotipik sinflar'
    assert len(three) == 27 and sum(three.values()) == 64


def test_grade10_x_linked_examples_keep_sons_and_all_offspring_denominators():
    pairs = list(product(('XW', 'Xw'), ('XW', 'Y')))
    sons = [p for p in pairs if p[1] == 'Y']
    affected = [p for p in sons if p[0] == 'Xw']
    assert question('paragraph-21', 3, grade=10)['correct_answer'] == str(int(Fraction(len(affected), len(sons)) * 120))
    assert question('paragraph-21', 4, grade=10)['correct_answer'] == str(int(Fraction(len(affected), len(pairs)) * 240))


def test_grade10_digital_lab_units_complement_and_model_math():
    def lab(n):
        return question('laboratory-1', n, grade=10)['correct_answer']
    assert lab(1) == f'{2400 // 2} juft'
    assert lab(2) == f'{Fraction(1200) * Fraction(34, 100)} nm'
    assert lab(3) == str((2400 - 400 * 2) // 2)
    template = 'TACGGA'
    rna = template.translate(str.maketrans('ATGC', 'UACG'))
    assert lab(4) == f'{rna[:3]}-{rna[3:]}'
    assert lab(5) == str(270 // 3)
    assert lab(6) == f'{3 * 38 + 2 * 2} mol'
    assert question('paragraph-6', 8, grade=10)['correct_answer'] == f'{(100 - 2 * 22) // 2}%'


def test_grade10_recombination_sums_both_classes_and_divides_by_all_offspring():
    assert question('paragraph-19', 3, grade=10)['correct_answer'] == f'{2 * Fraction(85, 10)}%'
    result = (Fraction(48) + 56) / 800 * 100
    assert question('paragraph-19', 6, grade=10)['correct_answer'] == f'{result}%'


def test_grade10_human_model_probability_is_conditional_not_a_diagnosis():
    distribution = offspring(('Aa',), ('aa',))
    answer = probability(distribution, lambda g: g == ('aa',))
    assert question('paragraph-24', 8, grade=10)['correct_answer'] == str(answer)
    assert 'klinik tashxis' in question('paragraph-24', 8, grade=10)['explanation']


def test_grade10_structural_and_genome_mutation_examples_have_consistent_math():
    before = 'ABCDEF'
    after_inversion = before[:2] + before[2:5][::-1] + before[5:]
    q = question('paragraph-23', 5, grade=10)
    assert after_inversion == 'ABEDCF' and sorted(before) == sorted(after_inversion)
    assert before in q['question_text'] and after_inversion in q['question_text']
    assert q['correct_answer'] == 'Inversiya'
    assert question('paragraph-23', 6, grade=10)['correct_answer'] == 'Trisomiya — aneuploidiya'
    assert 20 + 1 == 21 and 21 != 3 * 10
    assert question('paragraph-45', 5, grade=10)['correct_answer'] == f'{42 // 7}x'
