v = 0.4:0.01:0.8; 
t = 0.8;
j = 0.95;
g1 = (-8/3 * t .* log(3.*v -1)) + (8/3 .* (t ./ (3.*v -1))) - (6./v);
plot(v,g1)
hold on
g2 = (-8/3 * j .* log(3.*v -1)) + (8/3 .* (j ./ (3.*v -1))) - (6./v);
plot(v, g2)
axis([0.4 0.8 -inf inf]);
legend('t = 0.8', 't = 0.95');
ylabel('g');
xlabel('Pressure (P/Pc)');