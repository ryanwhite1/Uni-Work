# MATH3070 Practical Week 2 #

# -- Part a -- #
# Define a function that takes the current recruit size and the parameters 
# r and k and outputs the recruit biomass in the next time step

recruitment <- function(x, r, k){
  # Parameters
  # ----------
  # x - current biomass
  # r - proliferation/growth rate
  # k - carrying capacity
  # Returns
  # ------
  # x_new - biomass in the next time step
  
  x_new = r * x * (1 - x / k)
  return(x_new)
}

R_vals = seq(0, 100, 1)
R_t1 = recruitment(R_vals, 1.5, 100)

plot(R_vals, R_t1, type = "l", xlab="R_t", ylab="R_t+1")

t = seq(1, 25, 1)
x = vector(mode='numeric', length=25)
x[1] = 10
for(i in 2:25){
  x[i] = recruitment(x[i - 1], 1.5, 100)
}
plot(t, x, type='l')