from pylab import *

plot([1,2,3,3],[1,1,1.4,0.6], 'o', ms=45, markerfacecolor="None", markeredgecolor='red', markeredgewidth=1)
text(0.94,0.97,"S")
text(1.94,0.97,"I")
text(2.94,1.37,"R")
text(2.94,0.57,"P")

arrow(1.28, 1.0, 0.33, 0, head_width=0.1, head_length=0.1, fc='k', ec='k')
arrow(2.28, 1.0, 0.35, 0.3, head_width=0.1, head_length=0.1, fc='k', ec='k')
arrow(2.28, 1.0, 0.35, -0.3, head_width=0.1, head_length=0.1, fc='k', ec='k')

arrow(1.28, 1.0, 0.72, 0.45, head_width=0, head_length=0, fc='k', ec='k')
arrow(2, 1.45, 0.6, 0, head_width=0.1, head_length=0.1, fc='k', ec='k')

text(0.9,1.86,"Life cycle diagram for polio epidemic")


plot([0,4],[0,2],linewidth=0)
axis('off')
show()
