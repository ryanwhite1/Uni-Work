clear all;
m = 2 * 1.6735575 * 10^(-24);
k = 1.38064852 * 10^(-23);
T = 300;
SD = sqrt((k * T) / m);
vx = 1 + (SD .* randn(1, 1));
vy = 1 + (SD .* randn(1, 1));
dt = 0.1;
t = 50;
N = t / dt;
Particles = [[50 .* rand(1), 50 .* rand(1)], N];
%x_ini = 50 .* rand(1);
%y_ini = 50 .* rand(1);
[x_min, y_min, elapsed, hits] = deal(0);
[x_max, y_max] = deal(50);
J = zeros(t / dt, 1);
for i = 1:(t / dt)
    [x_ini, y_ini] = Particles(i(1));
    x_new = x_ini + vx * dt;
    y_new = y_ini + vy * dt;
    if x_new > x_max
        x_new = x_max - (x_new - x_max);
        J(i) = max(J) + (m * vx);
        hits = hits + 1;
        vx = -1 * vx;
    else
        J(i) = max(J);
    end
    if y_new > y_max
        y_new = y_max - (y_new - y_max);
        vy = -1 * vy;
    end
    if x_new < x_min
        x_new = x_min + (x_min - x_new);
        vx = -1 * vx;
    end
    if y_new < y_min
        y_new = y_min + (y_min - y_new);
        vy = -1 * vy;
    end
    elapsed = elapsed + dt;
    %plot(x_new, y_new, '.');
    %axis([0 50 0 50]);
    %M = getframe;
    %X(i) = x_new;
    %Y(i) = y_new;
    x_ini = x_new;
    y_ini = y_new;
    T(i) = elapsed;
end
plot(T, J);
axis([0, t, 0, ((hits + 1) * m * abs(vx))]);
F = J(t / dt) / t;
%animatedline(X, Y);
%movie(M, 1, 1 / dt);
