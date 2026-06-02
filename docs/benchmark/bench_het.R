# e156 engine benchmark — Dataset B (heterogeneous, I^2~90%): REML/PM/DL tau^2
# Requires: install.packages("metafor")
suppressMessages(library(metafor))
hr<-c(0.55,0.72,0.88,1.05,0.63); lci<-c(0.45,0.62,0.77,0.92,0.51); uci<-c(0.67,0.84,1.00,1.20,0.78)
yi<-log(hr); sei<-(log(uci)-log(lci))/(2*qnorm(0.975))
f<-function(x,d=2) formatC(x,digits=d,format="f")
for(m in c("REML","PM","DL")){ r<-rma(yi=yi,sei=sei,method=m,test="z")
  cat(sprintf("%-5s HR %s (%s-%s)  tau2=%s  I2=%s%%\n",
      m,f(exp(r$beta)),f(exp(r$ci.lb)),f(exp(r$ci.ub)),f(r$tau2,4),f(r$I2,1))) }
