from pylab import *

t = arange(30,86)
L = 7.7 * 10**-3 * (85 - t) * (2*t - 59)
LDash = 7.7 * 10**-3 * (229 - 4*t)
plot(t, L, label="L", linewidth=2)
plot(t, LDash, label="L'",linewidth=2)

# Add title and labels


grid(True)
# Draw the legend
legend(loc="center")
show()
