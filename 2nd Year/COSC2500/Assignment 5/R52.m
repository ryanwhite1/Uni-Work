%func1pts = (1/h^2, -1 - 2/h^2, 1/h^2, 2/3 * exp(tn(n)), 1, exp(1)/3);
%func2pts = (1/h^2, -2 - 2/h^2 - 4 * tn(n)^2, 1/h^2, 0, 1, exp(1));
%func3pts = (1/h^2 + 2/h, -2/h^2 - 3 - 2/h, 1/h^2, 0, exp(3), 1);

% How many points do we want ?
N = 100;
% Pre - allocate memory for matrix and vector
A = zeros(N, N);
c = zeros(N, 1);
tn = linspace(0, 1, N); % Need to change for 2(a), since it goes to 1.5
h = tn(2) - tn(1);
% Boundary conditions
A(1, 1) = 1;
c(1) = 1; % First BC
A(N, N) = 1;
c(N) = exp(1); % End BC
% Make the matrix
for n = 2:(N-1)
A(n, n-1) = 1/h^2;
A(n, n) = -2 - 2/h^2 - 4 * tn(n)^2;
A(n, n+1) = 1/h^2;
c(n) = 0;
end
Y = A\c;
plot(tn, Y)
