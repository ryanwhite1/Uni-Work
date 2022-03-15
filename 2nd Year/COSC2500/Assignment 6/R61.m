for t = 1:10
    montecarlo(t, 1000)
end

function x = montecarlo(D, N)
    for k = 1:1000
        points = rand(D, N);
        count = 0;
        for n = 1:N
            if sqrt(sum(points(:, n).^2)) <= 1
                count = count + 1;
            end
        end
        ratio = count / N;
        volume(k) = ratio;
    end
    m = mean(volume) * 2^D; s = std(volume); 
    formatSpec = ['The function returned a mean volume of %d with a standard '...
        'deviation of %d for %d Dimensions, \n and %d points across %d iterations.'];
    disp(sprintf(formatSpec, m, s, D, N, k));
end