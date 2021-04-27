library(tseries)
library(stats)
library(TSA)
library(rugarch)
library(e1071)

datos<- read.csv(input_file, sep= ",") 
train_size <- round(1 *nrow(datos), 0)
train <- datos[1:train_size,] 

train_size1 <- round(0.9*nrow(datos), 0)
train1 <- datos[1:train_size1,] 
test1 <- datos[train_size1:nrow(datos),] 


seriep <- ts(train$mean, start=c(2016,04,13), frequency=365)
serie1 <- ts(train1$mean, start=c(2016,04,13), frequency=365)
#modelo arima 
modelo <- arima(seriep,order = c(3,1,3),method = "ML")
modelo1 <- arima(serie1,order = c(3,1,3),method = "ML")
residuos<-residuals(modelo)

## el modelo ARCH/GARCH escogido es GARCH(0,19)
#Estimaci�n del modelo

spec = ugarchspec(variance.model = list(model="sGARCH",garchOrder=c(0,19)),
                  mean.model = list(armaOrder=c(3,3))) 
fit=ugarchfit(spec=spec, data=seriep)
fitted=fitted(fit)


spec1 = ugarchspec(variance.model = list(model="sGARCH",garchOrder=c(0,19)),
                  mean.model = list(armaOrder=c(3,3))) 
fit1=ugarchfit(spec=spec1, data=serie1)


#M�tricas de error
bootp1=ugarchboot(fit1,method=c("Partial","Full")[1],n.ahead = nrow(test1),n.bootpred=1000,n.bootfit=1000)
s_f1=bootp1@forc@forecast$seriesFor 
prediction=as.vector(s_f1)
price<- data.frame(prediction)
df<-data.frame(z=test1$mean, zhat=price$prediction)
# SSE
py_SSE <- sum((df$z -df$zhat)^2)
# MSE
py_MSE <- sum((df$z -df$zhat)^2) /nrow(df)
# MAPE
py_MAPE <- (sum(abs(df$z -df$zhat) /df$z) /(nrow(df))) *100


#Pron�stico
bootp=ugarchboot(fit,method=c("Partial","Full")[1],n.ahead = n_samples,n.bootpred=1000,n.bootfit=1000)

s_f=bootp@forc@forecast$seriesFor 
precio=as.vector(s_f)
output <- data.frame(precio)

