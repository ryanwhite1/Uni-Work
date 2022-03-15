clear all

%Following code finds time for full/sparse matrices
for method = 1:10
    if method == 1 %full gaussian elim
        pwer = 1:9;                                                     %choose how many powers to calculate to
        sizes1 = 2.^pwer;                                               %create array of numbers to iterate matrix dimensions over
        [GaussTimeA1, GaussTimeA2] = deal(zeros(size(sizes1)));         %initiate time arrays
        for n = 1:length(sizes1)
            [sA1, b1] = sparsesetup(sizes1(n), 2, 1, 2, [-1, 3, -1]);   %create matrices with dimensions n*n
            [sA2, b2] = sparsesetup(sizes1(n), 1, 0, -1, [1, 2, 1]);
            A1 = full(sA1); A2 = full(sA2);                             %convert to full matrices
            tic; gausselim(A1, b1); GaussTimeA1(n) = toc;               %time the solving computation, store time taken 
            tic; gausselim(A2, b1); GaussTimeA2(n) = toc;
        end
    elseif method == 2 %sparse gaussian elim
        pwer = 1:6;
        sizes2 = 2.^pwer;
        [sGaussTimeA1, sGaussTimeA2] = deal(zeros(size(sizes2)));
        for n = 1:length(sizes2)
            [sA1, b1] = sparsesetup(sizes2(n), 2, 1, 2, [-1, 3, -1]);
            [sA2, b2] = sparsesetup(sizes2(n), 1, 0, -1, [1, 2, 1]);
            tic; gausselim(sA1, b1); sGaussTimeA1(n) = toc;
            tic; gausselim(sA2, b1); sGaussTimeA2(n) = toc;
        end
    elseif method == 3 %full inverse func
        pwer = 1:11;
        sizes3 = 2.^pwer;
        [InvTimeA1, InvTimeA2] = deal(zeros(size(sizes3)));
        for n = 1:length(sizes3)
            [sA1, b1] = sparsesetup(sizes3(n), 2, 1, 2, [-1, 3, -1]);
            [sA2, b2] = sparsesetup(sizes3(n), 1, 0, -1, [1, 2, 1]);
            A1 = full(sA1); A2 = full(sA2);
            tic; inv(A1) * b1; InvTimeA1(n) = toc;
            tic; inv(A2) * b1; InvTimeA2(n) = toc;
        end
    elseif method == 4 %sparse inverse func
        pwer = 1:13;
        sizes4 = 2.^pwer;
        [sInvTimeA1, sInvTimeA2] = deal(zeros(size(sizes4)));
        for n = 1:length(sizes4)
            [sA1, b1] = sparsesetup(sizes4(n), 2, 1, 2, [-1, 3, -1]);
            [sA2, b2] = sparsesetup(sizes4(n), 1, 0, -1, [1, 2, 1]);
            tic; inv(sA1) * b1; sInvTimeA1(n) = toc;
            tic; inv(sA2) * b1; sInvTimeA2(n) = toc;
        end
    elseif method == 5 %full backslash
        pwer = 1:12;
        sizes5 = 2.^pwer;
        [SlashTimeA1, SlashTimeA2] = deal(zeros(size(sizes5)));
        for n = 1:length(sizes5)
            [sA1, b1] = sparsesetup(sizes5(n), 2, 1, 2, [-1, 3, -1]);
            [sA2, b2] = sparsesetup(sizes5(n), 1, 0, -1, [1, 2, 1]);
            A1 = full(sA1); A2 = full(sA2);
            tic; A1\b1; SlashTimeA1(n) = toc;
            tic; A2\b1; SlashTimeA2(n) = toc;
        end
    elseif method == 6 %sparse backslash
        pwer = 1:23;
        sizes6 = 2.^pwer;
        [sSlashTimeA1, sSlashTimeA2] = deal(zeros(size(sizes6)));
        for n = 1:length(sizes6)
            [sA1, b1] = sparsesetup(sizes6(n), 2, 1, 2, [-1, 3, -1]);
            [sA2, b2] = sparsesetup(sizes6(n), 1, 0, -1, [1, 2, 1]);
            tic; sA1\b1; sSlashTimeA1(n) = toc;
            tic; sA2\b1; sSlashTimeA2(n) = toc;
        end
   elseif method == 7 % full GMRes
        pwer = 1:12;
        sizes7 = 2.^pwer;
        [GMResTimeA1, GMResTimeA2] = deal(zeros(size(sizes7)));
        for n = 1:length(sizes7)
            [sA1, b1] = sparsesetup(sizes7(n), 2, 1, 2, [-1, 3, -1]);
            [sA2, b2] = sparsesetup(sizes7(n), 1, 0, -1, [1, 2, 1]);
            A1 = full(sA1); A2 = full(sA2);
            tic; gmres(A1, b1); GMResTimeA1(n) = toc;
            tic; gmres(A2, b2); GMResTimeA2(n) = toc;
        end
   elseif method == 8 %sparse GMRes
        pwer = 1:19;
        sizes8 = 2.^pwer;
        [sGMResTimeA1, sGMResTimeA2] = deal(zeros(size(sizes8)));
        for n = 1:length(sizes8)
            [sA1, b1] = sparsesetup(sizes8(n), 2, 1, 2, [-1, 3, -1]);
            [sA2, b2] = sparsesetup(sizes8(n), 1, 0, -1, [1, 2, 1]);
            tic; gmres(sA1, b1); sGMResTimeA1(n) = toc;
            tic; gmres(sA2, b2); sGMResTimeA2(n) = toc;
        end
   elseif method == 9 %full BiCG
        pwer = 1:12;
        sizes9 = 2.^pwer;
        [BiCGTimeA1, BiCGTimeA2] = deal(zeros(size(sizes9)));
        for n = 1:length(sizes9)
            [sA1, b1] = sparsesetup(sizes9(n), 2, 1, 2, [-1, 3, -1]);
            [sA2, b2] = sparsesetup(sizes9(n), 1, 0, -1, [1, 2, 1]);
            A1 = full(sA1); A2 = full(sA2);
            tic; bicg(A1, b1); BiCGTimeA1(n) = toc;
            tic; bicg(A2, b2); BiCGTimeA2(n) = toc;
        end
   elseif method == 10 %sparse BiCG
        pwer = 1:19;
        sizes0 = 2.^pwer;
        [sBiCGTimeA1, sBiCGTimeA2] = deal(zeros(size(sizes0)));
        for n = 1:length(sizes0)
            [sA1, b1] = sparsesetup(sizes0(n), 2, 1, 2, [-1, 3, -1]);
            [sA2, b2] = sparsesetup(sizes0(n), 1, 0, -1, [1, 2, 1]);
            tic; bicg(sA1, b1); sBiCGTimeA1(n) = toc;
            tic; bicg(sA2, b2); sBiCGTimeA2(n) = toc;
        end
    end
end

%following code produces side-by-side plot of comp time vs matrix
%dimensions
figure
subplot(1, 2, 1)        %subplot for full matrices
loglog(sizes1, GaussTimeA1);
hold on
loglog(sizes1, GaussTimeA2);
loglog(sizes3, InvTimeA1);
loglog(sizes3, InvTimeA2);
loglog(sizes5, SlashTimeA1);
loglog(sizes5, SlashTimeA2);
loglog(sizes7, GMResTimeA1);
loglog(sizes7, GMResTimeA2);
loglog(sizes9, BiCGTimeA1);
loglog(sizes9, BiCGTimeA2);
legend('Gauss Elim A1', 'Gauss Elim A2', 'Inverse A1', 'Inverse A2', 'BSlash A1', ...
    'BSlash A2', 'GMRes A1', 'GMRes A2', 'BiCG A1', 'BiCG A2', 'Location', 'southeast');
title('Computation Time vs Full Matrix Size');
ylabel('Time (s)');
xlabel('Matrix Dimension Length');

subplot(1, 2, 2)        %subplot for sparse matrices
loglog(sizes2, sGaussTimeA1);
hold on
loglog(sizes2, sGaussTimeA2);
loglog(sizes4, sInvTimeA1);
loglog(sizes4, sInvTimeA2);
loglog(sizes6, sSlashTimeA1);
loglog(sizes6, sSlashTimeA2);
loglog(sizes8, sGMResTimeA1);
loglog(sizes8, sGMResTimeA2);
loglog(sizes0, sBiCGTimeA1);
loglog(sizes0, sBiCGTimeA2);
legend('Gauss Elim A1', 'Gauss Elim A2', 'Inverse A1', 'Inverse A2', 'BSlash A1', ...
    'BSlash A2', 'GMRes A1', 'GMRes A2', 'BiCG A1', 'BiCG A2', 'Location', 'southeast');
title('Computation Time vs Sparse Matrix Size');
ylabel('Time (s)');
xlabel('Matrix Dimension Length');

function x = gausselim(A, b)
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

%following function is the textbook given program :(
function [a, b] = sparsesetup(n, b1, bn, bl, val)
% Input: n = size of system
%        b1, bn, bl = initial b value, filling b values, final b value respectively
%        val = 1x3 array of values for band
    e = ones(n, 1); n2 = n/2;
    a = spdiags([val(1)*e val(2)*e val(3)*e], -1:1, n, n); %entries of a
    a(n2 + 1, n2) = -1; a(n2, n2 + 1) = -1; %fix up to 2 entries
    b = zeros(n, 1);
    b(1) = 2; b(n) = bl; b(2:n-1) = bn; 
end