sol = gausselim(hilb(8), ones(8, 1));
cond(hilb(8))
function x = gausselim(A,b)
    %Gaussian Elimination
    %Input: matrices A and b, where A are the multiples of the unknowns,
    %and b the solutions
    %Output: Matrix x of solutions 
    %Source: Huskie, K, Jan, (1)
    [row, ~] = size(A);
    n = row;
    x = zeros(size(b));
    for k = 1:n-1   
      for i = k+1:n
         xMultiplier = A(i,k) / A(k,k);
         for j=k+1:n
            A(i,j) = A(i,j) - xMultiplier * A(k,j);
         end
         b(i, :) = b(i, :) - xMultiplier * b(k, :);
      end 
        % backsubstitution:
        x(n, :) = b(n, :) / A(n,n);
        for i = n-1:-1:1
            summation = b(i, :);
            for j = i+1:n
                summation = summation - A(i,j) * x(j, :);
            end
            x(i, :) = summation / A(i,i);
        end
    end
end