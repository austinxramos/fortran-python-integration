! Runge-Kutta 4th order ODE solver
! Solves dy/dt = f(t,y) with initial condition y(t0) = y0
!
! This is a classic numerical method - public domain algorithm
! Simplified for demonstration purposes

module rk4_module
    implicit none
    private
    public :: rk4_step, rk4_solve

contains

    ! Single RK4 step
    subroutine rk4_step(f, t, y, h, y_next, n)
        ! Arguments
        integer, intent(in) :: n
        real(8), intent(in) :: t, h
        real(8), dimension(n), intent(in) :: y
        real(8), dimension(n), intent(out) :: y_next

        interface
            function f(t, y, n) result(dydt)
                integer, intent(in) :: n
                real(8), intent(in) :: t
                real(8), dimension(n), intent(in) :: y
                real(8), dimension(n) :: dydt
            end function f
        end interface

        ! Local variables
        real(8), dimension(n) :: k1, k2, k3, k4

        ! RK4 algorithm
        k1 = f(t, y, n)
        k2 = f(t + h/2.0d0, y + h*k1/2.0d0, n)
        k3 = f(t + h/2.0d0, y + h*k2/2.0d0, n)
        k4 = f(t + h, y + h*k3, n)

        y_next = y + (h/6.0d0) * (k1 + 2.0d0*k2 + 2.0d0*k3 + k4)
    end subroutine rk4_step

    ! Solve ODE over interval [t0, tf]
    subroutine rk4_solve(f, t0, tf, y0, n_steps, n_vars, y_out, t_out)
        ! Arguments
        integer, intent(in) :: n_steps, n_vars
        real(8), intent(in) :: t0, tf
        real(8), dimension(n_vars), intent(in) :: y0
        real(8), dimension(n_steps+1, n_vars), intent(out) :: y_out
        real(8), dimension(n_steps+1), intent(out) :: t_out

        interface
            function f(t, y, n) result(dydt)
                integer, intent(in) :: n
                real(8), intent(in) :: t
                real(8), dimension(n), intent(in) :: y
                real(8), dimension(n) :: dydt
            end function f
        end interface

        ! Local variables
        integer :: i
        real(8) :: h, t
        real(8), dimension(n_vars) :: y

        h = (tf - t0) / real(n_steps, 8)
        t = t0
        y = y0

        ! Store initial condition
        t_out(1) = t
        y_out(1, :) = y

        ! Time stepping
        do i = 1, n_steps
            call rk4_step(f, t, y, h, y, n_vars)
            t = t + h
            t_out(i+1) = t
            y_out(i+1, :) = y
        end do
    end subroutine rk4_solve

end module rk4_module