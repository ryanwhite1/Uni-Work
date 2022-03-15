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