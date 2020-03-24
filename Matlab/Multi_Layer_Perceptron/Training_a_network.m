clear all; clc

[x,t] = simplefit_dataset;
plot(x,t);

%% create net
net = feedforwardnet([3 3 3]);

%% setup transfer function 
net.layers{1}.transferFcn = 'tansig';
net.layers{2}.transferFcn = 'tansig';

%% change ratio: training, validation e test 
net.divideParam.trainRatio = 0.6;
net.divideParam.valRatio = 0.2;
net.divideParam.testRatio = 0.2;

%% change number of validations needed to stop
net.trainParam.max_fail = 100;

%% train net
net = train (net,x,t);

%% result
y = sim(net,x);
w = net.IW
wh = net.LW

plot(x,t,x,y);