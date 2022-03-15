func = @(x) x^3 * exp(-1 * x^2);
x = spi(func, 0, 2, 1, 10)
y = func(x)


function y = spi(f, r, s, t, k)
    % Input: inline function f, initial guesses r, s, t, steps k 
    % Output: approximate minimum x
    % Source: Sauer, 3rd Edition
    spi_count = 0;
    x(1) = r; x(2) = s; x(3) = t;
    fr = f(r); fs = f(s); ft = f(t);
    for i = 4:k + 3
        spi_count = spi_count + 1;
        x(i) = (r + s) / 2 - (fs - fr) * (t - r) * (t - s) / (2 * ((s - r) * (ft - fs) - (fs - fr) * (t - s)));
        t = s; s = r; r = x(i);
        ft = fs; fs = fr; fr = f(r);        %single function evaluation
    end
    y = x(end);
end