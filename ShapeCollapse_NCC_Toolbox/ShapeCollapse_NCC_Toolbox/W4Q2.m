%% Question 2
% Part a
n = [0 1 2 3 4 5];
x_a = zeros(1,length(n));
v_a = zeros(1,length(n));

x_a(1:3)=[4 1 -1];
v_a(1:4)=[1 -2 3 -4];

y_a = conv(x_a, v_a);

Fig_A = figure;
stem(x_a,'x');
hold
stem(v_a,'^');
stem(0:length(y_a)-1, y_a);
xlabel('Time');
ylabel('Value');

% Part b
x_b = ones(1,length(n));
v_b = ones(1,length(n));

y_b = conv(x_b(1:6),v_b(1:6));

Fig_B = figure;
stem(x_b(1:6),'x');
hold
stem(v_b(1:6),'^');
stem(0:length(y_b)-1,y_b);
xlabel('Time');
ylabel('Value');

%% 
%% Question 2
%%(a) x = [4 1 -1 0 ... 0], v = [1 -2 3 -4 0 ... 0].
n = [0 1 2 3 4 5];
x_a = [4 1 -1 0 0 0];
v_a = [1 -2 3 -4 0 0];

% Compute the convolution
y_a = conv(x_a,v_a);

% Visualize your results
Fig_A = figure(1);
% *insert graphing code here*
stem(n,y_a(n+1))
xlabel('n')
ylabel('y[n]')
grid on
title('x[n]*v[n]')
%%(b) x = n = discrete-time step function.
x_b = [1 1 1 1 1 1];
v_b = [1 1 1 1 1 1];

% Compute the convolution
y_b = conv(x_b,v_b);




% Visualize your results

Fig_B = figure(2);

% *insert graphing code here*

stem(n,y_b(n+1))

xlabel('n')

ylabel('y[n]')

grid on

title('x[n]*v[n]')