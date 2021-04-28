#import packages#
library(astsa)
library(tsDyn)
library(readr)
library(e1071)

datos <- read.csv(input_file,sep=",")

train_size <- round(1*nrow(datos), 0)
train <- datos[1:train_size,] 


train_size1 <- round(0.9*nrow(datos), 0)
train1 <- datos[1:train_size1,] 
test1 <- datos[train_size1:nrow(datos),]


serie <- ts(train$mean,start = c(2016,04,13),frequency =365)

serie1 <- ts(train1$mean,start = c(2016,04,13),frequency =365)


#estimaci�n del modelo#

#lista de posibles modelos

mod <- list()
mod[["linear"]] <- linear(serie1, m=3)
mod[["SETAR"]] <- setar(serie1, m=3, thDelay = 1)
mod[["LSTAR"]] <- lstar(serie1, m=3, thDelay = 1)

sapply(mod, AIC)
sapply(mod, MAPE)

#de acuerdo con el AIC y el MAPE el mejor modelo es el SETAR#

modelo <- setar(serie,m=3, mL=3, mH=3, thDelay = 1)
modelo$fitted

modelo1 <- setar(serie1,m=3, mL=3, mH=3, thDelay = 1)
modelo1$fitted


#Metricas
fit_p<-data.frame(predict(modelo1, n.ahead=(nrow(test1))))
df<-data.frame(z=test1$mean, zhat=fit_p$predict.modelo1..n.ahead....nrow.test1...)
# SSE
py_SSE <- sum((df$z -df$zhat)^2)
# MSE
py_MSE <- sum((df$z -df$zhat)^2) /nrow(df)
# MAPE
py_MAPE <- (sum(abs(df$z -df$zhat) /df$z) /(nrow(df))) *100



#pronostico
prediction <- predict(modelo, n.ahead=(n_samples), prediction.interval=F, level=0.9)#intervalo de prediccion
output <- data.frame(prediction)



