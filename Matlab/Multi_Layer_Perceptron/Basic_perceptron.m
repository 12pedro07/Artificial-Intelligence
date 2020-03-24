clear all, clc;

net = newp([-2 2 ; -2 2 ; -2 2], 3)    % rede (ranges de entrada e n. de perceptrons)
net.IW{1,1} = [-.5 1 .5 ; .5 1 -.5 ; 1 1 1];           % pesos da rede

%view(net);

net.layers{1}.transferFcn = 'tansig'; % func. ativ.

p1 = [1;2;3]; % entradas

s = sim(net,p1) % saida