! Example: Exponential decay dy/dt = -k*y
module exponential_decay_module
    implicit none
    real(8), parameter :: decay_rate = 0.5d0

contains

    function exponential_decay(t, y, n) result(dydt)
        integer, intent(in) :: n
        real(8), intent(in) :: t
        real(8), dimension(n), intent(in) :: y
        real(8), dimension(n) :: dydt

        dydt(1) = -decay_rate * y(1)
    end function exponential_decay

end module exponential_decay_module