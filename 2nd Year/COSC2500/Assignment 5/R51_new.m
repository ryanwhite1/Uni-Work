clear all
func1 = @(t, y) [y(2); y(1) + 2/3 * exp(t)];
func2 = @(t, y) [y(2); (2 + 4 * t^2) * y(1)];
func3 = @(t, y) [y(2); 3 * y(1) - 2 * y(2)];
conds1 = [0, (1/3) * exp(1)];
conds2 = [1, exp(1)];
conds3 = [exp(1)^3, 1];

temp = @(s) bc_mismatch(s, func3, [0, 1], conds3);

sstar = fzero(temp, [-100, 100]);

sol = ode45(func3, [0, 1], [conds3(1), sstar]);
fplot(@(x)deval(sol, x, 1), [0, 1]);
xlabel('t'); ylabel('y');

function final_error = bc_mismatch(x, f, interval, conds)
% Find the roots of this for R5.1 shooting method 
% Solve the IVP

[t, y] = ode45(f, interval, [conds(1) x]);

% Compare with final BC
final_error = y(end, 1) - conds(2);
end
