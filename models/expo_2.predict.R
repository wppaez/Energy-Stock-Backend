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
datos$mean <- datos$mean
train_size <- round(1 *nrow(datos), 0) # since we're guessing the future, we use 100% of data.
train <- datos[1:train_size,]  # 100%

# time series
precio <- ts(train$mean, start=c(2017, 1, 1), frequency=365)
fit <- HoltWinters(precio, gamma=F)

# stats
df<-data.frame(z=train$mean[3:nrow(train)], zhat=fit$fitted[,1])
# SSE
py_SSE <- sum((df$z -df$zhat)^2)
# MSE
py_MSE <- sum((df$z -df$zhat)^2) /nrow(df)
# MAPE
py_MAPE <- (sum(abs(df$z -df$zhat) /df$z) /(nrow(df))) *100

# Predict
prediction <- predict(fit, n.ahead=(n_samples), prediction.interval=F, level=0.9) #intervalo de prediccion
output <- data.frame(prediction)
# plot(fit, data.frame(prediction))
