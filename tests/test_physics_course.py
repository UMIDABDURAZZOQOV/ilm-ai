"""Reviewed batches append to the original course without resetting any progress."""

import hashlib

import pytest
from test_physics_v2 import (
    PREFIX,
    answer_all,
    assert_private_absent,
    correct,
    finish,
    start,
    submit,
)
from test_physics_v2 import preview as preview  # noqa: PLC0414 - pytest fixture export
from test_release_hardening import setup as setup  # noqa: PLC0414 - pytest fixture export

from scripts.audit_physics_course import report
from services.assessment_grading import grade_answer
from services.assessment_models import CurriculumLessonV2
from services.models import User
from services.physics_curriculum import (
    DIRECTORY,
    import_batch,
    load_batch,
    load_course,
    validate_batch,
)

# Independent explicit numeric answer oracles. None reads expected_si or calls
# the production arithmetic calculator. Equivalent units and reciprocal powers
# deliberately differ from the content's stored canonical solution strings.
ORACLES = {
    (9, 6): ("0.0000000003", "m", "V/S"),
    (9, 7): ("0,3", "nm", "V*S^-1"),
    (13, 5): ("0.02", "mm/s", "h/t"),
    (13, 6): ("0.000015", "m/s", "h*t^-1"),
    (14, 5): ("850", "g", "1000*x"),
    (14, 6): ("0.375", "kg", "x/1000"),
    (14, 7): ("1600", "kg", "1000*x"),
    (15, 6): ("170", "g", "m3+m1+m2"),
    (15, 7): ("160", "g", "M-m0"),
    (16, 6): ("2.7", "g/cm³", "m/V"),
    (16, 7): ("20", "g", "V*rho"),
    (16, 8): ("30", "cm^3", "m*rho^-1"),
    (16, 9): ("15", "cm3", "V2-V1"),
    (17, 5): ("40", "cm³", "l3*l1*l2"),
    (17, 6): ("2700", "kg/m^3", "m*V^-1"),
    (17, 7): ("18", "cm3", "V2-V1"),
    (17, 8): ("2.5", "g/cm3", "m/V"),
}


ORACLES_BATCH3 = {
    (19, 5): ("2350", "m", "x*1000"),
    (19, 6): ("270", "s", "60*x"),
    (19, 7): ("4500", "s", "3600*x"),
    (19, 8): ("90", "m", "n*l"),
    (20, 5): ("6", "m/s", "s/t"),
    (20, 6): ("30", "m", "t*v"),
    (20, 7): ("12", "s", "s/v"),
    (20, 8): ("3", "m/s", "(s2+s1)/(t2+t1)"),
    (21, 5): ("4.905", "N", "g*m"),
    (21, 6): ("2", "kg", "F/g"),
    (23, 5): ("0.02", "m²", "b*a"),
    (23, 6): ("3", "kPa", "F/S"),
    (23, 7): ("0.1", "kN", "p*S"),
    (23, 8): ("300", "cm²", "F/p"),
    (24, 6): ("160", "N", "F1*(S2/S1)"),
    (24, 7): ("0.12", "kN", "S2/S1*F1"),
}


ORACLES_BATCH4 = {
    (25, 5): ("1962", "Pa", "g*rho*h"),
    (25, 6): ("3.924", "kPa", "rho*h*g"),
    (25, 7): ("20", "cm", "h1*(rho1/rho2)"),
    (26, 6): ("121590", "Pa", "101325*x"),
    (26, 7): ("60.795", "kPa", "x*101325"),
    (27, 6): ("1962", "mN", "rho*V*g"),
    (27, 7): ("3.924", "N", "g*V*rho"),
    (27, 8): ("1.2", "N", "Ph-Ps"),
    (28, 6): ("0.06", "kJ", "s*F"),
    (28, 7): ("12", "N", "A/s"),
    (28, 8): ("5", "m", "A/F"),
    (29, 6): ("29.43", "J", "g*m*h"),
    (29, 7): ("18", "J", "m*v*v/2"),
    (29, 8): ("0.06", "kW", "A/t"),
    (29, 9): ("30", "kJ", "t*N"),
}


ORACLES_BATCH5 = {
    (31, 5): ("2", "N·m", "l*F"),
    (31, 6): ("24", "N", "F1*(l1/l2)"),
    (31, 7): ("20", "cm", "l1*(F1/F2)"),
    (32, 4): ("2", "N", "F1*l1/l2"),
    (32, 5): ("18", "cm", "F1*l1/F2"),
    (33, 5): ("40", "N", "P/2"),
    (33, 6): ("30", "N", "P*(h/s)"),
    (33, 7): ("30", "N", "P*r/R"),
    (33, 8): ("12", "1", "R1*R2/(r1*r2)"),
    (34, 4): ("1.2", "m", "s2*(F2/F1)"),
    (34, 5): ("1.5", "m", "h*2"),
    (34, 6): ("120", "cm", "F2*s2/F1"),
    (35, 5): ("80", "%", "Af/Au"),
    (35, 6): ("180", "J", "Au*eta"),
    (35, 7): ("0.8", "1", "(P*h)/(F*s)"),
}

ORACLES_BATCH7 = {
    (45, 5): ("3000", "mV", "x*1000"),
    (45, 6): ("1800", "mV", "1000*x"),
}

ORACLES_BATCH8 = {
    (50, 5): ("1200", "km", "t*v"),
    (50, 6): ("0.003", "s", "s/v"),
    (52, 5): ("45", "cm", "d"),
    (52, 6): ("12", "cm", "0.5*R"),
    (52, 7): ("24", "cm", "1/(1/F-1/d)"),
    (52, 8): ("15", "cm", "F*d/(d-F)"),
    (53, 5): ("5", "dptr", "F^-1"),
    (53, 6): ("25", "cm", "D^-1"),
    (53, 7): ("2.5", "1/m", "1/F"),
}


ORACLES_BATCH9 = {
    (57, 5): ("300", "Hz", "n/t"),
    (57, 6): ("0.6", "kHz", "n*t^-1"),
    (58, 5): ("1372", "m", "t*v"),
    (58, 6): ("3", "s", "s/v"),
    (60, 4): ("450", "m", "0.5*v*t"),
    (60, 5): ("204", "m", "v*t/2"),
    (60, 6): ("1360", "m", "v*t"),
    (61, 5): ("30", "%", "Ea/Ei"),
    (61, 6): ("0.25", "1", "Ea*Ei^-1"),
}


# Full identity prevents grade7 §9/q6 from using grade6 §9/q6's answer.
NUMERIC_ORACLES = {
    (6, section, number): answer
    for (section, number), answer in (
        ORACLES
        | ORACLES_BATCH3
        | ORACLES_BATCH4
        | ORACLES_BATCH5
        | ORACLES_BATCH7
        | ORACLES_BATCH8
        | ORACLES_BATCH9
    ).items()
}

NUMERIC_ORACLES.update(
    {
        (7, 1, 5): ("8.5", "m/s", "v2+v1"),
        (7, 1, 6): ("21.6", "km/h", "v1+v2"),
        (7, 2, 5): ("3000", "km", "t*v"),
        (7, 2, 6): ("1200", "km", "v*t"),
        (7, 4, 6): ("13", "m", "b+a"),
        (7, 4, 7): ("7", "m", "a-b"),
        (7, 4, 8): ("15", "cm", "k*a"),
        (7, 5, 5): ("70", "cm", "n*d"),
        (7, 5, 6): ("480", "cm", "d*n"),
    }
)

NUMERIC_ORACLES.update(
    {
        (7, 6, 5): ("8", "m/s", "s/t"),
        (7, 6, 6): ("18", "km/h", "s/t"),
        (7, 7, 5): ("42", "m", "t*v"),
        (7, 7, 6): ("30", "s", "s/v"),
        (7, 7, 7): ("3.6", "km", "v*t"),
        (7, 8, 5): ("3", "m/s", "(s1+s2)/(t1+t2)"),
        (7, 8, 6): ("4", "m/s", "(s1+s2)/(t1+t2)"),
        (7, 8, 7): ("6", "m/s", "s/t"),
        (7, 9, 5): ("300", "cm/s2", "(v-v0)/t"),
        (7, 9, 6): ("-3", "m/s²", "(v-v0)/t"),
        (7, 9, 7): ("200", "cm/s2", "v/t-v0/t"),
        (7, 10, 5): ("11", "m/s", "v0+a*t"),
        (7, 10, 6): ("6", "m/s", "a*t+v0"),
        (7, 10, 7): ("9", "m/s", "(v0+v)/2"),
        (7, 10, 8): ("43.2", "km/h", "v0/2+v/2"),
    }
)

NUMERIC_ORACLES.update(
    {
        (7, 11, 4): ("900", "cm", "v0*t+a*t^2/2"),
        (7, 11, 5): ("28", "m", "t*v0+0.5*a*t*t"),
        (7, 11, 6): ("50", "m", "v0*t+a*t^2/2"),
        (7, 12, 5): ("20", "cm/s2", "2*s/(t*t)"),
        (7, 12, 6): ("0.2", "m/s2", "(a1+a2+a3)/3"),
        (7, 13, 4): ("30", "m/s", "v0+g*t"),
        (7, 13, 5): ("24", "m", "t*v0+0.5*g*t*t"),
        (7, 13, 6): ("19.62", "m/s", "g*t+v0"),
        (7, 14, 4): ("2.5", "s", "v0/g"),
        (7, 14, 5): ("-36", "km/h", "v0-g*t"),
        (7, 14, 6): ("40", "m", "v0*t-g*t^2/2"),
        (7, 14, 7): ("28", "m", "t*v0-0.5*g*t*t"),
        (7, 15, 4): ("3", "rad", "s/R"),
        (7, 15, 5): ("4", "rad/s", "phi/t"),
        (7, 15, 6): ("10.8", "km/h", "s/t"),
    }
)


NUMERIC_ORACLES.update(
    {
        (7, 16, 4): ("4.32", "km/h", "R*omega"),
        (7, 16, 5): ("1.5", "s", "t/n"),
        (7, 16, 6): ("0.0025", "kHz", "n/t"),
        (7, 16, 7): ("3.14", "rad/s", "2*p/T"),
        (7, 17, 4): ("200", "cm/s2", "v*v/R"),
        (7, 17, 5): ("1600", "cm", "v^2/ac"),
        (7, 17, 6): ("6", "m/s2", "v^2/R"),
        (7, 18, 5): ("12000", "mN", "F2+F1"),
        (7, 18, 6): ("8", "N", "F1-F2"),
        (7, 18, 7): ("0.3", "kN", "F1-F2"),
        (7, 20, 5): ("1500", "g", "m2+m1"),
        (7, 20, 6): ("600", "g", "m1+m2"),
    }
)


NUMERIC_ORACLES.update(
    {
        (7, 21, 4): ("600", "cm/s2", "F*m^-1"),
        (7, 21, 5): ("2000", "mN", "a*m"),
        (7, 21, 6): ("4000", "g", "F/a"),
        (7, 21, 7): ("4", "m/s2", "F/m"),
        (7, 22, 5): ("18", "N", "1*F1"),
        (7, 22, 6): ("2", "m/s2", "m1*a1/m2"),
        (7, 22, 7): ("0.12", "kN", "F1"),
        (7, 23, 4): ("4", "N", "m*v*v/R"),
        (7, 23, 5): ("3000", "mN", "m*v^2/R"),
        (7, 23, 6): ("0.01", "kN", "m*v^2/R"),
        (7, 24, 5): ("6", "N", "x*k"),
        (7, 24, 6): ("0.2", "kN/m", "F/x"),
        (7, 24, 7): ("3", "cm", "F/k"),
        (7, 24, 8): ("200", "N/m", "E*S/l"),
        (7, 25, 5): ("50", "N/m", "g*m/x"),
        (7, 25, 6): ("0.05", "kN/m", "(k1+k2+k3)/3"),
        (7, 25, 7): ("50", "N/m", "m*g/x"),
    }
)


NUMERIC_ORACLES.update(
    {
        (7, 26, 4): ("6.67e-11", "N", "G*m1*m2/r^2"),
        (7, 26, 5): ("1.334e-8", "N", "G*m2*m1/(r*r)"),
        (7, 26, 6): ("3.2016e-9", "N", "G*m1*m2/r^2"),
        (7, 27, 4): ("7500", "mN", "g*m"),
        (7, 27, 5): ("3000", "g", "F/g"),
        (7, 27, 6): ("2.45", "N", "m*g"),
        (7, 28, 4): ("8", "N", "m*g"),
        (7, 28, 5): ("0.0196", "kN", "g*m"),
        (7, 29, 4): ("360", "N", "m*g+m*a"),
        (7, 29, 5): ("240", "N", "m*(g-a)"),
        (7, 29, 6): ("150", "%", "1+a/g"),
        (7, 29, 7): ("0", "N", "m*g-m*a"),
        (7, 30, 4): ("1400", "cm", "t*v0"),
        (7, 30, 5): ("45", "m", "g*t^2/2"),
        (7, 30, 6): ("400.2", "cm/s2", "G*M/(R+h)^2"),
        (7, 30, 7): ("6400", "km", "v*v/g"),
    }
)


NUMERIC_ORACLES.update(
    {
        (7, 31, 6): ("360", "km", "v^2/g-R"),
        (7, 32, 4): ("4000", "mN", "F"),
        (7, 32, 5): ("8", "N", "1*F"),
        (7, 33, 4): ("12", "N", "N*mu"),
        (7, 33, 5): ("30", "%", "f/N"),
        (7, 33, 6): ("2000", "mN", "c*P/r"),
        (7, 33, 7): ("0.2", "N", "P*c/r"),
        (7, 34, 5): ("30", "%", "F/(m*g)"),
        (7, 34, 6): ("0.3", "1", "(mu1+mu2+mu3)/3"),
        (7, 34, 7): ("0.4", "1", "F/m/g"),
    }
)


NUMERIC_ORACLES.update(
    {
        (7, 36, 4): ("6", "kg*m/s", "t*F"),
        (7, 36, 5): ("-2", "N*s", "v*m"),
        (7, 36, 6): ("-8", "kg*m/s", "m*v-m*v0"),
        (7, 36, 7): ("-2", "N*s", "F*t"),
        (7, 37, 4): ("5", "N*s", "m1*v1+m2*v2"),
        (7, 37, 5): ("7.2", "km/h", "(m1*v1+m2*v2)/(m1+m2)"),
        (7, 37, 6): ("-1", "m/s", "(m1*v1+m2*v2)/(m1+m2)"),
        (7, 37, 7): ("0", "m/s", "(m1*v1+m2*v2)/(m1+m2)"),
        (7, 38, 4): ("-0.72", "km/h", "-m*u/M"),
        (7, 38, 5): ("-0.2", "m/s", "-(m*u)/M"),
        (7, 38, 6): ("0.6", "m/s", "-m*u/M"),
        (7, 39, 4): ("0.024", "kJ", "s*Fpr"),
        (7, 39, 5): ("-20", "J", "Fpr*s"),
        (7, 39, 6): ("0", "J", "Fpr*s"),
        (7, 39, 7): ("3000", "mJ", "Fpr*s"),
        (7, 40, 5): ("1.2", "J", "h*F"),
        (7, 40, 6): ("0.32", "J", "F*s"),
        (7, 40, 7): ("0.0000005", "MJ", "F*h"),
    }
)


NUMERIC_ORACLES.update(
    {
        (7, 41, 4): ("20", "J", "g*m*h"),
        (7, 41, 5): ("80", "J", "m*g*(h1-h2)"),
        (7, 41, 6): ("-0.0196", "kJ", "m*g*h1-m*g*h2"),
        (7, 42, 4): ("9000", "mJ", "0.5*m*v^2"),
        (7, 42, 5): ("4", "J", "m*v*v/2"),
        (7, 42, 6): ("21", "J", "m*(v2^2-v1^2)/2"),
        (7, 42, 7): ("-24", "J", "m*v2^2/2-m*v1^2/2"),
        (7, 43, 5): ("38", "J", "m*g*h+m*v^2/2"),
        (7, 43, 6): ("1", "J", "k*x^2/2"),
        (7, 43, 7): ("20", "J", "Ep1-Ep2+Ek1"),
        (7, 43, 8): ("2", "J", "0.5*k*x*x"),
        (7, 44, 5): ("40", "cm/s2", "2*s/(t*t)"),
        (7, 44, 6): ("7.2", "km/h", "a*t+v0"),
        (7, 44, 7): ("0.5", "J", "m*v^2/2"),
        (7, 45, 4): ("0.0003", "MW", "A/t"),
        (7, 45, 5): ("2000", "W*s", "t*N"),
        (7, 45, 6): ("120000", "mW", "v*F"),
        (7, 45, 7): ("400", "N", "N*v^-1"),
        (7, 46, 6): ("60", "%", "Af/Au"),
        (7, 46, 7): ("0.4", "kJ", "Au*eta"),
        (7, 46, 8): ("60", "%", "m*g*h/(N*t)"),
    }
)


NUMERIC_ORACLES.update(
    {
        (8, 2, 5): ("8e-19", "C", "e*n"),
        (8, 2, 6): ("20", "1", "q/e"),
        (8, 2, 7): ("1.82e-30", "kg", "m0*n"),
        (8, 3, 4): ("60", "uN", "k*q1*q2/r^2"),
        (8, 3, 5): ("18", "mN", "k*q2*q1/(r*r)"),
        (8, 3, 6): ("0.2", "N", "k*q1*q2/r^2"),
        (8, 4, 5): ("4", "nC", "sqrt(F*r^2/k)"),
        (8, 4, 6): ("4e10", "1", "q/e"),
        (8, 4, 7): ("-3", "nC", "(q1+q2)/2"),
        (8, 4, 8): ("4.516", "1", "(q1+q2)^2/(4*q1*q2)"),
        (8, 5, 5): ("3000", "N/C", "F/q"),
        (8, 5, 6): ("6", "µN", "q*E"),
        (8, 5, 7): ("900", "N/C", "k*q/r^2"),
        (8, 5, 8): ("400", "N/C", "E0/eps"),
        (8, 5, 9): ("3", "1", "E0/E"),
    }
)


NUMERIC_ORACLES.update(
    {
        (8, 7, 5): ("4", "nC", "F/E"),
        (8, 7, 6): ("3e6", "1", "F/e/E"),
        (8, 7, 7): ("6", "1", "k*q/(E*r^2)"),
        (8, 7, 8): ("2", "nC", "m*g/E"),
        (8, 8, 6): ("1.36", "km", "v*t"),
        (8, 8, 7): ("85000", "cm", "t*v"),
    }
)


NUMERIC_ORACLES.update(
    {
        (8, 11, 5): ("4000", "mV", "A/q"),
        (8, 11, 6): ("0.020", "kJ", "U*q"),
        (8, 11, 7): ("9", "C", "A/U"),
        (8, 11, 8): ("6", "V", "U0*n"),
        (8, 12, 5): ("200", "mA", "q/t"),
        (8, 12, 6): ("2", "C", "t*I"),
        (8, 12, 7): ("2.5", "min", "q/I"),
        (8, 12, 8): ("1000000000000000000", "1", "t*I/e"),
        (8, 13, 5): ("0.072", "kJ", "I*t*U"),
        (8, 13, 6): ("6000", "mV", "A/I/t"),
        (8, 13, 7): ("0.0000000182", "g", "m0*(I*t/e)"),
        (8, 13, 8): ("2.5", "min", "q/I"),
        (8, 15, 6): ("0.0088", "kΩ", "l*rho/S"),
        (8, 15, 7): ("0.0000011", "ohm*m", "S*R/l"),
        (8, 15, 8): ("200", "cm", "S*R/rho"),
        (8, 15, 9): ("0.5", "mm2", "l*rho/R"),
    }
)


NUMERIC_ORACLES.update(
    {
        (8, 17, 5): ("30", "mA", "U/R"),
        (8, 17, 6): ("6000", "mV", "R*I"),
        (8, 17, 7): ("0.06", "kΩ", "U/I"),
        (8, 17, 8): ("500", "mA", "U*S/rho/l"),
        (8, 18, 5): ("1500", "cm", "U*S/rho/I"),
        (8, 18, 6): ("1000", "uA", "U*S/(rho*l)"),
        (8, 18, 7): ("900", "mV", "rho*l*I/S"),
        (8, 18, 8): ("40", "Ω", "t*U/q"),
        (8, 18, 9): ("4000000000000000000", "1", "U*t/R/e"),
        (8, 19, 5): ("0.1", "kohm", "U/I"),
        (8, 19, 6): ("100", "ohm", "(R4+R3+R2+R1)/4"),
    }
)


NUMERIC_ORACLES.update(
    {
        (8, 21, 5): ("0.04", "kΩ", "R3+R2+R1"),
        (8, 21, 6): ("6000", "mV", "U2+U1"),
        (8, 21, 7): ("200", "mA", "U/(R1+R2)"),
        (8, 21, 8): ("3", "V", "R1*U/(R1+R2)"),
        (8, 22, 5): ("400000", "uA", "I2+I1"),
        (8, 22, 6): ("7.2", "ohm", "1/(1/R1+1/R2)"),
        (8, 22, 7): ("6", "Ω", "R1*R2*R3/(R1*R2+R1*R3+R2*R3)"),
        (8, 22, 8): ("200", "mA", "U/R"),
        (8, 23, 5): ("4.5", "V", "U3+U2+U1"),
        (8, 24, 5): ("0.26", "kohm", "R2+R1"),
        (8, 24, 6): ("120", "ohm", "1/(1/R1+1/R2)"),
        (8, 25, 5): ("8", "Ω", "R2*R3/(R2+R3)+R1"),
        (8, 25, 6): ("2500", "mA", "U/(R1+R2*R3/(R2+R3))"),
    }
)


NUMERIC_ORACLES.update(
    {
        (8, 26, 5): ("100", "mA", "U/(R1+R2)"),
        (8, 26, 6): ("3000", "mV", "U*R1/(R1+R2)"),
        (8, 26, 7): ("750", "mA", "U/R1+U/R2"),
        (8, 27, 5): ("5000", "pF", "q/U"),
        (8, 27, 6): ("0.045", "uC", "U*C"),
        (8, 27, 7): ("6", "V", "q/C"),
        (8, 27, 8): ("0.0354", "nF", "e0*eps*S/d"),
        (8, 28, 5): ("10000", "nF", "C2+C1"),
        (8, 28, 6): ("3000", "nF", "1/(1/C1+1/C2)"),
        (8, 28, 7): ("3", "uF", "1/(1/C1+1/C2+1/C3)"),
        (8, 28, 8): ("20", "uC", "C*U"),
        (8, 29, 5): ("10", "mm", "e0*eps*a*a/C"),
        (8, 29, 6): ("2", "1", "C*d/e0/S"),
        (8, 29, 7): ("9000", "nF", "C3+1/(1/C1+1/C2)"),
        (8, 30, 5): ("0.162", "kJ", "I*t*U"),
        (8, 30, 6): ("0.240", "kJ", "I*I*R*t"),
        (8, 30, 7): ("0.720", "kJ", "U*U*t/R"),
    }
)


NUMERIC_ORACLES.update(
    {
        (8, 31, 5): ("3000", "mW", "U*I"),
        (8, 31, 6): ("0.09", "kWh", "t*P"),
        (8, 31, 7): ("24", "ohm", "U*U/P"),
        (8, 31, 8): ("5.5", "kWh", "W2-W1"),
        (8, 32, 5): ("1500", "mA", "P/U"),
        (8, 32, 6): ("6", "W", "R1*P1/R2"),
        (8, 32, 7): ("0.020", "kW", "R2*P1/R1"),
        (8, 33, 5): ("1200", "mW", "I*U"),
        (8, 33, 6): ("1.2", "W", "(P3+P2+P1)/3"),
        (8, 34, 5): ("0.720", "kJ", "I*I*R*t"),
        (8, 34, 6): ("144", "J", "U*U*t/R"),
        (8, 34, 7): ("60", "%", "Af/At"),
        (8, 34, 8): ("75", "%", "Pf/Pt"),
        (8, 34, 9): ("2000", "mA", "(Q/(R*t))^(1/2)"),
        (8, 35, 5): ("0.864", "kJ", "U*I*t*eta"),
        (8, 35, 6): ("30", "1", "P1/P2"),
        (8, 35, 7): ("0.180", "kJ", "R1*A1/R2"),
    }
)


NUMERIC_ORACLES.update(
    {
        (8, 36, 6): ("0.072", "kJ", "I*I*R*t"),
        (8, 39, 5): ("5600", "mV", "rho*l*I/S"),
        (8, 39, 6): ("3000", "mA", "(P3+P2+P1)/U"),
        (8, 39, 7): ("0.060", "kJ", "R1*Q1/R2"),
        (8, 39, 8): ("0.100", "kJ", "R2*Q1/R1"),
    }
)


NUMERIC_ORACLES.update(
    {
        (8, 42, 5): ("0.01974", "g", "q*k"),
        (8, 42, 6): ("6.08", "mg", "I*t*k"),
        (8, 42, 7): ("20", "C", "m/k"),
        (8, 42, 8): ("1000", "mA", "m/k/t"),
        (8, 42, 9): ("0.329", "mg/C", "m/I/t"),
        (8, 43, 5): ("1.119", "mg/C", "M/Z/F"),
        (8, 43, 6): ("2.16", "g", "M*q/Z/F"),
        (8, 43, 7): ("48250", "C", "F*Z*n"),
        (8, 44, 5): ("93.92", "C", "S*h*rho/k"),
        (8, 44, 6): ("0.1974", "g", "P*t*k/U"),
        (8, 44, 7): ("2.51", "µm", "I*t*k/(2*a*b*rho)"),
    }
)


NUMERIC_ORACLES.update(
    {
        (8, 46, 5): ("400", "uA", "e*N/t"),
        (8, 46, 6): ("6250000000000000", "1", "t*I/e"),
        (8, 46, 7): ("20000000000000000", "1", "A/U/e"),
    }
)


NUMERIC_ORACLES.update(
    {
        (8, 53, 5): ("240", "mN", "I*l*B"),
        (8, 53, 6): ("2000", "mA", "F/B/l"),
        (8, 53, 7): ("100", "mT", "F/I/l"),
        (8, 53, 8): ("20", "cm", "F/B/I"),
        (8, 54, 5): ("2", "A", "F/(B*l)"),
        (8, 54, 6): ("10000", "uT", "F/(I*l)"),
        (8, 54, 7): ("60", "mN", "B*I*l"),
        (8, 54, 8): ("480", "C", "F*t/B/l"),
        (8, 54, 9): ("40", "mN", "q*B*l/t"),
        (8, 54, 10): ("200", "mm", "F/(B*I)"),
    }
)


NUMERIC_ORACLES.update(
    {
        (8, 56, 5): ("0.24", "pN", "B*v*q"),
        (8, 56, 6): ("0.0000000000000000006", "C", "F/v/B"),
        (8, 56, 7): ("5000", "km/s", "F/q/B"),
        (8, 56, 8): ("500", "mT", "F/q/v"),
        (8, 60, 5): ("0.16", "pN", "q*v*B"),
        (8, 60, 6): ("0.00000000000000000064", "C", "F/(v*B)"),
        (8, 60, 7): ("500000", "uT", "F/(q*v)"),
        (8, 60, 8): ("3000", "km/s", "F/(q*B)"),
        (8, 60, 9): ("0.288", "pN", "B*v*q"),
        (8, 60, 10): ("100", "mT", "F/q/v"),
    }
)


NUMERIC_ORACLES.update(
    {
        (9, 2, 5): ("0.5", "nm", "V*S^-1"),
        (9, 2, 6): ("24", "1", "m0*u^-1"),
        (9, 2, 7): ("2.988e-26", "kg", "u*Mr"),
        (9, 2, 8): ("20000000000000000000000000", "1", "m*m0^-1"),
        (9, 2, 9): ("200000000000000000000000", "1", "V*rho/m0"),
        (9, 3, 5): ("3.011e23", "1", "NA*nu"),
        (9, 3, 6): ("1.5", "mol", "N*NA^-1"),
        (9, 3, 7): ("2", "mol", "m*M^-1"),
        (9, 3, 8): ("11", "g", "M*nu"),
        (9, 3, 9): ("30.11", "g/mol", "NA*m0"),
        (9, 3, 10): ("5e-26", "kg", "M*NA^-1"),
        (9, 3, 11): ("6.022e26", "m^-3", "N*V^-1"),
        (9, 3, 12): ("0.3", "g/cm3", "m0*n"),
        (9, 4, 5): ("2e22", "1", "S*l*rho/m0"),
        (9, 4, 6): ("3e26", "m⁻³", "m*NA/M/V"),
        (9, 4, 7): ("1.4e20", "1", "S*h*rho*NA/M"),
        (9, 4, 8): ("3200", "cm2", "nu*M/rho/h"),
        (9, 4, 9): ("2", "nm", "D*k^-1"),
        (9, 5, 5): ("100", "kPa", "v^2*rho/3"),
        (9, 5, 6): ("0.6", "km/s", "(3*p/rho)^(1/2)"),
        (9, 5, 7): ("64", "kPa", "m0*n*v^2/3"),
        (9, 5, 8): ("80", "kPa", "n*E*2/3"),
        (9, 5, 9): ("3e-21", "J", "3*p/2/n"),
        (9, 5, 10): ("1.8", "kg/m3", "3*p/(v*v)"),
    }
)


NUMERIC_ORACLES.update(
    {
        (9, 6, 5): ("240", "K", "273.15+theta"),
        (9, 6, 6): ("8.28e-21", "J", "k*T*3/2"),
        (9, 6, 7): ("82.8", "kPa", "k*T*n"),
        (9, 6, 8): ("3e25", "m⁻³", "p/k/T"),
        (9, 6, 9): ("0.6", "kJ", "p*V*3/2"),
        (9, 7, 5): ("0.6434", "km/s", "(3*k*T/m0)^(1/2)"),
        (9, 7, 6): ("1797.48", "km/h", "(3*R*T/M)^0.5"),
        (9, 7, 7): ("600", "m/s", "(2*E/m0)^(1/2)"),
        (9, 7, 8): ("8.3076", "J/(mol*K)", "NA*k"),
        (9, 7, 9): ("0.5", "km/s", "R*(R-r)*omega/s"),
        (9, 7, 10): ("320.9", "K", "M*v*v/(3*R)"),
        (9, 8, 5): ("500", "K", "T2*M1/M2"),
        (9, 8, 6): ("60", "K", "DT/(v2^2/v1^2-1)"),
        (9, 8, 7): ("300", "K", "2*E/3/k"),
        (9, 9, 5): ("300", "kPa", "R*T*nu/V"),
        (9, 9, 6): ("16.62", "L", "T*R*nu/p"),
        (9, 9, 7): ("2", "mol", "p*V/R/T"),
        (9, 9, 8): ("5.6", "g", "M*p*V/R/T"),
        (9, 9, 9): ("300", "kPa", "p1*V1*T2/T1/V2"),
        (9, 10, 5): ("0.6", "L", "V1*p1/p2"),
        (9, 10, 6): ("300", "kPa", "V1*p1/V2"),
        (9, 10, 7): ("0.003", "g/cm3", "p2*rho1/p1"),
        (9, 10, 8): ("60", "kPa", "V2*dp/(V1-V2)"),
        (9, 10, 9): ("4", "L", "V1*p1/(p1+dp)"),
    }
)


NUMERIC_ORACLES.update(
    {
        (9, 11, 5): ("12", "L", "T2*V1/T1"),
        (9, 11, 6): ("210", "K", "T1*V2/V1"),
        (9, 11, 7): ("160", "K", "T1*(V1-V2)/V1"),
        (9, 11, 8): ("60", "K", "T1*(V2/V1-1)"),
        (9, 12, 5): ("150", "kPa", "T2*p1/T1"),
        (9, 12, 6): ("400", "K", "T1*p2/p1"),
        (9, 12, 7): ("90", "kPa", "T1*dp/(T2-T1)"),
        (9, 13, 5): ("4", "mm", "V*S^-1"),
        (9, 13, 6): ("7.5", "mm", "L*N^-1"),
        (9, 13, 7): ("60", "m3", "c*b*a"),
        (9, 13, 8): ("0.00116", "g/cm3", "M*p/R/T"),
        (9, 13, 9): ("2e25", "m^-3", "p/k/T"),
        (9, 13, 10): ("1200000000000000000000000000", "1", "V*n"),
        (9, 14, 5): ("75", "kPa", "p1*f*T2/T1"),
        (9, 14, 6): ("400", "K", "T1*rho1/rho2"),
        (9, 14, 7): ("300", "K", "DT*f^-1"),
        (9, 14, 8): ("3", "1", "rho*g*h/p0+1"),
        (9, 14, 9): ("25", "m", "p0*(x-1)/rho/g"),
        (9, 15, 5): ("7.479", "kJ", "nu*R*T*3/2"),
        (9, 15, 6): ("-3.7395", "kJ", "nu*R*(T2-T1)*3/2"),
        (9, 15, 7): ("200", "kPa", "2*U/3/V"),
        (9, 15, 8): ("0.45", "kJ", "p*(V2-V1)*3/2"),
    }
)


def new_answer(lesson, q):
    if q["grading_spec"]["kind"] == "numeric_quantity":
        grade = int(lesson["topic_id"].split("-")[1])
        number = int(q["key"].rsplit("q", 1)[1])
        value, unit, formula = NUMERIC_ORACLES[(grade, lesson["sequence"], number)]
        return {"value": value, "unit": unit, "formula": formula}
    return correct(q)


def test_original_frozen_content_and_honest_course_coverage():
    assert (
        hashlib.sha256((DIRECTORY / "grade6_batch1.json").read_bytes()).hexdigest()
        == "8d13627ce9275bda5a402b86d4ea94d67b1892c1538189c88dcc51891a3c6a78"
    )
    data = report()
    assert (data["authored"], data["remaining"], data["source_total"]) == (
        182,
        134,
        316,
    )
    assert [r["authored"] for r in data["grades"]] == [61, 46, 60, 15, 0, 0]
    row = data["grades"][0]
    assert (
        row["cards"],
        row["assessments"],
        row["frq"],
        row["laboratories"],
        row["practicals"],
    ) == (254, 394, 88, 7, 1)
    assert row["next_section"] is None
    assert len(load_course()) == 33
    with pytest.raises(ValueError, match="batch_not_reviewed"):
        load_batch("arbitrary_unreviewed_file")


def test_batch_two_independent_calculation_and_wrong_answers():
    doc = load_batch("grade6_batch2")
    assert validate_batch(doc) == {
        "lessons": 10,
        "cards": 41,
        "formulas": 14,
        "worked_examples": 12,
        "assessments": 67,
        "frq": 17,
    }
    seen = set()
    for lesson in doc["lessons"]:
        for q in lesson["assessments"]:
            answer = new_answer(lesson, q)
            spec = q["grading_spec"]
            assert grade_answer(spec, answer) == "correct", q["key"]
            if spec["kind"] == "numeric_quantity":
                seen.add((lesson["sequence"], int(q["key"].rsplit("q", 1)[1])))
                assert (
                    grade_answer(spec, {**answer, "unit": "s"}) == "dimension_mismatch"
                )
                assert (
                    grade_answer(spec, {**answer, "value": "999999999"})
                    == "out_of_tolerance"
                )
                assert grade_answer(spec, {**answer, "formula": "1"}) == "wrong_formula"
                assert (
                    grade_answer(spec, {**answer, "formula": "V.__class__"})
                    != "correct"
                )
                assert grade_answer(spec, {**answer, "value": "1/0"}) == "domain_error"
    assert seen == set(ORACLES)


@pytest.mark.parametrize(
    "tamper",
    [
        "gap",
        "negative",
        "dimension",
        "units",
        "untaught",
        "source",
        "physical",
        "frozen",
    ],
)
def test_new_batch_review_rejects_unsupported_or_changed_content(tamper):
    doc = load_batch("grade6_batch2")
    q = doc["lessons"][-1]["assessments"][-1]
    if tamper == "gap":
        doc["lessons"].pop(2)
    if tamper == "negative":
        q["public"]["givens"][1]["value"] = "-1"
    if tamper == "dimension":
        q["grading_spec"]["dimension"] = "length"
    if tamper == "units":
        q["public"]["unit_choices"] = ["s"]
    if tamper == "untaught":
        doc["lessons"][-1]["formulas"] = []
    if tamper == "source":
        q["source_refs"][0]["page_text_sha256"][0] = "0" * 64
    if tamper == "physical":
        doc["lessons"][-1]["review"]["physical_experiment_completed"] = True
    if tamper == "frozen":
        doc["lessons"][-1]["cards"][0]["body"] += " Unreviewed addition."
    with pytest.raises(ValueError):
        validate_batch(doc)
        import_batch(None, doc)  # evidence check fails before opening any DB


def test_all_seventeen_http_lessons_replay_append_and_private_keys(preview):
    client, factory = preview
    original = load_batch()
    for n in range(1, 8):
        attempt = start(client, n).json()
        answer_all(client, attempt, n)
        assert finish(client, attempt).json()["xp_awarded"] == 10
    with factory.begin() as db:
        old_hashes = {l.key: l.content_sha256 for l in db.query(CurriculumLessonV2)}
        for _ in range(2):
            for document in load_course():
                import_batch(db, document)
        assert all(
            db.get(CurriculumLessonV2, key).content_sha256 == digest
            for key, digest in old_hashes.items()
        )
        assert db.get(User, 1).xp_total == 70
    cat = client.get(f"{PREFIX}/catalog").json()
    assert [r["state"] for r in cat["lessons"][:9]] == ["completed"] * 7 + [
        "available",
        "locked",
    ]
    assert not cat["course_complete"]
    assert cat["grade_content_complete"] and len(cat["lessons"]) == 61
    assert [
        r["state"] for r in client.get(f"{PREFIX}/catalog?grade=7").json()["lessons"]
    ] == ["available"] + ["locked"] * 45
    assert client.get(f"{PREFIX}/catalog?grade=12").status_code == 422
    for lesson in load_batch("grade6_batch2")["lessons"]:
        response = start(client, lesson["sequence"])
        assert response.status_code == 200, response.text
        attempt = response.json()
        assert_private_absent(attempt)
        for q in lesson["assessments"]:
            answer = new_answer(lesson, q)
            result = submit(client, attempt, q["key"], answer)
            assert result.status_code == 200 and result.json()["is_correct"], (
                q["key"],
                result.text,
            )
            assert submit(client, attempt, q["key"], answer).json() == result.json()
        result = finish(client, attempt)
        assert result.status_code == 200 and result.json()["xp_awarded"] == 10
        assert finish(client, attempt).json() == result.json()
    with factory() as db:
        assert db.get(User, 1).xp_total == 170
    assert load_batch() == original


def test_import_gap_does_not_unlock_next_section(preview):
    client, factory = preview
    with factory.begin() as db:
        import_batch(db, load_batch("grade6_batch2"))
        db.query(CurriculumLessonV2).filter_by(sequence=1).update({"sequence": 100})
    rows = client.get(f"{PREFIX}/catalog").json()["lessons"]
    assert rows and all(r["state"] == "locked" for r in rows)


def test_batch_three_independent_answers_and_every_reviewed_equivalent():
    document = load_batch("grade6_batch3")
    assert validate_batch(document) == {
        "lessons": 7,
        "cards": 27,
        "formulas": 15,
        "worked_examples": 8,
        "assessments": 48,
        "frq": 16,
    }
    seen = set()
    for lesson in document["lessons"]:
        for q in lesson["assessments"]:
            answer = new_answer(lesson, q)
            spec = q["grading_spec"]
            assert grade_answer(spec, answer) == "correct", q["key"]
            if spec["kind"] != "numeric_quantity":
                continue
            seen.add((lesson["sequence"], int(q["key"].rsplit("q", 1)[1])))
            for expression in spec["formula"]["equivalents"]:
                assert (
                    grade_answer(spec, {**answer, "formula": expression}) == "correct"
                )
            wrong_unit = "kg" if spec["dimension"] == "time" else "s"
            assert (
                grade_answer(spec, {**answer, "unit": wrong_unit})
                == "dimension_mismatch"
            )
            assert grade_answer(spec, {**answer, "formula": "1"}) == "wrong_formula"
            assert (
                grade_answer(spec, {**answer, "value": "999999999"})
                == "out_of_tolerance"
            )
    assert seen == set(ORACLES_BATCH3)


def test_all_reviewed_http_content_and_replay(preview):
    client, factory = preview
    with factory.begin() as db:
        for document in load_course():
            import_batch(db, document)
    for document in load_course():
        for lesson in document["lessons"]:
            issued = start(client, lesson["sequence"], grade=document["grade"])
            assert issued.status_code == 200, issued.text
            attempt = issued.json()
            assert_private_absent(attempt)
            for q in lesson["assessments"]:
                answer = (
                    correct(q)
                    if document["grade"] == 6 and lesson["sequence"] < 8
                    else new_answer(lesson, q)
                )
                graded = submit(client, attempt, q["key"], answer)
                assert graded.status_code == 200 and graded.json()["is_correct"], (
                    q["key"],
                    graded.text,
                )
                assert submit(client, attempt, q["key"], answer).json() == graded.json()
            result = finish(client, attempt)
            assert result.status_code == 200 and result.json()["xp_awarded"] == 10
            assert finish(client, attempt).json() == result.json()
    with factory() as db:
        assert db.get(User, 1).xp_total == 1820


@pytest.mark.parametrize(
    "case", ["gravity", "zero_area", "fraction_steps", "mixed_areas", "zero_time"]
)
def test_source_domains_not_silently_relaxed(case):
    from copy import deepcopy

    document = deepcopy(load_batch("grade6_batch3"))
    locations = {
        "gravity": (3, 4, 1, "value", "10"),
        "zero_area": (5, 5, 1, "value", "0"),
        "fraction_steps": (1, 7, 1, "value", "2.5"),
        "mixed_areas": (6, 5, 2, "unit", "m2"),
        "zero_time": (2, 4, 1, "value", "0"),
    }
    li, qi, gi, key, bad = locations[case]
    document["lessons"][li]["assessments"][qi]["public"]["givens"][gi][key] = bad
    with pytest.raises(ValueError):
        validate_batch(document)


def test_batch_four_answers_alternatives_and_invalid_domains():
    from copy import deepcopy

    from services.physics_curriculum import calculation_value

    document = load_batch("grade6_batch4")
    assert validate_batch(document) == {
        "lessons": 5,
        "cards": 22,
        "formulas": 12,
        "worked_examples": 7,
        "assessments": 39,
        "frq": 15,
    }
    seen = set()
    for lesson in document["lessons"]:
        for q in lesson["assessments"]:
            answer = new_answer(lesson, q)
            spec = q["grading_spec"]
            assert grade_answer(spec, answer) == "correct", q["key"]
            if spec["kind"] != "numeric_quantity":
                continue
            seen.add((lesson["sequence"], int(q["key"].rsplit("q", 1)[1])))
            for expression in spec["formula"]["equivalents"]:
                assert (
                    grade_answer(spec, {**answer, "formula": expression}) == "correct"
                )
            assert grade_answer(spec, {**answer, "unit": "s"}) == "dimension_mismatch"
            assert (
                grade_answer(spec, {**answer, "value": "999999999"})
                == "out_of_tolerance"
            )
            assert grade_answer(spec, {**answer, "formula": "1"}) == "wrong_formula"
    assert seen == set(ORACLES_BATCH4)
    # Independent malformed-domain probes: no negative pressure-height,
    # impossible reading difference or zero-time power accepted by an author.
    for li, qi, gi, bad in [(0, 4, 2, "-1"), (2, 7, 1, "10"), (4, 7, 1, "0")]:
        q = deepcopy(document["lessons"][li]["assessments"][qi])
        q["public"]["givens"][gi]["value"] = bad
        with pytest.raises(ValueError):
            calculation_value(q)


def test_batch_five_independent_moments_efficiency_and_source_continuation():
    import json
    from copy import deepcopy

    from services.physics_curriculum import calculation_value

    doc = load_batch("grade6_batch5")
    assert validate_batch(doc) == {
        "lessons": 6,
        "cards": 24,
        "formulas": 14,
        "worked_examples": 6,
        "assessments": 39,
        "frq": 15,
    }
    seen = set()
    for lesson in doc["lessons"]:
        for q in lesson["assessments"]:
            spec = q["grading_spec"]
            answer = new_answer(lesson, q)
            assert grade_answer(spec, answer) == "correct", q["key"]
            if spec["kind"] != "numeric_quantity":
                continue
            seen.add((lesson["sequence"], int(q["key"].rsplit("q", 1)[1])))
            for expression in spec["formula"]["equivalents"]:
                assert (
                    grade_answer(spec, {**answer, "formula": expression}) == "correct"
                )
            assert grade_answer(spec, {**answer, "unit": "s"}) == "dimension_mismatch"
            assert (
                grade_answer(spec, {**answer, "value": "999999999"})
                == "out_of_tolerance"
            )
    assert seen == set(ORACLES_BATCH5)
    archived = json.loads((DIRECTORY / "physics_sources.json").read_text())["books"][0]
    assert (
        next(r for r in archived["records"] if r["id"] == "physics-6-section-32")[
            "pdf_end"
        ]
        == 89
    )
    assert doc["lessons"][2]["source_refs"][0]["pdf_pages"] == [89, 90]
    tampered = deepcopy(doc)
    tampered["lessons"][2]["source_refs"][0].pop("extent_note")
    with pytest.raises(ValueError, match="citation_outside_topic"):
        validate_batch(tampered)
    # Physically impossible incline geometry / >100% efficiency are rejected.
    for li, qi, gi, bad in [(3, 5, 1, "5"), (5, 4, 0, "200"), (5, 5, 0, "120")]:
        q = deepcopy(doc["lessons"][li]["assessments"][qi])
        q["public"]["givens"][gi]["value"] = bad
        with pytest.raises(ValueError):
            calculation_value(q)
