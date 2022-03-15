ODEs = {@(t,y) t, @(t,y) 2*(t+1)*y, @(t,y) 1 / y^2, @(t,y) t + y};
sols = {@(t) 1./2 .* (t.^2 + 2), @(t) exp(t .* (t + 2)), @(t) (3.*t+1).^(1./3), @(t) -t + 2.* exp(t) - 1};
diff = zeros(5, 1);
for k = 0:5
    steps(k+1) = 0.1 * 2^(-k);
end
figure
for k = 0:5
    h = steps(k+1);
    [te, ye] = euler1([0, 1], 1, (1 / h));
    [trk, yrk, lastrk] = RK4(ODEs{1}, [0, 1], 1, h);
    plot(te, ye); 
    hold on
    plot(trk, yrk);
    rk4diff(k + 1) = abs(sols{1}(1) - lastrk);
    diff(k + 1) =  abs(sols{1}(1) - y(end));
end
[to, yo] = ode45(ODEs{1}, [0, 1], 1);
plot(to, yo);

plot(t == [0:1:0.1 * 2^(-5)], sols{1}(t));
legend('E h = 0.1', 'RK h = 0.1', 'E h = 0.05', 'RK h = 0.05', 'E h = 0.025', 'RK h = 0.025', 'E h = 0.0125', 'Rk h = 0.0125', 'E h = 0.00625', 'RK h = 0.00625', 'ode45', 'Exact sol', 'Location', 'northwest');
xlabel('t');
ylabel('y');

figure
loglog(steps, diff);
hold on
loglog(steps, rk4diff);
xlabel('Step Size (h)');
ylabel('Error');
legend('Euler Error', 'RK4 Error');


function [t, y] = euler1(inter, y0, n)
    t(1) = inter(1); y(1) = y0;
    h = (inter(2) - inter(1)) / n;
    for i = 1:n
        t(i + 1) = t(i) + h;
        y(i + 1) = eulerstep(t(i), y(i), h);
    end
end

function y = eulerstep(t, y, h)
    y = y + h * ydot(t, y);
end

function z = ydot(t, y)
    z = t;
end

function [t,y,last] = RK4(f,tspan,yi,dt)
%Standard RK4 algorithm.
%This code is a standard RK4 algorithm with a fixed step-size.
%It can be used to solve explicit first-order ODEs.  The local truncation error is O(dt^5).  
%"Time" is the name for the x-axis variable.  
%
%Input:
%  f is a function handle for the first-order ODE - dy/dt = f(t,y)
%    - f is assumed to be a row vector.  
%  tspan is a vector that contains ti and tf, e.g. tspan = [ti,tf]
%  ti is the initial time
%  tf is the final time
%  yi is the initial values for the ODE.  yi is assumed to be a vector.  
%  dt is the step size
%
%Output:
%  t is a vector of time values.
%  y is the approximate solution curve for the initial value problem of the ODE.
%  last is the last y values - useful if you are using the last values for
%   something
%
%
%Hint - call the function like this:
%   [T,Y] = RK4(f,tspan,yi,dt)
%
%Code written for COSC2500.
%If you use this code, please just reference it as MOD4 RK4 code.
%There is no need to include it in the write-up - it's on blackboard which tutors can read...
%
%

    ti = tspan(1);  tf = tspan(2);
    num_steps = ceil((tf-ti)/dt); 	  %ceil forces it to be an integer
    t = linspace(ti,tf,num_steps+1).';  %creates time vector, then transposes

    if size(yi,2) > 1
        yi = yi.';
    end
    %Initialising y
    y = [yi,zeros(size(yi,1),num_steps)];

    %Application of the RK4 algorithm.
    for n = 1:num_steps
        k1 = dt*f(t(n),y(:,n));
        k2 = dt*f(t(n) + 0.5*dt, y(:,n) + 0.5*k1);
        k3 = dt*f(t(n) + 0.5*dt, y(:,n) + 0.5*k2);
        k4 = dt*f(t(n) + dt, y(:,n) + k3);
        y(:,n+1) = y(:,n) + (1/6)*(k1+ 2*k2 + 2*k3 + k4);
    end
    y = y.';
    last = y(end,:);
end