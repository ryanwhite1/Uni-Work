v = 0.1:0.01:1; 
t = 0.95;
p = 8*t ./(3*v-1) - 3./v.^2 ; 
plot(v,p)