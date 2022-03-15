x = 2;
num_points = 1000;

h = logspace(0, -10, num_points);

for n = 1:num_points
    forw = (f12(x+h(n))-f12(x)) / h(n);
    back = (f12(x)-f12(x-h(n))) / h(n);
    cent = (f12(x+h(n))-f12(x-h(n))) / (2*h(n));
    exac = 4*x^3 - 6*x^2;
    
    forw_err(n) = abs(forw - exac);
    back_err(n) = abs(back - exac);
    cent_err(n) = abs(cent - exac);
end

figure;
loglog(h, forw_err);
hold on
loglog(h, back_err);
loglog(h, cent_err);
title(['x = ' num2str(x)]);
ylabel('Error');
xlabel('Step size h');
legend("Forward", "Backward", "Central");

function y = f12(x)
err = 0.1 * randn(size(x));
y = x.^4 - 2*x.^3 + err;
return
end
