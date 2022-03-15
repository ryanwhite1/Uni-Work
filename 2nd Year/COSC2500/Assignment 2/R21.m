format long
clear all

f = @(x) (x-1).^3 .* (x + 2);     %define function
f_dash = @(x) (x - 1).^2 .* (4.*x + 5);      %define derivative of function
g = @(x) (x - 1).^3 .* (x + 2) + x;     %function used for fixed point iteration

bi_root = bisect(f, 0, 3, 0.00005)
fp_root = fpi(g, 0.95, 3)
new_root = newton(f, f_dash, 1.5, 0.00005)

function xc = bisect(f, a, b, tol)
    %Bisection Method
    %Input: function handle f; a,b such that f(a)*f(b) <0
    %       and tolerance tol
    %Output: Approximate solution xc
    %Source: Sauer, 3rd Edition
    if sign(f(a))*sign(f(b)) >= 0
        error('f(a)f(b)<0 not satisfied!') % ceases execution
    end
    bi_count = 0;
    while (b - a) / 2 > tol
        c = (a + b)/2;
        fa = f(a);
        fc = f(c);
        bi_count = bi_count + 1;
        if fc == 0 %c is a solution, done
            break
        end
        if sign(fc) * sign(fa) > 0 %a and c make the new interval
            a = c; 
        else %c and b make the new interval
            b = c; 
        end
    end
    xc = (a + b) / 2; %new midpoint is best estimate
    bi_count
end
function xc = fpi(g, x0, k)
    %Fixed-Point Iteration
    % Input: function handle g, starting guess x0, number of iteration steps k 
    % Output: Approximate solution xc
    %Source: Sauer, 3rd Edition
    x(1) = x0;
    for i = 1:k
        x(i + 1) = g(x(i));
    end
    xc = x(k + 1);
end
function xc = newton(f, f_dash, x0, tol)
    %Newton's Method
    %Input: function handle f, function handle derivative of f f_dash,
    %initial value x0, and maximum error tol
    %Output: Approximate solution xc
    %Source: Sil, Rohit (1)
    x(1) = x0;
    i = 1;
    new_count = 0;
    while abs(f(x(i))) > tol
        x(i+1) = x(i) - f(x(i)) / f_dash(x(i));
        i = i + 1;
        new_count = new_count + 1;
    end
    xc = x(i);
    new_count
end