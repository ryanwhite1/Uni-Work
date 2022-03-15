n = 400;
A = zeros(n);
x = ones(n, 1);
for j = 1:n
    for i = 1:n
        A(i, j) = abs(i - j) + 1;
    end
end
Cond_no = cond(A)
b = A * x;
xc = A\b;
for_err = max(abs(x - xc))
err_mag_fac = (for_err / max(abs(x))) / eps