%define variables and basic calculations
clear all;
xvar = [22 42 62 82 102 122 142];
yvar = [2 5 7 9 11 17 22];
x_uncertain = 3;
total_yvar = sum(yvar);
ave_xvar = mean(xvar);
ave_yvar = mean(yvar);

%check if uncertainty in y is an array (uncertainty is a percentage of each value)
[c, y] = size(x_uncertain);
if (c > 1) || (y > 1)
    isarray = 1;
else 
    isarray = 0;
end 

%plot basic graph
plot(xvar, yvar, '.');
hold on;
axis([0 150 0 25]);
xlabel('Change in Pressure (mmHg)');
ylabel('Cycle Count');
%title('Camel Salivation over Time');

if isarray == 1
    errorbar(xvar, yvar, x_uncertain, 'horizontal', 'LineStyle', 'none');
else 
    error = ones(size(yvar)) * x_uncertain;
    errorbar(xvar, yvar, error, 'horizontal', 'LineStyle', 'none');
end 

%calculate trendline parameters
tot_wx = 0;
tot_wy = 0;
tot_weight = 0;
for i = 1:length(xvar)
    if isarray == 0
        weights = 1 /(x_uncertain .^2);
    else
        weights = 1 /(x_uncertain(i) .^2);
    end
    val_wx = (weights) * xvar(i);
    val_wy = (weights) * yvar(i);
    tot_weight = tot_weight + (weights);
    tot_wx = tot_wx + val_wx;
    tot_wy = tot_wy + val_wy;
end

ave_wx = tot_wx / tot_weight;
ave_wy = tot_wy / tot_weight;
weight_diff = 0;
tot_weight_xdiff_y = 0;

for i = 1:length(xvar)
    if isarray == 0
        weights = 1 /(x_uncertain .^2);
    else
        weights = 1 /(x_uncertain(i) .^2);
    end
    diff = xvar(i) - ave_wx;
    weight_diff = weight_diff + (weights * (diff .^ 2));
    weight_xdiff_y = weights * (xvar(i) - ave_wx) * yvar(i);
    tot_weight_xdiff_y = tot_weight_xdiff_y + weight_xdiff_y;
end

gradient = (1/weight_diff) * tot_weight_xdiff_y;
int = ave_wy - (gradient * ave_wx);

%calculate gradient and intercept uncertainties
tot_di = 0;
tot_weight_di = 0;
for i = 1:length(xvar)
    di = yvar(i) - (gradient * xvar(i)) - int;
    tot_di = tot_di + di;
    weight_di = weights * (di .^ 2);
    tot_weight_di = tot_weight_di + weight_di;
end 

gradient_uncertainty = sqrt((1 / weight_diff) * (tot_weight_di / (length(xvar) - 2)));
int_uncertainty = sqrt(((1 / tot_weight) + ((ave_wx .^ 2) / weight_diff))) * (tot_weight_di / (length(xvar) - 2));

%define trendline bounds, then plot trendline with comments
trendy_start = (gradient * xvar(1)) + int;
trendy_end = (gradient * xvar(length(xvar))) + int;
trendy = [trendy_start trendy_end];
trendx = [xvar(1) xvar(length(xvar))];
plot(trendx, trendy);
% text(1.1*xvar(1), (1.1 * yvar(1)), ['Intercept: ' num2str(int, 2) '±' num2str(int_uncertainty, 2) 'mL']);
% text(1.1*xvar(1), (1.05 * yvar(1)), ['Gradient: ' num2str(gradient, 2) '±' num2str(gradient_uncertainty, 2) 'mL per hour']);
text(1, 22, ['Intercept: ' num2str(int, 2) '±' num2str(int_uncertainty, 2) 'Cycles']);
text(1, 20, ['Gradient: ' num2str(gradient, 2) '±' num2str(gradient_uncertainty, 2) 'Cycles per mmHg']);

comp = [4 9 13 17 14 18 23];
labels = ["1250nm" "2500nm" "3750nm" "5000nm" "6250nm" "7500nm" "8750nm"];
for i = 1:length(comp)
    yline(comp(i), ':m', labels(i));
    labels(i)
end