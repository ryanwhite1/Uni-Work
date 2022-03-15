T1 = readtable('Astar_data.csv', 'PreserveVariableNames', 1);
Adata = T1{:,:};
Lumin = Adata(:,1) .* 4*pi * (3.086*10^16 / 0.017)^2;

scatter(Adata(:,2)/24, Lumin)
hold on
plot([0.467 1.0413],[10^21.8 10^22.998], 'r', 'LineWidth', 2)
plot([1.473 2.841], [10^26.838 10^27.774], 'r', 'LineWidth', 2)
grid on
set(gca, 'yscale', 'log')
ylabel('$V$ Band Luminosity $L_V$ W', 'interpreter', 'latex');
xlabel('Period (days)', 'interpreter', 'latex');
ylim([10^21 2*10^28])
legend('Cluster A Variable', 'Trend', 'Location', 'southeast')