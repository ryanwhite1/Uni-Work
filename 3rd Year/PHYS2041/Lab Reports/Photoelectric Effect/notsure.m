clear all
yxvar = [-2.5 -2.2 -2 -1.8 -1.6 -1.4 -1.2 -1 -0.95 -0.9 -0.85 -0.8 -0.75 -0.7 -0.65 -0.6 -0.55 -0.5 -0.4 -0.3 -0.2 -0.1 0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2 2.1 2.2 2.3 2.4 2.5 5 7.5 10 12.5 15 17.5 20 22.5 25 27.5 30];
yyvar = [-11.8 -11.8 -11.6 -11.7 -11.6 -11.7 -11.8 -11.4 -10.2 -9.9 -9.8 -9.7 -9 -7.5 -3.5 4.4 16.7 32.2 74 127 159 185 253 316 341 385 434 470 510 550 590 630 660 710 740 770 800 840 880 910 930 970 990 1010 1060 1070 1110 1130 2000 2440 3000 3300 3600 3800 4000 4100 4300 4400 4500];
yy_uncertain = [0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.2 0.4 1 1 1 1 1 3 5 3 5 8 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 40 50 100 100 100 100 100 100 100 100 100];
yx_uncertain = 0.05 .* ones(length(yxvar), 1);
[ydydx, yunc_dydx] = deal(zeros(length(yxvar), 1));

for n = 1:(length(yxvar) - 1)
    ydydx(n) = (yyvar(n+1) - yyvar(n)) / (yxvar(n+1) - yxvar(n));
    yunc_dydx(n) = sqrt((yy_uncertain(n+1))^2 + (yy_uncertain(n))^2);
end

bxvar = [-2.5 -2.4 -2.3 -2.2 -2.1 -2 -1.9 -1.8 -1.7 -1.6 -1.5 -1.4 -1.3 -1.2 -1.1 -1 -0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2 2.1 2.2 2.3 2.4 2.5];
byvar = [-18 -18 -18 -18 -18 -18 -18 -18 -17 -16 -14 -10 -2 7 27 61 86 128 178 236 280 298 363 405 445 498 598 635 715 745 810 873 900 980 1000 1050 1080 1160 1220 1260 1340 1390 1440 1510 1520 1580 1660 1730 1790 1860 1940];
by_uncertain = [1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 1 2 2 3 5 5 6 6 8 8 15 13 10 7 6 20 20 10 30 20 20 20 20 20 20 30 20 20 30 20 20 30 20];
bx_uncertain = 0.05 .* ones(length(bxvar), 1);
[bdydx, bunc_dydx] = deal(zeros(length(bxvar), 1));

for n = 1:(length(bxvar) - 1)
    bdydx(n) = (byvar(n+1) - byvar(n)) / (bxvar(n+1) - bxvar(n));
    bunc_dydx(n) = sqrt((by_uncertain(n+1))^2 + (by_uncertain(n))^2);
end

% plot(yxvar, yyvar, 'x', 'LineStyle', '-', 'Color', [0.9290 0.6940 0.1250]);
% hold on;
% plot(bxvar, byvar, 'x', 'LineStyle', '-', 'Color', [0 0.4470 0.7410]);
% errorbar(yxvar, yyvar, yy_uncertain, yy_uncertain, yx_uncertain, yx_uncertain, 'LineStyle', 'none');
% errorbar(bxvar, byvar, by_uncertain, by_uncertain, bx_uncertain, bx_uncertain, 'LineStyle', 'none', 'Color', [0 0.4470 0.7410]);
% legend('Yellow', 'Blue', 'Location', 'northwest');
% ylabel('Current (x10^{-11}A)');

plot(yxvar, ydydx, 'LineStyle', '-', 'Color', [0.9290 0.6940 0.1250]);
hold on
plot(bxvar, bdydx, 'LineStyle', '-', 'Color', [0 0.4470 0.7410]);
errorbar(yxvar, ydydx, yunc_dydx, 'LineStyle', 'none', 'Color', [0.9290 0.6940 0.1250]);
errorbar(bxvar, bdydx, bunc_dydx, 'LineStyle', 'none', 'LineStyle', '-', 'Color', [0 0.4470 0.7410]);
legend('Yellow', 'Blue', 'Location', 'northeast');
ylabel('Current (x10^{-11}A per V)');

xlabel('Voltage (V)');

