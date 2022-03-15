function Area = SIMP42(Y,h);
%One form of Simpon's rule (the numbers don't really mean anything).
%
%Input:
%  Y = f(X), where f is the function to be integration;
%   X needs to be uniformly spaced vector with an odd number of points;
%   Please give Y as a row vector, or code will probably break...
%  h is the step-size;
%
%Output
%  Area is the approximated integral.
%
%Code written for COSC2500.
%If you use this code, please just reference it as SIMP42
%There is no need to include it in the write-up - it's on blackboard which tutors can read...
%
%

[~,n] = size(Y);
if n == 1
    error('Code cannot do integration at a point.  ')
elseif mod(n,2) == 0
    error('Y has an even number of points.\nPlease use an odd number of points.',1)
end

Y_mid = sum(4*Y(2:2:n-1));
Y_end = sum(2*Y(3:2:n-2));
Area = h/3*(Y_mid + Y_end + Y(1)+ Y(end));

end