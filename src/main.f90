program ode_solver
    use rk4_module
    use exponential_decay_module
    implicit none

    integer :: n_steps, n_vars, i
    real(8) :: t0, tf, y0_val
    real(8), allocatable :: y_out(:,:), t_out(:)

    ! Problem parameters
    n_vars = 1
    n_steps = 100
    t0 = 0.0d0
    tf = 10.0d0
    y0_val = 1.0d0

    ! Allocate output arrays
    allocate(y_out(n_steps+1, n_vars))
    allocate(t_out(n_steps+1))

    ! Solve ODE
    call rk4_solve(exponential_decay, t0, tf, [y0_val], n_steps, n_vars, y_out, t_out)

    ! Output results to CSV
    print *, "t,y"
    do i = 1, n_steps+1
        print '(F10.6,A,F10.6)', t_out(i), ',', y_out(i, 1)
    end do

    deallocate(y_out)
    deallocate(t_out)

end program ode_solver
