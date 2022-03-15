format long
clear all

f = @(x) (x - 7/11).^2 .* (x + 3/13) .* exp(-1 .* x.^2);
f_dash = @(x)(exp(-1.*x.^2).*(175 - 3572.*x + 4369.*x.^2 + 3278.*x.^3 - 3146.*x.^4))./1573;
f_ddash = @(x) (2.*(-1786 + 4194.*x + 8489.*x.^2 - 10661.*x.^3 - 3278.*x.^4 + 3146.*x.^5))./(1573.*exp(x.^2));

gss_est = gss(f, 1, 2, 10)
spi_est = spi(f, 1, 1.5, 2, 10)
new_est = newton(f_dash, f_ddash, 1.5, 0.005)

function y = gss(f, a, b, k)
    % Golden section search for minimum of f(x)
    % Start with unimodal f(x) and minimum in [a, b]
    % Input: function f, interval [a, b], number of steps k
    % Output: approximate minimum y
    % Source: Sauer, 3rd Edition
    gss_count = 0;
    g = (sqrt(5)-1) / 2;
    x1 = a + (1 - g) * (b - a);
    x2 = a + g * (b - a);
    f1 = f(x1); f2 = f(x2);
    for i = 1:k
        gss_count = gss_count + 1;
        if f1 > f2     %if f(x1) < f(x2), replace b with x2
            b = x2; x2 = x1; x1 = a + (1 - g) * (b - a);
            f2 = f1; f1 = f(x1);    %single function evaluation
        else    %otherwise, replace a with x1
            a = x1; x1 = x2; x2 = a + g * (b - a);
            f1 = f2; f2 = f(x2);    %single function evaluation
        end
    end
    y = (a + b) / 2;
end
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

function xc = newton(df, ddf, x0, tol)
    %Newton's Method
    %Input: function handle derivative of f df, function handle double derivative of f ddf,
    %initial value x0, and maximum error tol
    %Output: Approximate solution xc
    %Source: Sil, Rohit (1) (slightly changed from source)
    x(1) = x0;
    i = 1;
    new_count = 0;
    while abs(df(x(i))) > tol
        x(i+1) = x(i) - df(x(i)) / ddf(x(i));
        i = i + 1;
        new_count = new_count + 1;
    end
    xc = x(i);
    new_count
end
