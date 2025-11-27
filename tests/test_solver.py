"""Tests for Fortran solver wrapper."""

import math
import pytest

from python.ode_solver import FortranODESolver


def test_solver_initialization():
    """Test solver can be initialized."""
    solver = FortranODESolver()
    assert solver.executable_path.exists()


def test_solve_basic():
    """Test basic ODE solution."""
    solver = FortranODESolver()
    t_vals, y_vals = solver.solve(t0=0, tf=10, y0=1.0, n_steps=100)

    assert len(t_vals) == len(y_vals)
    assert len(t_vals) > 0
    assert t_vals[0] == pytest.approx(0.0)
    assert t_vals[-1] == pytest.approx(10.0, rel=0.05)
    assert y_vals[0] == pytest.approx(1.0)

    # Exponential decay: y should decrease
    assert y_vals[-1] < y_vals[0]


def test_exponential_decay_accuracy():
    """Test solution accuracy for exponential decay."""
    solver = FortranODESolver()
    t_vals, y_vals = solver.solve(t0=0, tf=10, y0=1.0, n_steps=1000)

    # Analytical solution: y(t) = exp(-0.5*t)
    expected_final = math.exp(-0.5 * 10.0)

    # Should be accurate to ~1%
    assert y_vals[-1] == pytest.approx(expected_final, rel=0.05)
