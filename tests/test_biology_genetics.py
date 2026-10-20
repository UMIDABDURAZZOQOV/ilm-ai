"""Independent probability checks for the reviewed textbook genetics exercises."""
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from itertools import product
from types import SimpleNamespace

import pytest

from services.curriculum_validation import load_documents, load_lesson_set, validate_lesson
from services.study import grade


def question(slug, number):
    lesson = next(l for l in load_lesson_set() if l['key'] == f'biology-9-{slug}-v1')
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
