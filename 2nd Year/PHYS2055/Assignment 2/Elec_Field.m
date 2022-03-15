clear all;
charge = 1;
[x, y] = deal(-1.5:0.01:1.5);
[X, Y] = meshgrid(x, y);
radius = 1;
const = 1 / (4 * pi * 8.8542e-12);
r1 = sqrt(((sqrt(3) / (2 * radius)) - X).^2 + ((1 / (2 * radius)) - Y).^2);
r2 = sqrt((-(sqrt(3) / (2 * radius)) - X).^2 + ((1 / (2 * radius)) - Y).^2);
r3 = sqrt(X.^2 + (- radius - Y).^2);
pot = (charge / const) * ((1 ./ r1) + (1 ./ r2) + (1 ./ r3));
imagesc(x, y, pot); axis xy;
view(2);
colorbar
hold on

% draw the circle of radius a
circ_bounds = 0:pi/50:2*pi;
circx = radius * cos(circ_bounds);
circy = radius * sin(circ_bounds);
plot(circx, circy);
hold on

% plot electric field vectors
x = -1.5:0.3:1.5;
y = -1.5:0.3:1.5;
[X, Y] = meshgrid(x, y);
r1 = sqrt(((sqrt(3) / (2 * radius)) - X).^2 + ((1 / (2 * radius)) - Y).^2);
r2 = sqrt((-(sqrt(3) / (2 * radius)) - X).^2 + ((1 / (2 * radius)) - Y).^2);
r3 = sqrt(X.^2 + (- radius - Y).^2);
pot = (charge / const) * ((1 ./ r1) + (1 ./ r2) + (1 ./ r3));
[elecX, elecY] = gradient(pot);
elecX = -elecX;
elecY = -elecY;
elecX(isinf(elecX)) = nan;
elecY(isinf(elecY)) = nan;
quiver(X, Y, elecX, elecY); 
hold off
