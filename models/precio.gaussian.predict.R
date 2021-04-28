library(stats)#
library(kernlab)#
library(forecast) #
library(dplyr)#


#datos 1 precio de oferta de despacho 
Y <- read.csv(despacho_file,sep=",")
Y=Y[,c(1,2)]
Y$Date <- as.Date(Y$Date,format="%Y-%m-%d")


#datos 2 precio de la escasez de activacion
Escazes <- read.csv(escasez_file,sep=",")
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


#ARIMA para el precio de la escasez
serieEsc <- ts(Escazes$Value,start = c(2017,12,01),frequency = 365)
modeloEsc <- auto.arima(serieEsc)
pronosticoEsc <- forecast(modeloEsc,h=(n_samples))
pronosticoEsc$mean
datosEsc <- data.frame(pronosticoEsc$mean)
names(datosEsc) <- c("Value")

datosEsc <-datosEsc %>% 
  mutate(consecutive=seq(1,nrow(datosEsc))) 

datosEsc$Date <-Escazes$Date[nrow(Escazes)] + datosEsc$consecutive

datosML <- datosEsc[,-2]
names(datosML) <-c("Escazes","Date")

#Gaussian Process

modelo <- gausspr(Value~.,data=Y,var=2)

modelo1 <- gausspr(Value~.,data=Ytrain,var=2)


#Metricas
fitg<-as.data.frame(predict(modelo1, Ytest))
df<-data.frame(z=Ytest$Value, zhat=fitg$V1)
# SSE
py_SSE <- sum((df$z -df$zhat)^2)
# MSE
py_MSE <- sum((df$z -df$zhat)^2) /nrow(df)
# MAPE
py_MAPE <- (sum(abs(df$z -df$zhat) /df$z) /(nrow(df))) *100

#pronostico
prediction <- predict(modelo, datosML)
output <- data.frame(prediction)
