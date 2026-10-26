"""Bounded chronology arithmetic, without adding historical facts or dates.

Only source-reviewed dates may enter authored questions. These helpers are
mathematics, not evidence for whether an event occurred on a particular date.
"""


def year_index(year, era):
    if (type(year) is not int or not 1 <= year <= 10_000_000
            or type(era) is not str or era not in {'BCE', 'CE'}):
        raise ValueError('positive_year_and_explicit_era_required')
    # Internal index is continuous across 1 BCE -> 1 CE, with no display year 0.
    return 1-year if era == 'BCE' else year


def century(year, era):
    year_index(year, era)
    return (year-1)//100+1


def elapsed_years(start_year, start_era, end_year, end_era):
    delta = year_index(end_year, end_era)-year_index(start_year, start_era)
    if delta < 0:
        raise ValueError('end_must_not_precede_start')
    return delta
