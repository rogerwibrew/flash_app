import pytest
import numpy as np
from flash.thermo import antoine_pressure, equilibrium_ratios


def test_antoine_pressure_water_at_100C():
    A, B, C = 8.07131, 1730.63, 233.426
    T = 100.0  # °C
    psat = antoine_pressure(T, A, B, C)
    assert psat == pytest.approx(760.0, rel=1e-2)


def test_equilibrium_ratios_simple_case():
    components = [
        {"A": 8.07131, "B": 1730.63, "C": 233.426},  # water
        {"A": 8.20417, "B": 1642.89, "C": 230.300},  # ethanol
    ]
    T = 78.0
    P = 760.0
    Ks = equilibrium_ratios(T, P, components)
    assert isinstance(Ks, np.ndarray)
    assert Ks.shape == (2,)
    assert Ks[1] == pytest.approx(1.0, rel=0.1)
    assert Ks[0] < 1.0
