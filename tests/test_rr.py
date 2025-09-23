import pytest
from flash.rr import solve_rr


def test_all_K_equal_one_returns_half():
    z = [0.5, 0.5]
    K = [1.0, 1.0]
    beta = solve_rr(z, K)
    assert beta == pytest.approx(0.5, rel=1e-6)


def test_simple_two_component_case():
    z = [0.5, 0.5]
    K = [2.0, 0.5]
    beta: float = solve_rr(z, K)
    assert 0.0 <= beta <= 1.0, f"beta out of range: {beta}"
    # rough expected root ~0.5
    assert beta == pytest.approx(0.5, rel=1e-2)


def test_all_K_less_than_one_returns_zero():
    z = [0.4, 0.6]
    K = [0.8, 0.9]
    beta = solve_rr(z, K)
    assert beta == pytest.approx(0.0, abs=1e-8)


def test_all_K_greater_than_one_returns_one():
    z = [0.4, 0.6]
    K = [1.5, 2.0]
    beta = solve_rr(z, K)
    assert beta == pytest.approx(1.0, abs=1e-8)
