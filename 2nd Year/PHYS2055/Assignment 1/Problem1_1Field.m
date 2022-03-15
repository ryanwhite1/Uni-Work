x = linspace(-4, 4, 100);
y = linspace(-2, 2, 100);
[X, Y] = meshgrid(x, y);
h = (10 * exp(-1 * (1 / 10) * X.^2)) + ((1 / 10) * Y.^2);

surf(X, Y, h, 'EdgeColor', 'none');
colorbar;
xlabel('x');
ylabel('y');