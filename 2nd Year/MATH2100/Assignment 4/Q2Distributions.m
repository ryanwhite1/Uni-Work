time = [100, 200, 300];         %choose time points
walkers = 1000;                 %number of random walks
[t1xcoords, t1ycoords, t2xcoords, t2ycoords, t3xcoords, t3ycoords] = deal(zeros(1, walkers));       %initialise vectors 
for t = 1:length(time)
    for n = 1:walkers
        [x, y] = randomwalk(time(t));
        if t == 1
            t1xcoords(n) = x(time(t)+1);
            t1ycoords(n) = y(time(t)+1);
        elseif t == 2
            t2xcoords(n) = x(time(t)+1);
            t2ycoords(n) = y(time(t)+1);
        else
            t3xcoords(n) = x(time(t)+1);
            t3ycoords(n) = y(time(t)+1);
        end
    end
end

figure
subplot(1,3,1)
scatter(t1xcoords, t1ycoords, '+');
axis([-50 50 -50 50]);
title('t = 100');
hold on
subplot(1,3,2)
scatter(t2xcoords, t2ycoords, 'o');
axis([-50 50 -50 50]);
title('t = 200');
subplot(1,3,3)
scatter(t3xcoords, t3ycoords, '*');
axis([-50 50 -50 50]);
title('t = 300');
    

function [X, Y] = randomwalk(N)
    [X, Y] = deal(zeros(1, N+1));       %deal zero vectors to X and Y coordinates
    for n = 1:N
        dX = sign(randn) * rand(1); dY = sign(randn) * sqrt(1 - dX^2);      %find value of x, 0<= x <= 1, with random sign, and value of y with random sign that gives triangle with sides x, y and hypotenuse 1
        X(n + 1) = X(n) + dX; Y(n + 1) = Y(n) + dY;                         %assign stepped values to initial value on X and Y coords
    end
end