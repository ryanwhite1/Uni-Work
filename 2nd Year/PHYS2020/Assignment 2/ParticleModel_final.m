clear all;
%following statements are initialising propeties of gas
m = 2 * 1.6735575 * 10^(-27);       %Mass of each particle, value is for H2
k = 1.38064852 * 10^(-23);          %Boltzmann's Constant
Temp = 550;                         %Temperature of gas
SD = sqrt((k * Temp) / m);          %Standard deviation of gas speed
N = 1000;                           %total number of particles
Particles = zeros(4, N);

%initialise box dimensions, time
dt = 10^(-3);                       %Time step for particle trajectories
t = 1;                              %Total time to simulate particles
Box_Size = 50;
[x_min, y_min, elapsed, hits] = deal(0);
[x_max, y_max] = deal(Box_Size);

%create impulse (J) and time arrays for graphing
[J, Time] = deal(zeros(t / dt, 1));

%following for loop determines values for particle variables
for n = 1:N
    Particles(1, n) = 50 .* rand(1);        %x_ini
    Particles(2, n) = 50 .* rand(1);        %y_ini
    Particles(3, n) = SD .* randn(1);       %vx
    Particles(4, n) = SD .* randn(1);       %vy
end

%particle simulation:
for i = 1:length(Time)
    for n = 1:N 
        %initialise properties for particle calculation
        x_ini = Particles(1, n);
        y_ini = Particles(2, n);
        vx = Particles(3, n);
        vy = Particles(4, n);
        x_new = x_ini + vx * dt;
        y_new = y_ini + vy * dt;
        %following if statements check if particle collides with wall
        if x_new > x_max
            x_new = x_max - (x_new - x_max);
            J(i) = max(J) + (2 * abs(m * vx));
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

        %assign new properties for next iteration
        Particles(1, n) = x_new;        
        Particles(2, n) = y_new;
        Particles(3, n) = vx;
        Particles(4, n) = vy;
    end
    %uncomment following lines for movie
%     plot(Particles(1,:), Particles(2,:), '.');     
%     axis([0 50 0 50]);
%     M(i) = getframe; 

    elapsed = elapsed + dt;     
    Time(i) = elapsed;
end

Force = J(end) / t;                             %average force on wall
Pressure = Force / (Box_Size^2)                 %average pressure of gas

%following calculations used to find apparent temperature
vrms = sqrt(mean(Particles(3, 1:N).^2 + Particles(4, 1:N).^2));
apparent_temp = (m / (2 * k)) * vrms^2

%plot impulse graph. comment out if opting for movie
plot(Time, J);                               %plot of impulse v time
axis([0, t, 0, inf]);
xlabel('Time (s)');
ylabel('Total Impulse (kg.m/s)');
% movie(M, 1, 1 / dt);                       %uncomment for movie
