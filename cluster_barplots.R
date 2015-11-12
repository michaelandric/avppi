# plotting the coef effects for significant clusters
setwd('/Users/andric/Documents/workspace/AVPPI/nii')
library(dplyr)
library(ggplot2)

subjects <- c()
s_nums <- seq(1, 18)[seq(1,18) != 11]   # bcs ss 11 (and 19) no good 
for (s in s_nums)
{
    subjects <- c(subjects, paste('ss', s, sep=''))
}

effects <- c('Aentr', 'Ventr', 'Aentr_intxn')

condition_vec <- rep(effects, each=length(subjects))
for (ss in subjects)
