"""Bounded notation parsing, not a source of chemical identities or reactions.

Only reviewed lesson keys say which formula/species/reaction is correct. No
periodic table, reaction predictor, Python evaluation or semantic AI is used.
Structural/ionic formula grading needs its own reviewed future contract.
"""
from collections import Counter
from functools import reduce
from math import gcd
import re

SUBSCRIPTS = str.maketrans('₀₁₂₃₄₅₆₇₈₉', '0123456789')


def text(value):
    if type(value) is not str or len(value) > 80:
        raise ValueError('invalid_answer')
    value = value.strip().translate(SUBSCRIPTS)
    if not value:
        raise ValueError('answer_required')
    # Accept ordinary spacing; do not NFKC-fold superscript charge/valence into
    # atom subscripts. Case remains significant throughout.
    return re.sub(r' +', '', value)


def formula(value):
    value = text(value)
    tokens = re.findall(r'[A-Z][a-z]?|[1-9][0-9]{0,2}|[()]', value)
    if ''.join(tokens) != value:
        raise ValueError('invalid_answer')
    position = 0

    def group(depth=0):
        nonlocal position
        if depth > 3:
            raise ValueError('invalid_answer')
        counts = Counter()
        canonical = []
        terms = 0
        while position < len(tokens) and tokens[position] != ')':
            token = tokens[position]
            position += 1
            if token == '(':
                part, spelling = group(depth+1)
                if position >= len(tokens) or tokens[position] != ')':
                    raise ValueError('invalid_answer')
                position += 1
                spelling = '('+spelling+')'
            elif re.fullmatch(r'[A-Z][a-z]?', token):
                part, spelling = Counter({token: 1}), token
            else:
                raise ValueError('invalid_answer')
            count = 1
            if position < len(tokens) and tokens[position].isdigit():
                count = int(tokens[position]); position += 1
            counts.update({k: v*count for k,v in part.items()})
            if sum(counts.values()) > 100000:
                raise ValueError('invalid_answer')
            canonical.append(spelling+(str(count) if count != 1 else ''))
            terms += 1
        if not terms:
            raise ValueError('invalid_answer')
        return counts, ''.join(canonical)

    counts, spelling = group()
    if position != len(tokens):
        raise ValueError('invalid_answer')
    return spelling, dict(counts)


def equation(value):
    value = text(value).replace('→','=').replace('->','=')
    if value.count('=') != 1:
        raise ValueError('invalid_answer')
    sides, atoms = [], []
    for side in value.split('='):
        terms = side.split('+')
        if not 1 <= len(terms) <= 8 or not all(terms):
            raise ValueError('invalid_answer')
        coefficients, total = Counter(), Counter()
        for term in terms:
            match = re.fullmatch(r'([1-9][0-9]{0,2})?([A-Z(].*)', term)
            if not match:
                raise ValueError('invalid_answer')
            coefficient = int(match[1] or '1')
            species, composition = formula(match[2])
            coefficients[species] += coefficient
            if coefficients[species] > 999:
                raise ValueError('invalid_answer')
            total.update({k: v*coefficient for k,v in composition.items()})
        sides.append(dict(coefficients)); atoms.append(dict(total))
    divisor = reduce(gcd, [n for side in sides for n in side.values()])
    canonical = tuple(tuple(sorted((s,n//divisor) for s,n in side.items())) for side in sides)
    return sides, atoms, canonical
