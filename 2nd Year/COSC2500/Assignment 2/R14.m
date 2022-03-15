clear all
endpt = linspace(0.1, 9000, 18000);

for n = 1:length(endpt)
    x1 = linspace(0, endpt(n), endpt(n)*9);
    x2 = linspace(0, endpt(n), 999);
    h(n) = 10^(-1);
    Y1 = exp(-x1);
    Y2 = exp(-x2);
    fun = @(x) exp(-x);
    
    s_area = trapz(x1, Y1);
    t_area = trapz(x2, Y2);
    exact =  integral(fun, 0, inf);
    
    s_err(n) = abs(s_area - exact);
    t_err(n) = abs(t_area - exact);
end

figure;
loglog(endpt, s_err);
hold on
loglog(endpt, t_err);
title('e^{-x}, 0 -> x');
ylabel('Error');
xlabel('Integration Endpoint');
legend("Fixed Step Size", "Fixed Number of Steps", 'Location', 'southwest');