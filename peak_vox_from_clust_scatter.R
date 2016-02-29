setwd('/Users/andric/Documents/workspace/AVPPI/peak_vox_from_clust/')
library(dplyr)
library(ggplot2)
library(gridExtra)
library(reshape2)

peak_dat <- read.csv('peak_voxel_data.csv')
mlt_peak_dat <- melt(peak_dat)

ggplot(peak_dat, aes(x=Aentr_1, y=Aentr_intxn_0)) + geom_point(size=3) + geom_smooth(method=lm) + theme_bw()

combo_names <- combn(names(peak_dat), 2)
plots <- list()
plt_cnt = 0
pdf('peak_vox_from_clust_scatter_plots.pdf')
for (i in 1:dim(combo_names)[2])
{
    plt_cnt = plt_cnt+1
    plt <- ggplot(peak_dat, aes_string(x=combo_names[1,i], y=combo_names[2,i])) + geom_point(size=3) + geom_smooth(method=lm, se=FALSE, size=1.15) + theme_bw()
    plots[[plt_cnt]] <- plt  # add each plot into plot list
    print(plt)
}
dev.off()
