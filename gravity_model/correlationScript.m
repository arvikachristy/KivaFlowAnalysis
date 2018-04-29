%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Gravity Model - Correlation Script
% -----------------------------------------------------------------------
% This correlation script produces Pearson and Kendall Tau correlation
% relationship between gdp and flow. 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

tic
% % For printing res to csv
fid = fopen('result_gravplot.csv','wt');
if fid>0
    for k=1:size(res.result,1)
        fprintf(fid,'%s,%s, %f, %f, %f, %f, %f, %f\n', [res.result{k,:}]);
    end
    fclose(fid);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %Open this line to use unsorted data
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% res = load('gres_flow_res.mat');
% offset = [res.result{:,6}]';
% gdpabs =[res.result{:,8}]';
% dist =[res.result{:,3}]';
% flow =[res.result{:,5}]';

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Open this to use sorted data by offset
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
load('sortedbyoffset.mat');
offset = getfield(sortedbyoffset, 'offset');
gdpabs = getfield(sortedbyoffset, 'GDPDiffabs');
dist = getfield(sortedbyoffset, 'distance');
flow = getfield(sortedbyoffset, 'flow');

%For splitting bands offset
sizer = size(gdpabs,1);
keeper = zeros(4,0);
counter = 1;

band_eliminate = 1;

for i = 1:sizer
        band_eliminate = band_eliminate + 1;
        keeper(1,counter) = offset(i);
        keeper(2,counter) = gdpabs(i);
        keeper(3,counter) = dist(i);
        keeper(4,counter) = flow(i);
        counter = counter + 1;
end

[peaVal, pvalp] = corr(keeper(1,:)',keeper(4,:)','Type','Pearson');
[kenVal, pvalk] = corr(keeper(1,:)',keeper(4,:)','Type','Kendall');

%Create regression line
x = keeper(4,:)';
y = keeper(1,:)';
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

toc