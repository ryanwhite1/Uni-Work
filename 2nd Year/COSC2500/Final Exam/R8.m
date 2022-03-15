montecarlo(3, 1000)

func = @(x, y, z) (x + 2) * sin(pi * y / 2) * sqrt(z) / 3;

function x = montecarlo(D, N)
    for k = 1:1000
        points = rand(D, N);
        count = 0;
        for n = 1:N
            if sqrt((points(1, n) + 2) * sin(pi * points(2, n) / 2) * sqrt(points(3, n)) / 3) <= 0.48
                count = count + 1;
            end
        end
        ratio = count / N;
        volume(k) = ratio;
    end
    m = mean(volume); s = std(volume); quote = 0.353678; err = m - quote;
    formatSpec = ['The function returned a mean volume of %d with a standard '...
        'deviation of %d for %d Dimensions, \n and %d points across %d iterations. ' ...
        'This gives an error of %d with a quoted volume of %d.'];
    disp(sprintf(formatSpec, m, s, D, N, k, err, quote));
end