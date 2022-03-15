time = [100, 200, 300];         %choose time points
walkers = 5000;                 %number of random walks
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
[t1dist, t2dist, t3dist] = deal(zeros(1, walkers));
for t = 1:length(time)
    for n = 1:walkers
        t1dist(n) = sqrt(t1xcoords(n)^2 + t1ycoords(n)^2);
        t2dist(n) = sqrt(t2xcoords(n)^2 + t2ycoords(n)^2);
        t3dist(n) = sqrt(t3xcoords(n)^2 + t3ycoords(n)^2);
    end
end
X = 1:2:60;


figure
subplot(1,3,1)
hist(t1dist, 1:2:50);
axis([0 60 0 900]);
title('t = 100');
ylabel('Number of Instances');
hold on
plot(X, ((2 .* X ./ time(1)) .* 2*walkers .* exp(-1 .* X.^2 ./ time(1))), 'r');
subplot(1,3,2)
hist(t2dist, 1:2:50);
axis([0 60 0 900]);
xlabel('Distance from Origin');
title('t = 200');
hold on
plot(X, ((2 .* X ./ time(2)) .* 2 .* walkers .* exp(-1 .* X.^2 ./ time(2))), 'r');
subplot(1,3,3)
hist(t3dist, 1:2:50);
axis([0 60 0 900]);
title('t = 300');
hold on
plot(X, ((2 .* X ./ time(3)) .* 2 .* walkers .* exp(-1 .* X.^2 ./ time(3))), 'r');
    

function [X, Y] = randomwalk(N)
    [X, Y] = deal(zeros(1, N+1));       %deal zero vectors to X and Y coordinates
    for n = 1:N
        dX = sign(randn) * rand(1); dY = sign(randn) * sqrt(1 - dX^2);      %find value of x, 0<= x <= 1, with random sign, and value of y with random sign that gives triangle with sides x, y and hypotenuse 1
        X(n + 1) = X(n) + dX; Y(n + 1) = Y(n) + dY;                         %assign stepped values to initial value on X and Y coords
    end
end