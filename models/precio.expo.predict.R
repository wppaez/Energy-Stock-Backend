library(stats)#


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
