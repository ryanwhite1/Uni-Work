format long
x = 1;
for h = [1e-3, 1e-5, 1e-7]
    deriv = (((x + h)^5 - 4*(x + h) + 3) - ((x - h)^5 - 4*(x - h) + 3)) / (2 * h)
    err = deriv - 1
end