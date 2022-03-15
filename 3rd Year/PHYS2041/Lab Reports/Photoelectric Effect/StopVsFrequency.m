xvar = [20 40 60 80 100];
yvar = [-1.311 -1.377 -1.388 -1.399 -1.405];
unc = [0.002 0.002 0.002 0.002 0.002];

plot(xvar, yvar, 'Color', '[0.4940, 0.1840, 0.5560]');
errorbar(xvar, yvar, unc, 'Color', '[0 0 0]');
xlabel('Light Intensity (%)');
ylabel('Stopping Voltage (V)');

        

