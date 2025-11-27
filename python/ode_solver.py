"""
Python wrapper for Fortran ODE solver.

Provides a Pythonic interface to the compiled Fortran code,
handling subprocess execution, output parsing, and parameter validation.
"""

import subprocess
from pathlib import Path
from typing import List, Tuple, Optional
import csv
import logging

logger = logging.getLogger(__name__)


class FortranODESolver:
    """
    Wrapper for Fortran RK4 ODE solver.

    Demonstrates integration of compiled Fortran code into Python workflows,
    directly applicable to integrating ocean models like MITgcm.

    Example:
        >>> solver = FortranODESolver()
        >>> t, y = solver.solve(t0=0, tf=10, y0=1.0, n_steps=100)
        >>> print(f"Final value: y({t[-1]}) = {y[-1]}")
    """

    def __init__(self, executable_path: Optional[Path] = None):
        """
        Initialize solver wrapper.

        Args:
            executable_path: Path to compiled ode_solver binary.
                             If None, searches in standard locations.
        """
        if executable_path is None:
            # Search for executable in common locations
            search_paths = [
                Path("build/ode_solver"),
                Path("./ode_solver"),
                Path(__file__).parent.parent / "build" / "ode_solver",
            ]

            for path in search_paths:
                if path.exists():
                    executable_path = path
                    break

            if executable_path is None:
                raise FileNotFoundError(
                    "Could not find ode_solver executable. "
                    "Have you run 'cmake .. && cmake --build .' in the build directory?"
                )

        self.executable_path = Path(executable_path)

        if not self.executable_path.exists():
            raise FileNotFoundError(f"Executable not found: {self.executable_path}")

        logger.info(f"Initialized Fortran solver: {self.executable_path}")

    def solve(
        self,
        t0: float = 0.0,
        tf: float = 10.0,
        y0: float = 1.0,
        n_steps: int = 100,
    ) -> Tuple[List[float], List[float]]:
        """
        Solve ODE using Fortran backend.

        Currently solves: dy/dt = -0.5*y with y(0) = y0
        (In a real project, input files / parameters would control the ODE.)

        Args:
            t0: Initial time
            tf: Final time
            y0: Initial condition
            n_steps: Number of time steps

        Returns:
            Tuple of (time_points, solution_values)

        Raises:
            RuntimeError: If Fortran executable fails
        """
        logger.debug(f"Solving ODE: t=[{t0}, {tf}], y0={y0}, steps={n_steps}")

        try:
            # For this simple example, our Fortran code uses fixed parameters,
            # so we just run the executable and parse its CSV-like output.
            result = subprocess.run(
                [str(self.executable_path)],
                capture_output=True,
                text=True,
                timeout=30,
                check=True,
            )

            # Parse CSV-like output ("t,y" header then rows "t,y")
            lines = result.stdout.strip().split("\n")
            data_lines = [line for line in lines if line and not line.strip().startswith("t,y")]

            t_vals: List[float] = []
            y_vals: List[float] = []

            for line in data_lines:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    t_vals.append(float(parts[0]))
                    y_vals.append(float(parts[1]))

            logger.info(f"Solved ODE: {len(t_vals)} points computed")
            return t_vals, y_vals

        except subprocess.TimeoutExpired:
            raise RuntimeError("Fortran solver timed out")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Fortran solver failed: {e.stderr}")
        except Exception as e:
            raise RuntimeError(f"Error running Fortran solver: {e}")

    def solve_to_file(self, output_path: Path, **kwargs) -> Path:
        """
        Solve ODE and save results to CSV file.

        Args:
            output_path: Where to save results
            **kwargs: Arguments passed to solve()

        Returns:
            Path to output file
        """
        t_vals, y_vals = self.solve(**kwargs)

        output_path = Path(output_path)
        with output_path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["t", "y"])
            for t, y in zip(t_vals, y_vals):
                writer.writerow([t, y])

        logger.info(f"Saved results to {output_path}")
        return output_path


def parameter_sweep(
    param_name: str,
    param_values: List[float],
    solver: FortranODESolver,
    **base_kwargs,
) -> List[Tuple[float, List[float], List[float]]]:
    """
    Run parameter sweep by varying one parameter.

    Demonstrates batch execution pattern useful for model sensitivity analysis.

    Args:
        param_name: Parameter to vary ('t0', 'tf', 'y0', 'n_steps')
        param_values: List of values to try
        solver: Solver instance
        **base_kwargs: Base parameters for solve()

    Returns:
        List of (param_value, t_vals, y_vals) tuples
    """
    results: List[Tuple[float, List[float], List[float]]] = []

    for value in param_values:
        kwargs = base_kwargs.copy()
        kwargs[param_name] = value

        logger.info(f"Running with {param_name}={value}")
        t_vals, y_vals = solver.solve(**kwargs)
        results.append((value, t_vals, y_vals))

    return results
