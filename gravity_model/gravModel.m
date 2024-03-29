%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% # Gravity Model - Main gravity model
% # -----------------------------------------------------------------------
% # This script produces the main gravity model including the plotting.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


function gravModel

load('gravitymodelresult.mat');

%For original offset 
cfrom = getfield(gravitymodelresult, 'Country_From');
cto = getfield(gravitymodelresult, 'Country_to');
flow = getfield(gravitymodelresult, 'FlowFijFji');
latfrom = getfield(gravitymodelresult, 'Latitude_from');
longfrom = getfield(gravitymodelresult, 'Longitude_from');
latto = getfield(gravitymodelresult, 'Latitude_to');
longto = getfield(gravitymodelresult, 'Longitude_to');
popFrom = getfield(gravitymodelresult, 'pop_from');
popTo = getfield(gravitymodelresult, 'pop_to');
gdpdiff = getfield(gravitymodelresult, 'GDPDiff');
gdpdiffabs = getfield(gravitymodelresult, 'GDPDiffabs');

result = cell(4559,8);
for i=1:size(gravitymodelresult,1)
    [dis, ~]= latlongReader([latfrom(i),longfrom(i)],[latto(i), longto(i)]);
    result{i,1} = string(cfrom(i)); %country from
    result{i,2} = string(cto(i)); %country to
    result{i,3} = dis; % distance
    result{i,4} = log(gravCal(dis, popFrom(i), popTo(i))); % gravity
    result{i,5} = log(flow(i)); % flow
end

x = [result{:,5}]'; %flow
y = [result{:,4}]'; %gravity
format long
scatter(x,y)
hold on
xlabel('Flow')
ylabel('gResidual')
title('')
grid on
X = [ones(length(x),1) x];
b = X\y;
yCalc2 = X*b;
plot(x,yCalc2,'--')
legend('Pairing','Slope & Intercept','Location','best');

for i=1:size(gravitymodelresult,1)
    v_off = vertical_offset(b(2), b(1), result{i,5}, result{i,4});
    result{i,6} = v_off; % offset
    result{i,7} = gdpdiff(i); % gdpdiff
    result{i,8} = gdpdiffabs(i); % gdpdiff
end

end

function v_offset = vertical_offset(slope, intercept, x, y)
    y1 = intercept + (slope * x);
    v_offset = y1 - y;
end

function gravity = gravCal(distance, populationA, populationB)
    gravity = (populationA * populationB)/(distance*distance);
end
