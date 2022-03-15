format long
%PART A

iA = [2, -2, -1; 
      4, 1, -2;
      -2, 1, -1];
iiA = [1, 2, -1;
       0, 3, 1;
       2, -1, 1];
iiiA = [2, 1, -4;
        1, -1, 1;
        -1, 3, -2];
ib = [-2; 1; -3];
iib = [2; 4; 2];
iiib = [-7; -2; 6];

i = gausselim(iA, ib);
ii = gausselim(iiA, iib);
iii = gausselim(iiiA, iiib);

%PART B
b1 = gausselim(hilb(2), ones(2, 1));
b2 = gausselim(hilb(5), ones(5, 1));
b3 = gausselim(hilb(10), ones(10, 1));

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