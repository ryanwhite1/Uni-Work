clear all
%import data and assign names

%SpaceX Data
X = readtable('SpaceX Data.xlsx', 'Range', 'A1:G117');
ULA = readtable('ULA Data.xlsx', 'Range', 'A1:F106');
RL = readtable('Other Data.xlsx', 'Range', 'A1:F20');

%Assign data to rockets
FHrows = ismember(X.Rocket, '"FH"'); F910rows = ismember(X.Rocket, '"F9 v1.0"'); F911rows = ismember(X.Rocket, '"F9 v1.1"');
F9FTrows = ismember(X.Rocket, '"F9 FT"'); F9B4rows = ismember(X.Rocket, '"F9 B4"'); F9B5rows = ismember(X.Rocket, '"F9 B5"');
D2rows = ismember(ULA.Rocket, 'D2'); D4rows = ismember(ULA.Rocket, 'D4'); D4Hrows = ismember(ULA.Rocket, 'D4H');
A5rows = ismember(ULA.Rocket, 'A5'); ELrows = ismember(RL.Rocket, 'Electron');

%Assign data to Orbit
F9LEOrows = ismember(X.Orbit, 'LEO'); F9GTOrows = ismember(X.Orbit, 'GTO'); F9ISSrows = ismember(X.Orbit, 'LEO (ISS)');
ULAISSrows = ismember(ULA.Orbit, 'LEO (ISS)'); ULALEOrows = ismember(ULA.Orbit, 'LEO'); ULAGTOrows = ismember(ULA.Orbit, 'GTO');
RLLEOrows = ismember(RL.Orbit, 'LEO');

%following figure assigns and plots data for LEO and ISS orbits
figure 
hold on
%following lines remove NaN values (from military launches)
rlleoprice = RL.PricePerKg(RLLEOrows);ri = ~isnan(rlleoprice); rlleodate = RL.Date(RLLEOrows);
xleoprice = X.PricePerKg(F9LEOrows); xi = ~isnan(X.PricePerKg(F9LEOrows)); xleodate = X.Date(F9LEOrows);
xissprice = X.PricePerKg(F9ISSrows); xxi = ~isnan(X.PricePerKg(F9ISSrows)); xissdate = X.Date(F9ISSrows);
uleoprice = ULA.PricePerKg(ULALEOrows); ui = ~isnan(ULA.PricePerKg(ULALEOrows)); uleodate = ULA.Date(ULALEOrows);
uissprice = ULA.PricePerKg(ULAISSrows); uii = ~isnan(ULA.PricePerKg(ULAISSrows)); uissdate = ULA.Date(ULAISSrows);
xgtoprice = X.PricePerKg(F9GTOrows); xg = ~isnan(X.PricePerKg(F9GTOrows)); xgtodate = X.Date(F9GTOrows);
ugtoprice = ULA.PricePerKg(ULAGTOrows); ug = ~isnan(ULA.PricePerKg(ULAGTOrows)); ugtodate = ULA.Date(ULAGTOrows);
ug(1) = 0; xxi(2) = 0; xi(4) = 0; ri(2) = 0; ri(9) = 0;%this is to remove huge outliers in the data

%now to plot the data
scatter(xleodate(xi), xleoprice(xi), [], [0 0.447 0.741])
plot(xleodate(xi), movmean(xleoprice(xi), [length(xleoprice(xi))-1 0]), 'Color', [0 0.44 0.714])
scatter(xissdate(xxi), xissprice(xxi), [], [0.3010 0.7450 0.9330])
plot(xissdate(xxi), movmean(xissprice(xxi), [length(xleoprice(xxi))-1 0]), 'Color', [0.3010 0.7450 0.9330])
scatter(uleodate(ui), uleoprice(ui), [], [0.8500 0.3250 0.0980])
plot(uleodate(ui), movmean(uleoprice(ui), [length(uleoprice(ui))-1 0]), 'Color', [0.8500 0.3250 0.0980])
scatter(uissdate(uii), uissprice(uii), [], [0.6350 0.0780 0.1840])
plot(uissdate(uii), movmean(uissprice(uii), [length(uissprice(uii))-1 0]), 'Color', [0.6350 0.0780 0.1840])
scatter(rlleodate(ri), rlleoprice(ri), [], [0.4660 0.6740 0.1880])
plot(rlleodate(ri), movmean(rlleoprice(ri), [length(rlleoprice(ri))-1 0]), 'Color', [0.4660 0.6740 0.1880])
title('Price for LEO Launch per Provider');
ylabel('Price Per Kg (USD/kg)');
xlabel('Date');
legend("SpaceX", '', "SpaceX ISS", '', "ULA", '', "ULA ISS", '', "Rocket Labs", '', 'Location', 'northwest')
hold off

%plot data ignoring high rocket lab values
figure
hold on
scatter(xleodate(xi), xleoprice(xi), [], [0 0.447 0.741])
plot(xleodate(xi), movmean(xleoprice(xi), [length(xleoprice(xi))-1 0]), 'Color', [0 0.44 0.714])
scatter(xissdate(xxi), xissprice(xxi), [], [0.3010 0.7450 0.9330])
plot(xissdate(xxi), movmean(xissprice(xxi), [length(xleoprice(xxi))-1 0]), 'Color', [0.3010 0.7450 0.9330])
scatter(uleodate(ui), uleoprice(ui), [], [0.8500 0.3250 0.0980])
plot(uleodate(ui), movmean(uleoprice(ui), [length(uleoprice(ui))-1 0]), 'Color', [0.8500 0.3250 0.0980])
scatter(uissdate(uii), uissprice(uii), [], [0.6350 0.0780 0.1840])
plot(uissdate(uii), movmean(uissprice(uii), [length(uissprice(uii))-1 0]), 'Color', [0.6350 0.0780 0.1840])
title('Price for LEO (ignoring RocketLab) per Provider');
ylabel('Price Per Kg (USD/kg)');
xlabel('Date');
legend("SpaceX", '', "SpaceX ISS", '', "ULA", '', "ULA ISS", '')
hold off

%plot GTO data
figure
hold on
scatter(xgtodate(xg), xgtoprice(xg), [], [0 0.447 0.741])
plot(xgtodate(xg), movmean(xgtoprice(xg), [length(xgtoprice(xg))-1 0]), 'Color', [0 0.44 0.714])
scatter(ugtodate(ug), ugtoprice(ug), [], [0.8500 0.3250 0.0980])
plot(ugtodate(ug), movmean(ugtoprice(ug), [length(ugtoprice(ug))-1 0]), 'Color', [0.8500 0.3250 0.0980])
% plot(ugtodate(ug), ugtop)
title('Price for GTO Launch per Provider');
ylabel('Price Per Kg (USD/kg)');
xlabel('Date');
legend("SpaceX", '', "ULA", '')
hold off

%plot histogram of launches per launch provider in 2010s
figure 
hold on
histogram(X.Date, 'binmethod', 'year', 'BinLimits', [datetime(2010,1,1), datetime(2020,12,31)])
histogram(ULA.Date, 'binmethod', 'year', 'BinLimits', [datetime(2010,1,1), datetime(2020,12,31)])
histogram(RL.Date, 'binmethod', 'year', 'BinLimits', [datetime(2010,1,1), datetime(2020,12,31)])
legend("SpaceX Launches", "ULA Launches", "RocketLab Launches");
xlabel('Date')
ylabel('Number of Launches')
title('Number of Launches per Year per Provider')
hold off

%plot histogram of launches per launch provider in 2010s
figure 
hold on
yyaxis left
%plot histograms of SpaceX, ULA and RocketLab respectively
histogram(X.Date, 'binmethod', 'year', 'BinLimits', [datetime(2010,1,1), datetime(2020,12,31)], 'FaceAlpha', 0.2, 'FaceColor', [0 0.44 0.714])
histogram(ULA.Date, 'binmethod', 'year', 'BinLimits', [datetime(2010,1,1), datetime(2020,12,31)], 'FaceAlpha', 0.2, 'FaceColor',[0.8500 0.3250 0.0980])
histogram(RL.Date, 'binmethod', 'year', 'BinLimits', [datetime(2010,1,1), datetime(2020,12,31)], 'FaceAlpha', 0.2, 'FaceColor',[0.4660 0.6740 0.1880])
xlabel('Date')
ylabel('Number of Launches')
title('Number of Launches and Price per Year per Provider')
yyaxis right    %change y-axis
scatter(xleodate(xi), xleoprice(xi), [], [0 0.2 0.5])   %plot spacex leo raw data
plot(xleodate(xi), movmean(xleoprice(xi), [length(xleoprice(xi))-1 0]),'-', 'Color', [0 0.2 0.5]) %plot SpaceX leo rolling average
scatter(xissdate(xxi), xissprice(xxi), [], [0 0.44 0.714]) %plot SpaceX ISS raw data
plot(xissdate(xxi), movmean(xissprice(xxi), [length(xleoprice(xxi))-1 0]), '-', 'Color', [0 0.44 0.714])
scatter(uleodate(ui), uleoprice(ui), [], [0.8500 0.3250 0.0980]) %plot ULA leo raw data
plot(uleodate(ui), movmean(uleoprice(ui), [length(uleoprice(ui))-1 0]),'-', 'Color', [0.8500 0.3250 0.0980]) %plot ULA leo rolling average
scatter(uissdate(uii), uissprice(uii), [], [0.6350 0.0780 0.1840]) %plot ULA ISS raw data
plot(uissdate(uii), movmean(uissprice(uii), [length(uissprice(uii))-1 0]),'-', 'Color', [0.6350 0.0780 0.1840])
scatter(rlleodate(ri), rlleoprice(ri), [], [0.1660 0.5 0.1880]) %plot RocketLab LEO raw data
plot(rlleodate(ri), movmean(rlleoprice(ri), [length(rlleoprice(ri))-1 0]), '-', 'Color', [0.1660 0.5 0.1880]) %plot Rocket Lab rolling average
ylabel('Price per Kg (USD/kg)')
legend("SpaceX Launches", "ULA Launches", "RocketLab Launches", "SpaceX", '', "SpaceX ISS", '', "ULA", '', "ULA ISS", '', "Rocket Labs", '', 'Location', 'northwest');
hold off

%plot pie chart of total launches per provider
figure
hold on
pie([length(X.Date), length(ULA.Date), length(RL.Date)], {'SpaceX', 'ULA', 'RocketLabs'})
title('Proportion of Total Launches in the 2010s')
set(gca, 'visible', 'off')
hold off

%plot stacked density plot of total launches per provider
figure
hold on
XT = []; UT = []; RT = [];
for i = 1:length(X.Date)
    XT(i, :) = [datenum(X.Date(i)), i, 1]; %assign date to ith row, then launch number, and 1 for spaceX
end
for i = 1:length(ULA.Date)
    UT(i, :) = [datenum(ULA.Date(i)), i, 2];%assign date to ith row, then launch number, and 2 for ULA
end
for i = 1:length(RL.Date)
    RT(i, :) = [datenum(RL.Date(i)), i, 3];%assign date to ith row, then launch number, and 3 for Rocket Lab
end
TotData = sortrows([XT; UT; RT], 1); %append all matrices together, then sort by ascending date
newData = zeros(size(TotData, 1), 4);
xtot = 0; utot = 0; rtot = 0; %variables for total launches thus far in loop, for SX, ULA, RL respectively
for i = 1:size(TotData, 1)
    if TotData(i, 3) == 1 %if spacex rocket, then
        xtot = TotData(i, 2); %number of spacex launches so far
    elseif TotData(i, 3) == 2 %if ula rocket, then
        utot = TotData(i, 2);
    else    %if rocketlab rocket, then
        rtot = TotData(i, 2);
    end
    xnorm = (xtot)/sum([xtot utot rtot]); %proportion of spacex rockets vs all rockets so far
    unorm = (utot)/sum([xtot utot rtot]);
    rnorm = (rtot)/sum([xtot utot rtot]);
    newData(i, :) = [TotData(i, 1), rnorm, xnorm, unorm]; %assign proportions of each provider to row of time i
end
area(newData(:, 1), newData(:, 2:end)) %plot time vs provider proportions
colororder([0.4660 0.6740 0.1880; 0 0.447 0.741; 0.8500 0.3250 0.0980]) 
axis([newData(1, 1) datenum('31-Dec-2020', 'dd-mmm-yyyy') 0 1]); %set axis as 1/1/2010 to 31/12/2020
legend("RocketLabs", "SpaceX", "ULA")
ylabel('Proportion of Total Launches since 2010')
title('Total Proportion of Launches since 2010 by Launch Provider')
xlabel('Date')
datetick('x', 'yyyy')
grid ON
set(gca, 'layer', 'top');
