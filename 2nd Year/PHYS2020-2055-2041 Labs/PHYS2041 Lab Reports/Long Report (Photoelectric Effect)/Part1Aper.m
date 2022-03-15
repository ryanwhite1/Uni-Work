xvar = [436 546 577];
yvar = [-1.432, -0.808, -0.707];
unc = 0.06 .* ones(3, 1);

plot(xvar, smooth(uvyvar), 'Color', '[0 0 0]');
hold on
plot(xvar, smooth(yvar), 'Color', '[0.4940, 0.1840, 0.5560]');
errorbar(xvar, uvyvar, unc, 'Color', '[0 0 0]');
xlabel('Aperture Width (mm)');
ylabel('Stopping Voltage (V)');
axis([1 10 -2.5 0]);
legend('Ultraviolet', 'Violet', 'Blue', 'Green', 'Yellow', 'Location', 'northeast');

        

