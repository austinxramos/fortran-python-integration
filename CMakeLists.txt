cmake_minimum_required(VERSION 3.15)

project(FortranODESolver LANGUAGES Fortran)

# Enable Fortran
enable_language(Fortran)

# Fortran compiler flags
set(CMAKE_Fortran_STANDARD 90)
set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} -O2 -fPIC")

# Build the library with the ODE integrator and example system
add_library(rk4_lib STATIC
    src/rk4.f90
    src/exponential_decay.f90
)

# Build the executable that uses the library
add_executable(ode_solver src/main.f90)
target_link_libraries(ode_solver PRIVATE rk4_lib)

# Install targets
install(TARGETS ode_solver DESTINATION bin)
install(TARGETS rk4_lib DESTINATION lib)

# Testing
enable_testing()
add_test(NAME run_solver COMMAND ode_solver)
