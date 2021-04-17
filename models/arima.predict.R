if("tidyverse" %in% rownames(installed.packages()) == FALSE){
  install.packages("tidyverse")
}
if("stats" %in% rownames(installed.packages()) == FALSE){
  install.packages("stats")
}
if("astsa" %in% rownames(installed.packages()) == FALSE){
  install.packages("astsa")
}
if("quantmod" %in% rownames(installed.packages()) == FALSE){
  install.packages("quantmod")
}
if("forecast" %in% rownames(installed.packages()) == FALSE){
  install.packages("forecast")
}
if("lubridate" %in% rownames(installed.packages()) == FALSE){
  install.packages("lubridate")
}
if("tseries" %in% rownames(installed.packages()) == FALSE){
  install.packages("tseries")
}
if("foreign" %in% rownames(installed.packages()) == FALSE){
  install.packages("foreign")
}
if("MLmetrics" %in% rownames(installed.packages()) == FALSE){
  install.packages("MLmetrics")
}
library(tidyverse)
library(stats)
library(astsa)
library(quantmod)
library(forecast)
library(lubridate)
library(tseries)
library(foreign)
library(MLmetrics)


#solo agarrando los datos desde 2016-04-13
datos <- read.csv(file=input_file,sep=",")


train_size <- round(1*nrow(datos), 0)
train <- datos[1:train_size,] 

serie <- ts(train$mean,start = c(2016,04,13),frequency =365)
plot(serie)

adf.test(serie,alternative = "stationary")
# valor p dio 0.059, es mayor a 0.05, entonces no rechazo Ho,por ende, no es estacionaria

#convirtiendo a estacionaria
seriedif=diff(serie)
seriedif
plot(seriedif)

#probando estacionaridad
adf.test(seriedif,alternative = "stationary") 
# valor p dio 0.01, es menor a 0.05, entonces rechazo Ho,por ende, es estacionaria

par(mfrow=c(1,2))
acf(ts(seriedif,frequency = 1))
pacf(ts(seriedif,frequency = 1))

modelo <- arima(serie,order = c(3,1,3),method = "ML")
modelo
tsdiag(modelo)


#Metricas
fitg<-as.data.frame(fitted.values(modelo))
df<-data.frame(z=train$mean, zhat=fitg$x)
# SSE
py_SSE <- sum((df$z -df$zhat)^2)
# MSE
py_MSE <- sum((df$z -df$zhat)^2) /nrow(df)
# MAPE
py_MAPE <- (sum(abs(df$z -df$zhat) /df$z) /(nrow(df))) *100

#pronostico

prediction <- predict(modelo, n.ahead=(n_samples), prediction.interval=F, level=0.9)#intervalo de prediccion
output <- data.frame(prediction)
