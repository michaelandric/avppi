# Ben's code to generate the markov chains
library(markovchain)
#create the High Transition Matrix
High <-matrix(c(0,.8,.2,0,0,0,.8,.2,.2,0,0,.8,.8,.2,0,0),byrow=TRUE,nrow = 4) 
rownames(High)<-colnames(High)<-c("1","2","3","4")
Highmc<-as(High, "markovchain")
#plot(Highmc)

#Generate many iterations of High markov chains
HLISTER <- c()
for ( i in 1:10000) {
    Hchain <- rmarkovchain(100, Highmc)
    Hfit <- markovchainFit(data=Hchain)
    Hdiff <- sum(abs(Hfit$estimate@transitionMatrix - High))
    HLISTER <-rbind(HLISTER,c(Hdiff,Hchain))
}
sHlister <- HLISTER[order(HLISTER[,1]),]
write.csv(sHlister, file = "HighChains.vis.csv")
#markovchainFit(sHlister[1,2:101])

for (i in 1:24) { 
    write.table(sHlister[i,2:101], file = paste0("H",i,".vis.txt"), row.names=FALSE, col.names=FALSE, quote=FALSE)
}

#create the Low transition Matrix
Low <-matrix(c(0,1/3,1/3,1/3,1/3,0,1/3,1/3,1/3,1/3,0,1/3,1/3,1/3,1/3,0),byrow=TRUE,nrow = 4) 
rownames(Low)<-colnames(Low)<-c("1","2","3","4")
Lowmc<-as(Low, "markovchain")
#plot(Lowmc)

#Generate many iterations of low markov chains
LLISTER <- c()
for ( i in 1:10000) {
    Lchain <- rmarkovchain(100, Lowmc)
    Lfit <- markovchainFit(data=Lchain)
    Ldiff <- sum(abs(Lfit$estimate@transitionMatrix - Low))
    LLISTER <-rbind(LLISTER,c(Ldiff,Lchain))
}

sLlister <- LLISTER[order(LLISTER[,1]),]
write.csv(sLlister, file = "LowChains.vis.csv")
#markovchainFit(sLlister[1,2:101])

for (i in 1:24) { 
    write.table(sLlister[i,2:101], file = paste0("L",i,".vis.txt"), row.names=FALSE, col.names=FALSE, quote=FALSE)
}
