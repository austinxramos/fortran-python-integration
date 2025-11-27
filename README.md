# Fortran-Python Integration: ODE Solver

**Demonstrates integration of compiled Fortran scientific code into Python workflows.**

This project shows how to:
- Build Fortran code with CMake
- Wrap Fortran executables with Python
- Create clean Python APIs for compiled codes
- Run parameter sweeps and batch jobs

**Directly applicable to**: Integrating ocean circulation models (MITgcm, ROMS) into analysis pipelines.

---

## Quick Start

### Build Fortran Code
```bash
mkdir build && cd build
cmake ..
make
./ode_solver  # Test it works
cd ..
```

### Use Python Wrapper
```python
from python.ode_solver import FortranODESolver

solver = FortranODESolver()
t, y = solver.solve(t0=0, tf=10, y0=1.0, n_steps=100)

print(f"Solution at t=10: y={y[-1]:.4f}")
```

### CLI
```bash
pip install -e .

# Solve ODE
ode-solve solve --t0 0 --tf 10 --y0 1.0 --steps 100 -o results.csv

# Parameter sweep
ode-solve sweep --param y0 --values "0.5,1.0,2.0" -o ./sweep_results/
```

---

## What This Demonstrates

✅ **CMake build system** - Standard approach for scientific codes  
✅ **Subprocess wrapper** - Execute compiled code from Python  
✅ **Output parsing** - Handle structured text output (CSV)  
✅ **Parameter sweeps** - Batch execution patterns  
✅ **Error handling** - Timeouts, failed builds, missing executables  
✅ **Documentation** - Comments, docstrings, README  

**This is the pattern for integrating MITgcm, ROMS, or any compiled ocean/climate model.**

---

## Project Structure
```
fortran-python-integration/
├── src/
│   ├── rk4.f90                 # Fortran module: RK4 algorithm
│   ├── exponential_decay.f90   # Example ODE system
│   └── main.f90                # Fortran executable
├── python/
│   ├── __init__.py
│   ├── ode_solver.py           # Python wrapper
│   └── cli.py                  # Click CLI
├── tests/
│   └── test_solver.py
├── CMakeLists.txt              # Build configuration
└── setup.py                    # Python package
```

---

## The ODE Being Solved

$$\frac{dy}{dt} = -0.5y, \quad y(0) = y_0$$

Analytical solution: $y(t) = y_0 e^{-0.5t}$

The Fortran code implements 4th-order Runge-Kutta (RK4), a standard numerical method for ODEs used in climate/ocean models.

---

## Extending This

**For MITgcm-style integration:**

1. **Configuration files**: Write Python code to generate MITgcm input files (namelists, forcing data)
2. **Batch execution**: Use similar subprocess pattern to run model
3. **Output parsing**: Read NetCDF outputs with xarray instead of CSV
4. **Parameter sweeps**: Vary ocean physics parameters systematically

Example:
```python
class MITgcmWrapper:
    def __init__(self, executable="mitgcmuv"):
        self.executable = executable
    
    def run(self, config_dir, output_dir):
        subprocess.run([self.executable], cwd=config_dir, check=True)
        return self.parse_outputs(output_dir)
```

---

## Requirements

- **Fortran compiler**: gfortran (tested with 9.3+)
- **CMake**: 3.15+
- **Python**: 3.9+

Install gfortran:
```bash
# Ubuntu/Debian
sudo apt install gfortran cmake

# macOS
brew install gcc cmake
```

---

## Testing
```bash
# Build Fortran code
mkdir build && cd build
cmake ..
make
cd ..

# Run Python tests
pytest tests/ -v

# Test CLI
ode-solve solve --help
ode-solve solve -o test.csv
```

---

## Performance

| Operation | Time |
|-----------|------|
| Single solve (100 steps) | ~0.01s |
| Single solve (10000 steps) | ~0.05s |
| Parameter sweep (10 runs) | ~0.1s |

Fortran computation is fast; Python overhead is minimal with subprocess approach.

---

## Author

**Xavier Ramos**  
xramos2@illinois.edu

Built to demonstrate compiled code integration skills for computational science workflows.

---

## License

MIT License - Fortran RK4 code based on public domain algorithms
