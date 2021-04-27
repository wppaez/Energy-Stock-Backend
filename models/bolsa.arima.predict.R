library(astsa)
library(forecast)
library(tseries)
library(stats)

#solo agarrando los datos desde 2016-04-13
datos <- read.csv(input_file, sep=",")

train_size <- round(1*nrow(datos), 0)
train <- datos[1:train_size,] 


train_size1 <- round(0.9*nrow(datos), 0)
train1 <- datos[1:train_size1,] 
test1 <- datos[train_size1:nrow(datos),] 


serie <- ts(train$mean,start = c(2016,04,13),frequency =365)
modelo <- auto.arima(serie)


serie1 <- ts(train1$mean,start = c(2016,04,13),frequency =365)
modelo1 <- auto.arima(serie1)

#Metricas
fit_p<-data.frame(predict(modelo1, n.ahead=(nrow(test1))))
df<-data.frame(z=test1$mean, zhat=fit_p$pred)
# SSE
py_SSE <- sum((df$z -df$zhat)^2)
# MSE
py_MSE <- sum((df$z -df$zhat)^2) /nrow(df)
# MAPE
py_MAPE <- (sum(abs(df$z -df$zhat) /df$z) /(nrow(df))) *100

#pronostico

prediction <- predict(modelo, n.ahead=(n_samples), prediction.interval=F, level=0.9) #intervalo de prediccion
output <- data.frame(prediction)
