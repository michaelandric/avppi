setwd('/Users/andric/Documents/workspace/AVPPI/nii/dice_coefs/')
library(dplyr)
library(ggplot2)
library(gridExtra)
library(reshape2)

# all
full <- read.table('out_dice_all_Aentr_intxn.scores')

# intxn
intxn <- read.table('out_dice_Aentr_intxn.scores')

steps <- c(1, 4, 6)
blocks <- c('30s & 20s', '20s & 15s', '15s & 10s')
full_steps <- data.frame(full[steps,], blocks)
names(full_steps) <- c('coef', 'blocks')
intxn_steps <- data.frame(intxn[steps,], blocks)
names(intxn_steps) <- c('coef', 'blocks')

pdf('dice_plots.pdf')
intxn_steps$blocks <- factor(intxn_steps$blocks, levels=rev(levels(intxn_steps$blocks)))
plt <- ggplot(intxn_steps, aes(x=blocks, y=coef, group=1, ymin=0, ymax=.8)) + geom_point(size=5) + geom_line(size=1) + ggtitle('Dice coefficients (Interaction cluster only)') + theme_bw()
print(plt)

full_steps$blocks <- factor(full_steps$blocks, levels=rev(levels(full_steps$blocks)))
plt <- ggplot(full_steps, aes(x=blocks, y=coef, group=1, ymin=0, ymax=.8)) + geom_point(size=5) + geom_line(size=1) + ggtitle('Dice coefficients (All significant voxels)') + theme_bw()
print(plt)
dev.off()
