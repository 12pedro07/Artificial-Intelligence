saida = out.data(:,end);
entradas = out.data(:,1:end-1);

net = feedforwardnet([10 5]);


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
net = train(net,entradas',saida');