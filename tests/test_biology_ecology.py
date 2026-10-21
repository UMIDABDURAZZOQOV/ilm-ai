"""Independent unit-aware checks for reviewed ecology models, not real field data."""
from fractions import Fraction

import pytest

from services.curriculum_validation import load_lesson_set


def authored_answer(paragraph, number):
    lesson = next(l for l in load_lesson_set() if l['key'] == f'biology-11-{paragraph}-v1')
    return lesson['questions'][number - 1]['correct_answer']


@pytest.mark.parametrize('slug,number,expected', [
    ('paragraph-14', 3, f'{180 // 6} tup/ga'),
    ('paragraph-14', 7, f'{14 - 9} individ ortadi'),
    ('paragraph-17', 6, f'{200 * 5} g'),
    ('paragraph-18', 3, f'{int(25000 * Fraction(1, 10) ** 2)} kJ'),
    ('laboratory-2', 3, f'{int(5000 * Fraction(1, 10) ** 2)} kg'),
    ('laboratory-2', 4, f'{sum(6 * 10 ** level for level in range(4))} kg'),
])
def test_reviewed_ecology_values_preserve_units_and_trophic_steps(slug, number, expected):
    assert authored_answer(slug, number) == expected


def test_trophic_transfer_count_is_edges_not_number_of_levels():
    values = [Fraction(9000)]
    while values[-1] > 9:
        values.append(values[-1] / 10)
    assert values == [9000, 900, 90, 9]
    assert authored_answer('laboratory-2', 5) == f'{len(values) - 1} o‘tish'
