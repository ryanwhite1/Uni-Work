clear all
x = rn(3)

function x1 = rn(seed)
    y(1) = seed;
    for i = 2:3
        y(i) = rem(31, 3 * y(i - 1));
        u(i) = y(i) / 13;
    end
    x1 = sqrt(-2 * log(1 - u(2))) * cos(2 * pi * u(3));
end