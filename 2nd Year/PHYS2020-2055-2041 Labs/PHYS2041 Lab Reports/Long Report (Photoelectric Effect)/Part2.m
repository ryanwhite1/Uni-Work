yxvar = [-3.2 -3.1 -3 -2.9 -2.8 -2.7 -2.6 -2.5 -2.4 -2.3 -2.2 -2.1 -2 -1.9 -1.8 -1.7 -1.6 -1.5 -1.4 -1.3 -1.2 -1.1 -1 -0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2 2.1 2.2 2.3 2.4 2.5 2.6 2.7 2.8 2.9 3 3.1 3.2 3.3 3.4 3.5 3.6 3.7 3.8 3.9 4];
yyvar = [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 5 12 21 32 43 53 64 71 81 94 104 112 122 132 133 153 161 168 176 186 190 199 207 214 220 226 233 241 242 253 263 267 273 278 285 288 299 302 306 314 320 326 327 335 343 346 349 351 360 362 366 368 373];
yy_uncertain = [1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 1 2 2 2 3 2 2 1 1 3 2 1 1 2 1 2 3 1 2 3 2 2 1 3 2 1 2 3 4 3 5 5 4 1 3 3 3 4 5 5];
yx_uncertain = 0.05 .* ones(length(yxvar), 1);
[ydydx, yunc_dydx] = deal(zeros(length(yxvar), 1));

for n = 1:(length(yxvar) - 1)
    ydydx(n) = (yyvar(n+1) - yyvar(n)) / (yxvar(n+1) - yxvar(n));
    yunc_dydx(n) = sqrt((10 * yy_uncertain(n+1))^2 + (10 * yy_uncertain(n))^2);
end

gxvar = [-3.2 -3.1 -3 -2.9 -2.8 -2.7 -2.6 -2.5 -2.4 -2.3 -2.2 -2.1 -2 -1.9 -1.8 -1.7 -1.6 -1.5 -1.4 -1.3 -1.2 -1.1 -1 -0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2 2.2 2.4 2.6 2.8 3];
gyvar = [-5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -4 -2 7 32 55 80 108 123 151 185 218 231 255 276 310 340 368 397 418 450 464 492 522 536 557 576 598 626 635 662 690 712 730 750 760 784  830  867  920  940  960];
gy_uncertain = [1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 4 3 5 4 3 4 3 4 4 4 7 6 7 10 5 5 5 6 10 6 5 10 12];
gx_uncertain = 0.05 .* ones(length(gxvar), 1);
[gdydx, gunc_dydx] = deal(zeros(length(gxvar), 1));

for n = 1:(length(gxvar) - 1)
    gdydx(n) = (gyvar(n+1) - gyvar(n)) / (gxvar(n+1) - gxvar(n));
    gunc_dydx(n) = sqrt((10 * gy_uncertain(n+1))^2 + (10 * gy_uncertain(n))^2);
end

bxvar = [-3.2 -3.1 -3 -2.9 -2.8 -2.7 -2.6 -2.5 -2.4 -2.3 -2.2 -2.1 -2 -1.9 -1.8 -1.7 -1.6 -1.5 -1.4 -1.3 -1.2 -1.1 -1 -0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2 2.2 2.4 2.6 2.8 3];
byvar = [-22 -21 -21 -21 -21 -21 -21 -21 -20 -20 -19 -18 -14 -4 11 47 79 123 165 230 264 320 382 448 497 568 633 685 750 825 883 935 1045 1150 1220 1310 1370 1420 1460 1570 1630 1700 1740 1840 1930 1980 2010 2080 2150 2250 2300 2390 2480  2600  2730  2900  2980  3140];
by_uncertain = [1 1 1 1 1 1 1 1 1 1 1 1 1 3 1 1 1 1 2 1 1 4 3 6 5 6 6 10 10 8 10 15 15 20 20 10 10 10 10 20 20 20 10 30 30 20 30 20 30 20 30 30 30  30  30  30  30  30 ];
bx_uncertain = 0.05 .* ones(length(bxvar), 1);
[bdydx, bunc_dydx] = deal(zeros(length(bxvar), 1));

for n = 1:(length(bxvar) - 1)
    bdydx(n) = (byvar(n+1) - byvar(n)) / (bxvar(n+1) - bxvar(n));
    bunc_dydx(n) = sqrt((10 * by_uncertain(n+1))^2 + (10 * by_uncertain(n))^2);
end

vxvar = [-3.2 -3.1 -3 -2.9 -2.8 -2.7 -2.6 -2.5 -2.4 -2.3 -2.2 -2.1 -2 -1.9 -1.8 -1.7 -1.6 -1.5 -1.4 -1.3 -1.2 -1.1 -1 -0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2 2.2 2.4 2.6 2.8 3];
vyvar = [-9 -9 -8 -8 -8 -8 -8 -7 -7 -6 -4 1 8 15 24 42 59 80 99 133 167 188 206 236 265 292 326 378 390 440 453 502 534 566 615 648 677 704 725 757 796 838 872 905 920 960 990 1015 1055 1085 1115 1174 1215  1255  1340  1400  1450  1520];
vy_uncertain = [1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 3 2 2 2 4 2 5 3 3 3 5 6 10 5 4 4 5 6 4 4 8 5 5 4 5 6 5 5 5 6 6  12  10  20  10  10 ];
vx_uncertain = 0.05 .* ones(length(vxvar), 1);
[vdydx, vunc_dydx] = deal(zeros(length(vxvar), 1));

for n = 1:(length(vxvar) - 1)
    vdydx(n) = (vyvar(n+1) - vyvar(n)) / (vxvar(n+1) - vxvar(n));
    vunc_dydx(n) = sqrt((10 * vy_uncertain(n+1))^2 + (10 * vy_uncertain(n))^2);
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
legend('Yellow', 'Green', 'Blue', 'Violet', 'Location', 'northwest');
%axis([400 585 299 310]);
xlabel('Voltage (V)');
ylabel('Current per Volt (x10^{-11}A per V)');
%title('Camel Salivation over Time');