if("dplyr" %in% rownames(installed.packages()) == FALSE){
  install.packages("dplyr")
}
if("readxl" %in% rownames(installed.packages()) == FALSE){
  install.packages("readxl")
}
if("writexl" %in% rownames(installed.packages()) == FALSE){
  install.packages("writexl")
}
if("ggplot2" %in% rownames(installed.packages()) == FALSE){
  install.packages("ggplot2")
}
if("ggcorrplot" %in% rownames(installed.packages()) == FALSE){
  install.packages("ggcorrplot")
}
if("TSA" %in% rownames(installed.packages()) == FALSE){
  install.packages("TSA")
}
if("rugarch" %in% rownames(installed.packages()) == FALSE){
  install.packages("rugarch")
}

if("stats" %in% rownames(installed.packages()) == FALSE){
  install.packages("stats")
}
if("astsa" %in% rownames(installed.packages()) == FALSE){
  install.packages("astsa")
}
if("forecast" %in% rownames(installed.packages()) == FALSE){
  install.packages("forecast")
}
if("tseries" %in% rownames(installed.packages()) == FALSE){
  install.packages("tseries")
}
if("car" %in% rownames(installed.packages()) == FALSE){
  install.packages("car")
}
if("caret" %in% rownames(installed.packages()) == FALSE){
  install.packages("caret")
}
if("nnet" %in% rownames(installed.packages()) == FALSE){
  install.packages("nnet")
}
if("tidyverse" %in% rownames(installed.packages()) == FALSE){
  install.packages("tidyverse")
}
if("xgboost" %in% rownames(installed.packages()) == FALSE){
  install.packages("xgboost")
}
if("data.table" %in% rownames(installed.packages()) == FALSE){
  install.packages("data.table")
}

library(dplyr)
library(readxl)
library(writexl)
library(ggplot2)
library(ggcorrplot)
library(stats)
library(astsa)
library(forecast)
library(tseries)
library(car)
library(caret)
library(nnet)
library(tidyverse)
library(xgboost)
library(data.table)





#datos 1 precio de oferta de despacho 
Y <- read.csv(file=despacho_file,sep=",")
Y=Y[,c(1,2)]
Y$Date <- as.Date(Y$Date,format="%Y-%m-%d")


#datos 2 precio de la escasez de activacion
Escazes <- read.csv(file=escasez_file,sep=",")
Escazes=Escazes[,c(1,2)]
Escazes$Date <- as.Date(Escazes$Date,format="%Y-%m-%d")



#JuntarDatos
for (i in 1:nrow(Y)) {
  if (Y$Date[i]==Escazes$Date[i]) {
    Y$Escazes[i] <- Escazes$Value[i]
  }else {
    Y$Escazes[i] <- "NA"
  }}


n <- nrow(Y)-31
x <- n+1
m <- n+31
Ytrain <- Y[1:n,]
Ytest <- Y[x:m,]


#SUAVIZACION Exponencial doble
serie <- ts(Y$Value,start = c(2017,12,01),frequency = 365)
modelo <- HoltWinters(serie,alpha = T,beta = T,gamma = F)


serie1 <- ts(Ytrain$Value,start = c(2017,12,01),frequency = 365)
modelo1 <- HoltWinters(serie1,alpha = T,beta = T,gamma = F)

#Metricas
fit_e<-as.data.frame(predict(modelo1, n.ahead=(nrow(Ytest)), prediction.interval=F))
df<-data.frame(z=Ytest$Value, zhat=fit_e$fit)
# SSE
py_SSE <- sum((df$z -df$zhat)^2)
# MSE
py_MSE <- sum((df$z -df$zhat)^2) /nrow(df)
# MAPE
py_MAPE <- (sum(abs(df$z -df$zhat) /df$z) /(nrow(df))) *100

#pronostico

prediction <- predict(modelo, n.ahead=(n_samples), prediction.interval=F, level=0.9)#intervalo de prediccion
output <- data.frame(prediction)
