#!/usr/bin/env python3
"""Command-line interface for Fortran ODE solver."""

import logging
from pathlib import Path

import click

from .ode_solver import FortranODESolver, parameter_sweep

logging.basicConfig(level=logging.INFO)


@click.group()
def cli():
    """Fortran ODE Solver - Python CLI."""
    pass


@cli.command()
@click.option("--t0", default=0.0, help="Initial time")
@click.option("--tf", default=10.0, help="Final time")
@click.option("--y0", default=1.0, help="Initial condition")
@click.option("--steps", default=100, help="Number of steps")
@click.option("--output", "-o", type=click.Path(), help="Save to CSV")
def solve(t0, tf, y0, steps, output):
    """Solve ODE dy/dt = -0.5*y using the Fortran backend."""
    solver = FortranODESolver()

    if output:
        solver.solve_to_file(Path(output), t0=t0, tf=tf, y0=y0, n_steps=steps)
        click.echo(f"Results saved to {output}")
    else:
        t_vals, y_vals = solver.solve(t0=t0, tf=tf, y0=y0, n_steps=steps)
        click.echo("t,y")
        for t, y in zip(t_vals, y_vals):
            click.echo(f"{t:.6f},{y:.6f}")


@cli.command()
@click.option("--param", type=click.Choice(["y0", "tf"]), required=True)
@click.option("--values", required=True, help="Comma-separated values, e.g. '0.5,1.0,2.0'")
@click.option("--output-dir", "-o", type=click.Path(), required=True)
def sweep(param, values, output_dir):
    """Run parameter sweep over a chosen parameter."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    param_vals = [float(v.strip()) for v in values.split(",")]

    solver = FortranODESolver()
    results = parameter_sweep(param, param_vals, solver)

    for val, _, _ in results:
        file_path = output_path / f"{param}_{val:.3f}.csv"
        solver.solve_to_file(file_path, **{param: val})

    click.echo(f"Saved {len(results)} results to {output_dir}")


if __name__ == "__main__":
    cli()
