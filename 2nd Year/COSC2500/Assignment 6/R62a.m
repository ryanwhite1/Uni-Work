n = 10000; 
count = 0;
p = 0.7; q = 1 - p;
int = [-8, 3];
for i = 1:n
    w = 0;
    while w ~= int(2)
        if rand > p
            w = w - 1;
        else
            w = w + 1;
        end
        if w == int(1)
            break 
        end
    end
    if w == int(2)
        count = count + 1;
    end
end
ratio = count / n;
actual = ((q / p)^(abs(int(1))) - 1) / ((q / p)^(abs(int(2)) + abs(int(1))) - 1);
err = ratio - actual;

    