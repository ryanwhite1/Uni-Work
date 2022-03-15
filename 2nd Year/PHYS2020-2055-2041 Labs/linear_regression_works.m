%define variables and basic calculations
clear all;
xvar = [2*pi/(436*10^-9) 2*pi/(546*10^-9) 2*pi/(577*10^-9)];
yvar = [-1.432, -0.808, -0.707];
y_uncertain = [0.002, 0.002, 0.002];
is_log = 0;             %0 for no log, 1 for log(y), 2 for log(x), 3 for log(y) and log(x)

%check if uncertainty in y is an array (uncertainty is a percentage of each value)
[c, y] = size(y_uncertain);
is_array = 0;
if (c > 1) | (y > 1)
    is_array = 1;
end 

%checks if log plot, calculates uncertainties and changes values accordingly
if is_log == 1 | is_log == 3
    if is_array == 1
        [y_neg_unc, y_pos_unc] = deal(zeros(length(yvar)));
        for i = 1:length(yvar)
            y_pos_unc(i) = yvar(i) + y_uncertain(i); y_neg_unc(i) = yvar(i) - y_uncertain(i);
        end
        yvar = log(yvar);
        y_pos_unc = log(y_pos_unc) - yvar; y_neg_unc = yvar - log(y_neg_unc);
    else
        y_pos_unc = yvar + y_uncertain; y_neg_unc = yvar - y_uncertain;
        yvar = log(yvar);
        y_pos_unc = log(y_pos_unc) - yvar; y_neg_unc = yvar - log(y_neg_unc);
    end
    if is_log == 3
        xvar = log(xvar);
    end
elseif is_log == 2
    xvar = log(xvar);
end
total_yvar = sum(yvar);
ave_xvar = mean(xvar);
ave_yvar = mean(yvar); 

%plot basic graph
plot(xvar, yvar, 'x');
hold on;
%axis([400 585 299 310]);
xlabel('k (Cycles per Meter)');
ylabel('Cut-Off Voltage (V)');
%title('Camel Salivation over Time');

%plots errorbars for appropriate log situation
if is_log == 0 | is_log == 2
    if is_array == 1
        errorbar(xvar, yvar, y_uncertain, 'LineStyle', 'none');
    else 
        error = ones(size(yvar)) * y_uncertain;
        errorbar(xvar, yvar, error, 'LineStyle', 'none');
    end
else
    errorbar(xvar, yvar, y_neg_unc, y_pos_unc, 'LineStyle', 'none');
end

%calculate trendline parameters
tot_wx = 0; tot_wy = 0; tot_weight = 0;
for i = 1:length(xvar)
    if is_array == 0
        weights = 1 /(y_uncertain.^2);
    else
        weights = 1 /(y_uncertain(i).^2);
    end
    val_wx = (weights) * xvar(i); val_wy = (weights) * yvar(i);
    tot_weight = tot_weight + (weights);
    tot_wx = tot_wx + val_wx; tot_wy = tot_wy + val_wy;
end

ave_wx = tot_wx / tot_weight; ave_wy = tot_wy / tot_weight;
weight_diff = 0; tot_weight_xdiff_y = 0;

for i = 1:length(xvar)
    if is_array == 0
        weights = 1 /(y_uncertain.^2);
    else
        weights = 1 /(y_uncertain(i).^2);
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
trendy = [trendy_start trendy_end]; trendx = [xvar(1) xvar(length(xvar))];
plot(trendx, trendy);
%punc_trendy = trendy + gradient_uncertainty; munc_trendy = trendy - gradient_uncertainty;       %finds the upper and lower trendlines
%plot(trendx, punc_trendy, '--'); plot(trendx, munc_trendy, '--');                               %plots the trendline uncertainties
text(0.75*xvar(1), 0.8 * yvar(1), ['Intercept: ' num2str(int, 2) '±' num2str(int_uncertainty, 2) ' V']);
text(0.75*xvar(1), 0.85 * yvar(1), ['Gradient: ' num2str(gradient, 2) '±' num2str(gradient_uncertainty, 2) ' (V.m per Cycle)']);
% text(3, 5, ['Intercept: ' num2str(int, 2) '±' num2str(int_uncertainty, 2) ' (deg)']);
% text(3, 4, ['Gradient: ' num2str(gradient, 2) '±' num2str(gradient_uncertainty, 2) ' (deg/nm)']);
