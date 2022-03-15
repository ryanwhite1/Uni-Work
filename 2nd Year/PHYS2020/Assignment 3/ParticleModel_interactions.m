clear all;

%following statements are initialising propeties of gas
m = 2 * 14 * 1.6735575 * 10^(-27);       %Mass of each particle, value is for N2
k = 1.38064852 * 10^(-23);          %Boltzmann's Constant
Temp = 70;                         %Temperature of gas
SD = sqrt((k * Temp) / m);          %Standard deviation of gas speed
N = 100;                           %total number of particles
Dissipation = 0.01;                %percentage loss of speed each timestep
Particles = zeros(4, N);

%initialise box dimensions, time
dt = 10^(-5);                       %Time step for particle trajectories
t = 0.1;                              %Total time to simulate particles
Box_Size = 0.1;
[x_min, y_min, elapsed, hits] = deal(0);
[x_max, y_max] = deal(Box_Size);

%create impulse (J), Pressure (P), Temp (T) and time arrays for graphing
[J, P, T, Time] = deal(zeros(round(t / dt), 1));

%following for loop determines values for particle variables
for n = 1:N
    Particles(1, n) = Box_Size .* rand(1);        %x_ini
    Particles(2, n) = Box_Size .* rand(1);        %y_ini
    Particles(3, n) = SD .* randn(1);             %vx
    Particles(4, n) = SD .* randn(1);             %vy
end

%particle simulation:
for i = 1:length(Time)
    for n = 1:N 
        %initialise properties for particle calculation
        x_ini = Particles(1, n);
        y_ini = Particles(2, n);
        vxi = Particles(3, n);
        vyi = Particles(4, n);
        %following applies dissipation to velocity
        vx = (vxi / abs(vxi)) * sqrt(abs((1 - Dissipation)^2 * vxi^2 + vyi*((1 - Dissipation)^2 - 1))); 
        vy = (vyi / abs(vyi)) * sqrt(abs((1 - Dissipation)^2 * vyi^2 + vxi*((1 - Dissipation)^2 - 1)));
        %following applies interaction forces
        for j = 1:N
            if j ~= n
                dx = Particles(1, j) - Particles(1, n); %find x distance between two particles
                dy = Particles(2, j) - Particles(2, n); %find y distance between two particles
                [dvx, dvy] = force_interaction(dt, m, dx, dy);
                ax(j) = dvx;
                ay(j) = dvy;
                vx = vx + (dt * dvx);   %apply acceleration to x speed
                vy = vy + (dt * dvy);   %apply acceleration to y speed
            end
        end
        A(n) = sqrt((mean(ax))^2 + (mean(ay))^2);
        x_new = x_ini + vx * dt;
        y_new = y_ini + vy * dt;
        %following if statements check if particle collides with wall
        if x_new > x_max
            x_new = x_max - (x_new - x_max);
            J(i) = J(i) + (2 * abs(m * vx));
            hits = hits + 1;
            vx = -1 * vx;
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
        %assign new properties for next iteration
        Particles(1, n) = x_new;        
        Particles(2, n) = y_new;
        Particles(3, n) = vx;
        Particles(4, n) = vy;
    end

    %uncomment following lines for movie
%     plot(Particles(1,:), Particles(2,:), '.');     
%     axis([0 Box_Size 0 Box_Size]);
%     M(i) = getframe; 
    vrms = sqrt(mean(Particles(3, 1:N).^2 + Particles(4, 1:N).^2));
    apparent_temp = (m / (2 * k)) * vrms^2
    order = sqrt((1/N) * sum((A(n) - mean(A))^2))
    O(i) = order;
    T(i) = apparent_temp;
%     P(i) = J(i) / (Box_Size^2);

    elapsed = elapsed + dt;     
    Time(i) = elapsed;
end

Force = J(end) / t;                             %average force on wall
Pressure = Force / (Box_Size^2)                 %average pressure of gas

%following calculations used to find apparent temperature
vrms = sqrt(mean(Particles(3, 1:N).^2 + Particles(4, 1:N).^2));
apparent_temp = (m / (2 * k)) * vrms^2;

%plot temperature, pressure vs time graph
yyaxis left
plot(Time, T);                               %plot of temperature v time
axis([0, t, 0, inf]);
xlabel('Time (s)');
ylabel('Temperature (K)');
hold on
yyaxis right
plot(Time, O);
ylabel('Pressure (Pa)');

%plot impulse graph. 
% plot(Time, J);                               %plot of impulse v time
% axis([0, t, 0, inf]);
% xlabel('Time (s)');
% ylabel('Total Impulse (kg.m/s)');
% movie(M, 1, 1 / dt);                       %uncomment for movie

function [ax, ay] = force_interaction(dt, m, dx, dy)
    sig = 3.715 * 10^(-8);
    eps = 10^-2;
    ax = 24 * (1 / m) * eps * sig^6 * (1 / dx^(13)) * (2*(sig^6) - dx^6);   %acceleration in x direction
    ay = 24 * (1 / m) * eps * sig^6 * (1 / dy^(13)) * (2*(sig^6) - dy^6);   %acceleration in y direction
    if dt * abs(ax) > 1    %checks if acceleration is abnormally large, sets to 0 if so
        ax = 0;
    end
    if dt * abs(ay) > 1    %checks if acceleration is abnormally large, sets to 0 if so
        ay = 0;
    end
end