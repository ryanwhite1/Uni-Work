yxvar = [-3.2 -2.2 -1.2 -0.2 0.8 1.8 2.8 3.8 4.8 5.8 6.8 7.8 8.8 9.8 10.8 11.8 12.8 13.8 14.8 15.8 16.8 17.8 18.8 19.8 20.8 21.8 22.8 23.8 24.8 25.8 26.8 27.8 28.8 29.8 30.8 31.8 ];
yyvar = [0 0 8 99 193 262 327 369 380 415 454 486 513 550 578 600 621 648 667 670 685 707 735 753 758 770 783 790 799 822 828 840 843 840 860 874 ];
yy_uncertain = [1 1 1 1 2 3 3 2 2 2 2 3 3 5 6 5 9 6 7 5 5 8 5 5 8 8 8 13 6 10 5 5 10 5 13 8 ];
yx_uncertain = 0.05 .* ones(length(yxvar), 1);
[ydydx, yunc_dydx] = deal(zeros(length(yxvar), 1));

for n = 1:(length(yxvar) - 1)
    ydydx(n) = (yyvar(n+1) - yyvar(n)) / (yxvar(n+1) - yxvar(n));
    yunc_dydx(n) = sqrt((1/(yxvar(n+1) - yxvar(n)) * yy_uncertain(n+1))^2 + ((1/(yxvar(n+1) - yxvar(n))) * yy_uncertain(n))^2);
end

gxvar = [-3.2 -2.2 -1.2 -0.2 0.8 1.8 2.8 3.8 4.8 5.8 6.8 7.8 8.8 9.8 10.8 11.8 12.8 13.8 14.8 15.8 16.8 17.8 18.8 19.8 20.8 21.8 22.8 23.8 24.8 25.8 26.8 27.8 28.8 29.8 30.8 31.8 ];
gyvar = [-5 -4 29 289 525 727 916 1062 1125 1220 1350 1450 1560 1660 1770 1860 1920 1990 2030 2090 2140 2190 2250 2320 2370 2420 2430 2450 2520 2520 2570 2600 2610 2660 2680 2690 ];
gy_uncertain = [1 1 1 1 3 3 2 3 5 5 7 7 20 10 10 10 10 10 10 10 20 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 ];
gx_uncertain = 0.05 .* ones(length(gxvar), 1);
[gdydx, gunc_dydx] = deal(zeros(length(gxvar), 1));

for n = 1:(length(gxvar) - 1)
    gdydx(n) = (gyvar(n+1) - gyvar(n)) / (gxvar(n+1) - gxvar(n));
    gunc_dydx(n) = sqrt((1/(gxvar(n+1) - gxvar(n)) * gy_uncertain(n+1))^2 + ((1/(gxvar(n+1) - gxvar(n))) * gy_uncertain(n))^2);
end

bxvar = [-3.2 -2.2 -1.2 -0.2 0.8 1.8 2.8 3.8 4.8 5.8 6.8 7.8 8.8 9.8 10.8 11.8 12.8 13.8 14.8 15.8 16.8 17.8 18.8 19.8 20.8 21.8 22.8 23.8 24.8 25.8 26.8 27.8 28.8 29.8 30.8 31.8 ];
byvar = [-21 -19 277 950 1680 2380 3110 3570 3880 4380 4890 5370 5710 6080 6380 6740 7040 7300 7520 7770 8000 8350 8530 8840 9000 9260 9450 9650 9900 10100 10300 10450 10600 10650 10750 11000 ];
by_uncertain = [1 1 1 3 10 20 30 50 60 60 40 60 60 60 130 100 90 80 80 40 100 100 120 100 150 80 150 150 150 150 150 150 150 150 150 150 ];
bx_uncertain = 0.05 .* ones(length(bxvar), 1);
[bdydx, bunc_dydx] = deal(zeros(length(bxvar), 1));

for n = 1:(length(bxvar) - 1)
    bdydx(n) = (byvar(n+1) - byvar(n)) / (bxvar(n+1) - bxvar(n));
    bunc_dydx(n) = sqrt(((1/(bxvar(n+1) - bxvar(n))) * by_uncertain(n+1))^2 + ((1/(bxvar(n+1) - bxvar(n))) * by_uncertain(n))^2);
end

vxvar = [-3.2 -2.2 -1.2 -0.2 0.8 1.8 2.8 3.8 4.8 5.8 6.8 7.8 8.8 9.8 10.8 11.8 12.8 13.8 14.8 15.8 16.8 17.8 18.8 19.8 20.8 21.8 22.8 23.8 24.8 25.8 26.8 27.8 28.8 29.8 30.8 31.8 ];
vyvar = [-9 -5 162 474 820 1150 1489 1730 1910 2120 2420 2620 2820 3020 3150 3330 3500 3620 3800 3920 4040 4130 4270 4400 4520 4670 4780 4870 5000 5160 5250 5230 5370 5420 5500 5580 ];
vy_uncertain = [1 1 1 3 10 10 7 10 15 20 20 20 20 20 10 40 30 20 30 20 20 30 30 60 30 50 50 50 40 70 40 40 40 50 50 70 ];
vx_uncertain = 0.05 .* ones(length(vxvar), 1);
[vdydx, vunc_dydx] = deal(zeros(length(vxvar), 1));

for n = 1:(length(vxvar) - 1)
    vdydx(n) = (vyvar(n+1) - vyvar(n)) / (vxvar(n+1) - vxvar(n));
    vunc_dydx(n) = sqrt(((1/(vxvar(n+1) - vxvar(n))) * vy_uncertain(n+1))^2 + ((1/(vxvar(n+1) - vxvar(n))) * vy_uncertain(n))^2);
end

figure
plot(yxvar, yyvar, 'Color', '[0.9290, 0.6940, 0.1250]');
hold on;
plot(gxvar, gyvar, 'Color', '[0, 0.5, 0]');
plot(bxvar, byvar, 'Color', '[0, 0.4470, 0.7410]');
plot(vxvar, vyvar, 'Color', '[0.4940, 0.1840, 0.5560]');
errorbar(yxvar, yyvar, yy_uncertain, 'Color', '[0.9290, 0.6940, 0.1250]');
errorbar(bxvar, byvar, by_uncertain, 'Color', '[0, 0.4470, 0.7410]');
errorbar(vxvar, vyvar, by_uncertain, 'Color', '[0.4940, 0.1840, 0.5560]');
errorbar(gxvar, gyvar, gy_uncertain, 'Color', '[0, 0.5, 0]');
xlabel('Voltage (V)');
ylabel('Current (x10^{-11}A)');
legend('Yellow', 'Green', 'Blue', 'Violet', 'Location', 'northwest');
%axis([-2.6 -1 -30 60]);
figure
plot(yxvar, ydydx, 'Color', '[0.9290, 0.6940, 0.1250]');
hold on
plot(gxvar, gdydx, 'Color', '[0, 0.5, 0]');
plot(bxvar, bdydx, 'Color', '[0, 0.4470, 0.7410]');
plot(vxvar, vdydx, 'Color', '[0.4940, 0.1840, 0.5560]');
errorbar(yxvar, ydydx, yunc_dydx, 'Color', '[0.9290, 0.6940, 0.1250]');
errorbar(bxvar, bdydx, bunc_dydx, 'Color', '[0, 0.4470, 0.7410]');
errorbar(gxvar, gdydx, gunc_dydx, 'Color', '[0, 0.5, 0]');
errorbar(vxvar, vdydx, vunc_dydx, 'Color', '[0.4940, 0.1840, 0.5560]');
legend('Yellow', 'Green', 'Blue', 'Violet', 'Location', 'northeast');
%axis([400 585 299 310]);
xlabel('Voltage (V)');
ylabel('Current per Volt (x10^{-11}A per V)');
%title('Camel Salivation over Time');