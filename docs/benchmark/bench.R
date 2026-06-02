# e156 engine benchmark — Dataset A (homogeneous, tau^2=0): z, knha, floored-knha
# Requires: install.packages("metafor")   (tested with metafor 5.0.1, R 4.6.0)
suppressMessages(library(metafor))
hr<-c(0.74,0.75,0.79,0.82,0.67); lci<-c(0.65,0.65,0.69,0.73,0.52); uci<-c(0.85,0.86,0.90,0.92,0.85)
yi<-log(hr); sei<-(log(uci)-log(lci))/(2*qnorm(0.975)); k<-length(yi)
fmt<-function(x) formatC(x,digits=5,format="f")
ln<-function(lab,e,lo,hi) cat(sprintf("%-26s HR %s (%s - %s)\n",lab,fmt(exp(e)),fmt(exp(lo)),fmt(exp(hi))))
rz <- rma(yi=yi,sei=sei,method="PM",test="z")     # no Hartung-Knapp -> Wald/z
rk <- rma(yi=yi,sei=sei,method="PM",test="knha")  # Hartung-Knapp (no floor)
ln("metafor PM test=z",   rz$beta, rz$ci.lb, rz$ci.ub)
ln("metafor PM knha",     rk$beta, rk$ci.lb, rk$ci.ub)
# floored Hartung-Knapp (the e156 convention): mult = sqrt(max(1, Q/(k-1)))
w<-1/sei^2; muFE<-sum(w*yi)/sum(w); seFE<-sqrt(1/sum(w)); Q<-sum(w*(yi-muFE)^2)
mult<-sqrt(max(1, Q/(k-1))); hw<-qt(0.975,k-1)*seFE*mult
ln("metafor + HKSJ floor", muFE, muFE-hw, muFE+hw)
cat(sprintf("\nQ=%.4f, k-1=%d, Q/(k-1)=%.4f, tau2=%.5f, I2=%.1f%%\n", Q, k-1, Q/(k-1), rz$tau2, rz$I2))
