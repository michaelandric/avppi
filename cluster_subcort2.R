setwd('/Users/andric/Documents/workspace/AVPPI/nii')
library(dplyr)
library(ggplot2)
library(gridExtra)
library(reshape2)
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
effects <- c('Aentr', 'Ventr', 'Aentr_intxn')
regularity <- c('low', 'high')
auditory <- rep(regularity, each=length(subjects)*2)
visual <- rep(rep(regularity, each=length(subjects)), 2)

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


plots <- list()
plt_cnt <- 0
for (rg in rois_ids)
{
    region <- paste(labels$Label[which(labels$id==rg)])
    condition_vec <- rep(conditions, each=length(subjects))
    subjects_vec <- rep(subjects, length(conditions))
    subj_mean_vec <- c()
    for (cn in conditions)   # could change to conditions
    {
        m <- get(paste('subj_mat_', cn, sep=''))
        for (s in 1:length(subjects))
        {
            subj_mean_vec <- c(subj_mean_vec, mean(m[which(subcort_mat[,s] == rg), s]))
        }
    }
    cluster_df <- tbl_df(data.frame
                         (subj_mean_vec, condition_vec, subjects_vec, auditory, visual))
    names(cluster_df) <- c('clustermean', 'condition', 'subj', 'AuditoryRegularity', 'VisualRegularity')
    subj_means <- rep(tapply(cluster_df$clustermean, list(cluster_df$subj), mean), each=4)
    cluster_df <- cluster_df[order(cluster_df$subj), ]   # re-order
    cluster_df$demeaned <- cluster_df$clustermean - subj_means
    cond_stds <- tapply(cluster_df$demeaned, list(cluster_df$AuditoryRegularity, cluster_df$VisualRegularity),sd)
    within_err <- cond_stds / sqrt(length(subjects))   # Aud on left; Vis on top row
    mlt_within_err <- melt(within_err)
    mlt_df <- melt(tapply(cluster_df$clustermean,
                          list(cluster_df$AuditoryRegularity,
                               cluster_df$VisualRegularity), mean))
    mlt_df$within_err <- melt(within_err)$value
    names(mlt_df) <- c('AuditoryRegularity', 'VisualRegularity', 'value', 'within_err')

    plt_cnt = plt_cnt+1
    bp <- ggplot(mlt_df, aes(AuditoryRegularity, value,
                             group=VisualRegularity, fill=VisualRegularity)) +
        geom_bar(stat='identity', position=position_dodge(.9), alpha=.9) +
        geom_errorbar(aes(ymin=value-within_err, ymax=value+within_err),
                      position=position_dodge(.9), width=.5) +
        scale_fill_grey() + theme_bw() + ggtitle(paste(region))    
    print(region)
    print(summary(aov(clustermean ~ AuditoryRegularity*VisualRegularity + Error(subj/(AuditoryRegularity*VisualRegularity)), cluster_df)))
    print(bp)
    plots[[plt_cnt]] <- bp  # add each plot into plot list
}

pdf('subcort2_regions_conditions_barplots.pdf')
for (n in seq(rois_ids))
{
    print(plots[[n]])
}
dev.off()

# summary(aov(clustermean ~ condition + Error(subj/condition), cluster_df))
