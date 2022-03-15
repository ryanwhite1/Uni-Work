x = linspace(0, 0.2, 500);
y = linspace(0, 5*494.1, 500);
w = 0.4;
r = ((2 * 16.2 * pi^2) / (500 * 7900 * w^2))^(-1);
[X, Y] = meshgrid(x, y);
T = 60 * sin((2 / w) * pi .* X) .* exp(-1 .* (Y / r)) + 293;
surf(X, Y, T,'EdgeColor', 'none');
axis([(0), (0.2), (0), (5*494.1), (225), (360)]);