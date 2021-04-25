# handle missing packages
if("tseries" %in% rownames(installed.packages()) == FALSE){
    install.packages("tseries")
}
if("forecast" %in% rownames(installed.packages()) == FALSE){
    install.packages("forecast")
}
if("ggplot2" %in% rownames(installed.packages()) == FALSE){
    install.packages("ggplot2")
}
if("MLmetrics" %in% rownames(installed.packages()) == FALSE){
    install.packages("MLmetrics")
}

# import packages.
library("tseries")
library("forecast")
library("ggplot2")
library("MLmetrics")

datos <- read.csv(input_file, sep= "," )
datos$mean<-log(datos$mean)
train_size <- round(1 *nrow(datos), 0) # since we're guessing the future, we use 100% of data.
train <- datos[1:train_size,]  # 100%

train_size1 <- round(0.9*nrow(datos), 0)
train1 <- datos[1:train_size1,] 
test1 <- datos[train_size1:nrow(datos),] 

# time series
precio <- ts(train$mean, start=c(2016,04,13), frequency=365)
fit <- HoltWinters(precio, gamma=F)

precio1 <- ts(train1$mean, start=c(2016,04,13), frequency=365)
fit1 <- HoltWinters(precio1, gamma=F)

# stats
fit_e<-as.data.frame(predict(fit1, n.ahead=(nrow(test1)), prediction.interval=F))
df<-data.frame(z=test1$mean, zhat=fit_e$fit)
# SSE
py_SSE <- sum((df$z -df$zhat)^2)
# MSE
py_MSE <- sum((df$z -df$zhat)^2) /nrow(df)
# MAPE
py_MAPE <- (sum(abs(df$z -df$zhat) /df$z) /(nrow(df))) *100

# Predict
prediction <- predict(fit, n.ahead=n_samples, prediction.interval=F, level=0.9)#intervalo de prediccion
output <- data.frame(exp(prediction))
