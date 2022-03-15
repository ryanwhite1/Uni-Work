X = linspace(-4, 4, 20);
Y = linspace(-2, 2, 20);
[x, y] = meshgrid(X, Y);
h = (10 * exp(-1 * (1 / 10) * x.^2)) + ((1 / 10) * y.^2);

[dfdx, dfdy] = gradient(h);
quiver(X, Y, dfdx, dfdy);
xlabel('x');
ylabel('y');