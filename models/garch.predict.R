
if("tseries" %in% rownames(installed.packages()) == FALSE){
  install.packages("tseries")
}
if("FinTS" %in% rownames(installed.packages()) == FALSE){
  install.packages("FinTS")
}
if("stats" %in% rownames(installed.packages()) == FALSE){
  install.packages("stats")
}
if("forecast" %in% rownames(installed.packages()) == FALSE){
  install.packages("forecast")
}
if("zoo" %in% rownames(installed.packages()) == FALSE){
  install.packages("zoo")
}
if("TSA" %in% rownames(installed.packages()) == FALSE){
  install.packages("TSA")
}
if("rugarch" %in% rownames(installed.packages()) == FALSE){
  install.packages("rugarch")
}

library("MLmetrics")
library("tseries")
library("FinTS")
library("stats")
library("forecast")
library("zoo")
library("TSA")
library("rugarch")

datos<- read.csv(input_file, sep= ",") 
datos$mean <- datos$mean
train_size <- round(1 *nrow(datos), 0)
train <- datos[1:train_size,] 
train$mean<-datos$mean

seriep <- ts(train$mean, start=c(2017,1,1), frequency=365)
View(seriep)

#modelo arima 
modelo <- arima(seriep,order = c(3,1,3),method = "ML")
modelo
residuos<-residuals(modelo)

## el modelo ARCH/GARCH escogido es GARCH(0,19)
#Estimación del modelo
fitg<-(fitted.values(modelo))
fitgarch<- fitted.values(garch(residuos,order = c(0,19),trace=F))[,1]
low <- fitg - (1.96*fitgarch)
high <- fitg + (1.96*fitgarch)
par(mfrow=c(1,1))
lines(low,col="blue")
lines(high,col="green")
lines(fitg,col="red")

spec = ugarchspec(variance.model = list(model="sGARCH",garchOrder=c(0,19)),
                  mean.model = list(armaOrder=c(3,3))) 
fit=ugarchfit(spec=spec, data=seriep)
fitted=fitted(fit)

#Métricas de error
df<-data.frame(z=train$mean, zhat=fitted)
# SSE
py_SSE <- sum((df$z -df$zhat)^2)
# MSE
py_MSE <- sum((df$z -df$zhat)^2) /nrow(df)
# MAPE
py_MAPE <- (sum(abs(df$z -df$zhat) /df$z) /(nrow(df))) *100


#Pronóstico
ugfore=ugarchforecast(fit, n.ahead =n_samples, levels=0.9)
bootp=ugarchboot(fit,method=c("Partial","Full")[1],n.ahead = n_samples,n.bootpred=1000,n.bootfit=1000)

s_f=bootp@forc@forecast$seriesFor 
precio=as.vector(s_f)
output <- data.frame(precio)

