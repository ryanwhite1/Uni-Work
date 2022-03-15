clear all
h = [0.1, 0.01, 0.001]; n = 5000;
h = h(3);
for k = 1:n
    clear y Bt
    y(1) = 0; Bt = zeros(1, 1/h); dt = 1/h;
    z = randn(dt, 1);
    for i = 2:(dt)
        dBt(1, i) = z(i) * sqrt(h);
        Bt(1, i) = sum(dBt(1:i));
        y(i) = y(i-1) +  Bt(1, i-1) * h + (9 * y(i-1)^2)^(1/3) * dBt(1, i-1);
    end
    Y(k) = y(end);
end
sol = mean(Y);
err = std(Y) / sqrt(n);

