
%fun = @(y, t) y + (2/3) * exp(t);
[t, y] = shoot_method([0, 1], [0, (exp(1) / 3)]);

%t = -10:0.001:10;
plot(t, y);

function [x, y] = shoot_method(dom, bv)
    shoot1 = -10;
    shoot2 = 10;
    a1 = [bv(1), shoot1];
    a2 = [bv(1), shoot2];
    
    [x, F1] = ode45(@(y, t) y + (2/3) * exp(t), dom, a1);
    [x, F2] = ode45(@(y, t) y + (2/3) * exp(t), dom, a2);
    
    F1 = F1(1, end) - bv(2);
    F2 = F2(1, end) - bv(2);
    
    F3 = F1;
    while abs(F3) > 1e-6
        shoot3 = (shoot1 + shoot2) / 2;
        a3 = [bv(1), shoot3];
        
        [x, F3] = ode45(@(y, t) y + (2/3) * exp(t), dom, a3);
        if (F1 * F3 < 0)
            shoot2 = shoot3; F2 = F3;
        elseif (F1 * F2 < 0)
            shoot1 = shoot3; F1 = F3;
        end
    end
end
