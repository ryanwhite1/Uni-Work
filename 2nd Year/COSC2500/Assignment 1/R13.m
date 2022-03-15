clear all
syms z

endpt = 10;

expMax = 28;                       %Exponent max
exponents = 1:expMax;              %vector of exponents
num_points = 2.^exponents+1;       %numPts stands for number of points

for n = 1:length(num_points)
    x = linspace(0, endpt, num_points(n));
    h(n) = x(2) - x(1);
    Y = sin(x.^2) + 1;
    
    s_area = SIMP42(Y, h(n));
    t_area = trapz(x, Y);
    exact =  10.58367089992962334;
    
    s_err(n) = abs(s_area - exact);
    t_err(n) = abs(t_area - exact);
end

figure;
loglog(h, s_err);
hold on
loglog(h, t_err);
title('sin(x^2)+1, 0 -> 10');
ylabel('Error');
xlabel('Step size h');
legend("Simpson's Rule", "Trapezoid Rule", 'Location', 'northwest');

function Area = SIMP42(Y,h)
%Input:
%  Y = f(X), where f is the function to be integration;
%   X needs to be uniformly spaced vector with an odd number of points;
%   Please give Y as a row vector, or code will probably break...
%  h is the step-size;
[~,n] = size(Y);
if n == 1
    error('Code cannot do integration at a point.  ')
elseif mod(n,2) == 0
    error('Y has an even number of points.\nPlease use an odd number of points.',1)
end

Y_mid = sum(4*Y(2:2:n-1));
Y_end = sum(2*Y(3:2:n-2));
Area = h/3*(Y_mid + Y_end + Y(1)+ Y(end));

end