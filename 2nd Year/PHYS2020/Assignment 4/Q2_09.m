v = 0.4:0.01:4; 
t = 0.8;
j = 0.95;
p = (8 * t) ./ (3 * v - 1) - (3 ./ v.^2); 
plot(v,p)
hold on
h = (8 * j) ./ (3 * v - 1) - (3 ./ v.^2);
plot(v, h)
axis([0.4 4 -0.5 5]);
legend('t = 0.8', 't = 0.95');
ylabel('Pressure (P/Pc)');
xlabel('Volume (V/Vc)');