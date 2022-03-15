T = load('Temperature.txt');
BT = load('Second_Order.txt');
c = 1;
Temps = [300, 400, 500, 600, 700, 800, 900, 1000]; 
for i = 1:length(BT)
    for a = 1:length(Temps)
        if T(i) == Temps(a)
            Coef(c) = BT(i);
            c = c + 1;
        end
    end
end
n = 1;
V = [0.001:0.0001:0.002];
colour = ["b", "g", "r", "c", "m", "y", "k", "b"];
for i = 1:length(Temps)
    P = ((n * 8.314 * Temps(i)) ./ V);
    PVir = ((n * 8.314 * Temps(i)) ./ V) .* (1 + (Coef(i) ./ (1000000 .* V)));
    lineOne = strcat("-", colour(i));
    lineTwo = strcat("--", colour(i));
    plot(V, P, lineOne);
    hold on;
    plot(V, PVir, lineTwo);
    legend('Ideal Gas', 'Ideal Gas with Virial Expansion');
    axis([(1 * 10^(-3)), (2 * 10^(-3)), (1 * 10^6), (9 * 10^6)]);
    xlabel('Volume (m^3)');
    ylabel('Pressure (Pa)');
end

