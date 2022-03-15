clear all;
y = [-5:0.1:5];
dist = 1;
charge = 1;
const = 1 / (pi * 8.8542e-12);
field = const * (dist * charge) ./ (dist^2 + y.^2);
plot(y, field);
xlabel("y (Multiples of 1/2 Separation Distance)")
ylabel("Electric Field Strength")