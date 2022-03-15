%define variables and basic calculations
clear all;
xvar = [1.25 2.5 3.75 5 6.25 7.5 8.75 10 11.25 12.5 13.75 15];
yvar = [4 9 13 17 14 18 23 27 32 45 41 46];
y_uncertain = 0.05;
total_yvar = sum(yvar);
ave_xvar = mean(xvar);
ave_yvar = mean(yvar);

%check if uncertainty in y is an array (uncertainty is a percentage of each value)
[c, y] = size(y_uncertain);
if (c > 1) || (y > 1)
    isarray = 1;
else 
    isarray = 0;
end 

%plot basic graph
plot(xvar, yvar, 'x');
hold on;
axis([0 16.25 0 47]);
xlabel('Ethanol Mass Fraction');
ylabel('Change in Volume (mL)');
%title('Camel Salivation over Time');

if isarray == 1
    errorbar(xvar, yvar, y_uncertain, 'LineStyle', 'none');
else 
    error = ones(size(yvar)) * y_uncertain;
    errorbar(xvar, yvar, error, 'LineStyle', 'none');
end 

%calculate trendline parameters
tot_wx = 0;
tot_wy = 0;
tot_weight = 0;
for i = 1:length(xvar)
    if isarray == 0
        weights = 1 /(y_uncertain .^2);
    else
        weights = 1 /(y_uncertain(i) .^2);
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
        weights = 1 /(y_uncertain .^2);
    else
        weights = 1 /(y_uncertain(i) .^2);
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
text(0.1, 9.5, ['Intercept: ' num2str(int, 2) '±' num2str(int_uncertainty, 2) 'mL']);
text(0.1, 9, ['Gradient: ' num2str(gradient, 2) '±' num2str(gradient_uncertainty, 2) 'mL per proportion']);
