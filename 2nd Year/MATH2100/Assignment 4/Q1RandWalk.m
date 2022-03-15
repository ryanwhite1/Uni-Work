[WX1, WY1] = randomwalk(500);
[WX2, WY2] = randomwalk(500);
[WX3, WY3] = randomwalk(500);

plot(WX1, WY1);
hold on 
plot(WX2, WY2);
plot(WX3, WY3);

function [X, Y] = randomwalk(N)
    [X, Y] = deal(zeros(1, N+1));       %deal zero vectors to X and Y coordinates
    for n = 1:N
        dX = sign(randn) * rand(1); dY = sign(randn) * sqrt(1 - dX^2);      %find value of x, 0<= x <= 1, with random sign, and value of y with random sign that gives triangle with sides x, y and hypotenuse 1
        X(n + 1) = X(n) + dX; Y(n + 1) = Y(n) + dY;                         %assign stepped values to initial value on X and Y coords
    end
end