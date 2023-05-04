%this program reads in a jpeg image into matlab and plots the red channel (of
%rgb) values with a 256 point colourmap. Doing this allows you to check
%whether the camera is saturating at the current settings.

%read in the image - put your file path here
data=imread('\PHYS3051', 'jpg');


%takes the red channel only
spot=data(:,:,1);

%plot image of red channel counts
figure(1)
image(spot)
colormap(hot(256))
colorbar
grid on
xlabel('pixels')
ylabel('pixels')
title('Red intensity image of output spot.')


%user inputs row number for display - ideally this should be a cut through
%the centre of the spot (where the intensity is highest)
userow=input('Choose row number to display    ');

%this takes the row selected from the red channel data
nacut=spot(userow,:);

%makes a vector of pixel numbers
zs=size(spot);
red=1:zs(2);

%plot the row cut against pixel number
figure(2)
plot(red,nacut(1:length(red)),'.')
grid on
xlabel('x pixels')
ylabel('Red intensity (AU)')
title('Cut through single row of spot image.')
