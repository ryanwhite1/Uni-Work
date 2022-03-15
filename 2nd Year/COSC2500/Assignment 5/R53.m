w = heatfd(0, 1, 0, 1, 10, 100);        %comment out for exact solution
% [X, T] = meshgrid(0:0.002:1);         %remove comment for exact solution
% U = exp(2.*T + X);
% surf(X, T, U, 'EdgeColor', 'none')
% view(60, 30);
xlabel('x'); ylabel('t'); zlabel('u');



function w = heatfd(xl, xr, yb, yt, M, N) 
%Program 8.1 Forward difference method for heat equation 
%input: space interval [xl, xr], time interval [yb, yt], 
%       number of space steps M, number of time steps N 
%output: solution w 
%Example usage: w = heatfd(0, 1, 0, 1, 10, 250) 
    f = @(x) exp(x); 
    l = @(t) exp(2 * t);
    r = @(t) exp(2 * t + 1); 
    D = 1; % diffusion coefficient 
    h = (xr - xl)/M; k = (yt - yb)/N; m = M - 1; n = N; 
    sigma = D * k/(h * h); 
    a = diag(1 - 2 * sigma * ones(m, 1)) + diag(sigma * ones(m-1, 1), 1); 
    a = a + diag(sigma * ones(m-1, 1), -1); % define matrix a 
    lside = l(yb + (0:n)*k); rside = r(yb + (0:n) * k); 
    w(:,1) = f(xl + (1:m) * h)'; % initial conditions 
    for j=1:n 
        w(:, j+1) = a * w(:, j) + sigma * [lside(j); zeros(m - 2, 1); rside(j)]; 
    end 
    w = [lside; w; rside]; % attach boundary conds 
    x = (0:m + 1) * h; t = (0:n)*k; 
    mesh(x, t, w') % 3-D plot of solution w 
    view(60, 30); axis([xl xr yb yt -1 1]) 
end