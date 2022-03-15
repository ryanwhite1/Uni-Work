X = linspace(-4, 4, 100);
Y = linspace(-2, 2, 100);
[x, y] = meshgrid(X, Y);
h = (10 * exp(-1 * (1 / 10) * x.^2)) + ((1 / 10) * y.^2);

[dfdx, dfdy] = gradient(h);
div = divergence(X, Y, dfdx, dfdy);
surf(X, Y, div, 'EdgeColor', 'none');
colorbar;
xlabel('x');
ylabel('y');