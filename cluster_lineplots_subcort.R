setwd('/Users/andric/Documents/workspace/AVPPI/nii')
library(dplyr)
library(ggplot2)
library(gridExtra)
# below brings in 'multiplot' function
# http://www.cookbook-r.com/Graphs/Multiple_graphs_on_one_page_(ggplot2)/
# source('/Users/andric/Documents/workspace/AVPPI/code/mult_gplot.R')

subjects <- c()
s_nums <- seq(1, 19)
s_nums <- s_nums[s_nums != 3]
s_nums <- s_nums[s_nums != 11]
for (s in s_nums)
{
    subjects <- c(subjects, paste('ss', s, sep=''))
}

nr <- 262245   # corresponding common space number of voxels

rois <- c('Left-Caudate', 'Left-Putamen', 'Left-Hippocampus',
          'Right-Caudate', 'Right-Putamen', 'Right-Hippocampus')
labels <- read.table('subcort_masks/labels.txt', header=T)
rois_ids <- c(labels$id[labels$Label %in% rois])
conditions <- c('ALowVLow', 'ALowVHigh', 'AHighVLow', 'AHighVHigh')
# read in the subj data for later use
suffx <- paste('Powered.cleanEPI_REML_fnirted_MNI2mm.txt')
for (cn in conditions)
{
    subj_mat <- matrix(ncol=length(subjects), nrow=nr)
    for (i in 1:length(subjects))
    {
        ss <- subjects[i]
        subj_mat[, i] <- read.table(paste
                                    ('deconvolve_outs_concat_dec/',
                                     cn,'_coef_',s_nums[i],'_concat.',suffx, sep=''))$V1
    }
    ef_mat_name <- paste('subj_mat_', cn, sep='')
    assign(ef_mat_name, subj_mat)
}

subcort_mat <- matrix(ncol=length(subjects), nrow=nr)
for (i in 1:length(subjects))
{
    ss <- subjects[i]
    subcort_mat[, i] <- read.table(paste('subcort_masks/',
                                         i,'_T1_subcort_seg_fnirted_MNI2mm.txt',
                                         sep=''))$V1
}

cluster_df <- data.frame() %>% tbl_df
for (rg in rois_ids)
{
    region <- paste(labels$Label[which(labels$id==rg)])
    condition_vec <- rep(conditions, each=length(subjects))
    subjects_vec <- rep(subjects, length(conditions))
    aud_vec <- rep(entropy_level, each=length(subjects)*2)
    vis_vec <- rep(rep(entropy_level, each=length(subjects)), 2)
    region_id_vec <- as.factor(rep(region, length(subjects)*
                                        length(entropy_level)*
                                        length(modality)))
    subj_mean_vec <- c()    
    
    for (cn in conditions)   # could change to conditions
    {
        m <- get(paste('subj_mat_', cn, sep=''))
        for (s in 1:length(subjects))
        {
            subj_mean_vec <- c(subj_mean_vec, mean(m[which(subcort_mat[,s] == rg), s]))
        }
    }
    cluster_df <- rbind(cluster_df,
                        tbl_df(data.frame(subj_mean_vec, condition_vec,
                                          subjects_vec, aud_vec, vis_vec,
                                          region_id_vec)))
}
names(cluster_df) <- c('clustermean', 'condition', 'subj',
                       'AuditoryEntropy', 'VisualEntropy', 'Region')
mn_mlt <- melt(tapply(cluster_df$clustermean,
                      list(cluster_df$condition, cluster_df$Region), mean))
names(mn_mlt) <- c('condition', 'Region', 'value')
mn_mlt$Region <- as.factor(mn_mlt$Region)
bp <- ggplot(mn_mlt, aes(condition, value,
                         group=Region, colour=as.factor(Region))) +
    geom_line() + geom_point(size=4) + ggtitle(paste('Subcortical Regions')) +
    xlab('Conditions') + ylab('Means') + theme_bw()
print(bp)


pdf('subcort_regions_conditions_lineplot.pdf')
print(bp)
dev.off()

# summary(aov(clustermean ~ condition + Error(subj/condition), cluster_df))
