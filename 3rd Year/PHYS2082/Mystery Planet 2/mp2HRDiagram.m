clear all

T1 = readtable('Bstar_data-Bstar_data.csv', 'PreserveVariableNames', 1);
T2 = readtable('Cstar_data-Cstar_data.csv', 'PreserveVariableNames', 1);
Bdata = T1{:,:}; Cdata = T2{:,:};

for i=1:200
    BP(i) = Bdata(i, 4);
    CP(i) = Cdata(i, 4);
    if BP(i)
        VBFluxB(i) = Bdata(i, 1);
        VBFluxV(i) = Bdata(i, 2);
        VBFluxR(i) = Bdata(i, 3);
        VBBV(i) = 5/2 * log10(VBFluxV(i) / VBFluxB(i));
        VBP(i) = BP(i); %period
        BD(i) = Bdata(i, 9); % distance
        VBAbsMag(i) = -26.72 - 2.5* log10(((VBFluxV(i))/(185)) * (24.013)^2)+1;
    else
        BFluxB(i) = Bdata(i, 1);
        BFluxV(i) = Bdata(i, 2);
        BFluxR(i) = Bdata(i, 3);
        BBV(i) = 5/2 * log10(BFluxV(i) / BFluxB(i));
        BAbsMag(i) = -26.72 - 2.5* log10(((BFluxV(i))/(185)) * (24.013)^2)+1;
    end
    if CP(i)
        VCFluxB(i) = Cdata(i, 1);
        VCFluxV(i) = Cdata(i, 2);
        VCFluxR(i) = Cdata(i, 3);
        VCBV(i) = 5/2 * log10(VCFluxV(i) / VCFluxB(i));
        VCP(i) = CP(i); %period
        CD(i) = Cdata(i, 9); % distance
        VCAbsMag(i) = -26.72 - 2.5* log10((VCFluxV(i))/(185) * (150.51)^2)+1;
    else
        CFluxB(i) = Cdata(i, 1);
        CFluxV(i) = Cdata(i, 2);
        CFluxR(i) = Cdata(i, 3);
        CBV(i) = 5/2 * log10(CFluxV(i) / CFluxB(i));
        CAbsMag(i) = -26.72 - 2.5* log10((CFluxV(i))/(185) * (150.51)^2)+1;
    end
end
countC = 0;
countB = 0;
for i=1:length(CD)
    if CD(i) > 0
        countC = countC+1;
    end
end
for i=1:length(BD)
    if BD(i) > 0
        countB = countB + 1;
    end
end
aveBdist = sum(BD) / countB;
aveCdist = sum(CD) / countC;

normBFluxV = BFluxV * 4 * pi * (aveBdist * 3.086 * 10^16)^2;
normCFluxV = CFluxV * 4 * pi * (aveCdist * 3.086 * 10^16)^2;
normVBFluxV = VBFluxV * 4 * pi * (aveBdist * 3.086 * 10^16)^2;
normVCFluxV = VCFluxV * 4 * pi * (aveCdist * 3.086 * 10^16)^2;

% scatter(VBBV, normVBFluxV, [], [0.9290, 0.6940, 0.1250], '*')
% hold on 
% scatter(VCBV, normVCFluxV, [], [0.3010, 0.7450, 0.9330], '*')
% scatter(BBV, normBFluxV, [], [0.8500, 0.3250, 0.0980])
% scatter(CBV, normCFluxV, [], [0, 0.4470, 0.7410])
% set(gca, 'yscale', 'log')


scatter(VBBV, VBAbsMag, [], [0.9290, 0.6940, 0.1250], '*')
hold on 
scatter(VCBV, VCAbsMag, [], [0.3010, 0.7450, 0.9330], '*')
scatter(BBV, BAbsMag, [], [0.8500, 0.3250, 0.0980])
scatter(CBV, CAbsMag, [], [0, 0.4470, 0.7410])
set(gca, 'YDir', 'reverse')

grid on
grid minor
xlim([-1, 2.5]);
ylabel('Absolute Magnitude $M_V$', 'interpreter', 'latex');
xlabel('B $-$ V', 'interpreter', 'latex');
legend('Variable Cluster B', 'Variable Cluster C', 'Cluster B', 'Cluster C', 'Location', 'southwest');



