[xe, ye] = euler1([0, pi], 0, 100);
plot(xe, ye);
xlabel('x'); ylabel('y');

function [x, y] = euler1(inter, y0, n)
    x(1) = inter(1); y(1) = y0;
    h = (inter(2) - inter(1)) / n;
    for i = 1:n
        x(i + 1) = x(i) + h;
        y(i + 1) = eulerstep(x(i), y(i), h);
    end
end

function y = eulerstep(x, y, h)
    y = y + h * ydot(x, y);
end

function z = ydot(x, y)
    z = x + y;
end
