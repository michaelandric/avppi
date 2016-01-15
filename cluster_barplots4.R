# plotting the coef effects for significant clusters

# this version uses the 4 conditions (rather than main effects and interaction)
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

entropy_level <- factor(c('Low', 'High'))
# effects <- c('Aentr', 'Ventr', 'Aentr_intxn')
effects <- c('Aentr', 'Aentr_intxn')
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

total_unique_clusters <- 0

plots <- list()
plt_cnt <- 0
# now iterate through effects (or indiv conditions) and clusters
for (ef in effects)
{
    main_ef <- ef
    cl <- read.table(paste
                     ('group_effects_dec/clust_',ef,'_flt2_msk_mema_p.005_mask+tlrc.txt',
                      sep=''))$V1
    cl_var_name <- paste('clust_',ef,sep='')
    assign(cl_var_name, cl)
    unique_clusters <- length(unique(cl[cl > 0]))
    total_unique_clusters <- total_unique_clusters + unique_clusters
    for (i in 1:unique_clusters)
    {
        condition_vec <- rep(conditions, each=length(subjects))
        subjects_vec <- rep(subjects, length(conditions))
        aud_vec <- rep(entropy_level, each=length(subjects)*2)
        vis_vec <- rep(rep(entropy_level, each=length(subjects)), 2)
        subj_mean_vec <- c()
        for (cn in conditions)   # could change to conditions
        {
            m <- get(paste('subj_mat_', cn, sep=''))
            for (s in 1:length(subjects))
            {
                subj_mean_vec <- c(subj_mean_vec, mean(m[which(cl == i), s]))
            }
        }
        cluster_df <- tbl_df(data.frame
                             (subj_mean_vec, condition_vec, subjects_vec, aud_vec, vis_vec))
        names(cluster_df) <- c('clustermean', 'condition', 'subj', 'AuditoryEntropy', 'VisualEntropy')
        subj_means <- rep(tapply(cluster_df$clustermean, list(cluster_df$subj), mean), each=4)
        cluster_df <- cluster_df[order(cluster_df$subj), ]   # re-order
        cluster_df$demeaned <- cluster_df$clustermean - subj_means
        cond_stds <- tapply(cluster_df$demeaned,
                            list(cluster_df$AuditoryEntropy, cluster_df$VisualEntropy),
                            sd)
        within_err <- cond_stds / sqrt(length(subjects))   # Aud on left; Vis on top row
        mlt_within_err <- melt(within_err)
        
        # ggplot(cluster_df, aes(AuditoryEntropy, clustermean)) + geom_bar(aes(fill=VisualEntropy), position='dodge', stat='identity') + scale_fill_grey(start=.25, end=.75) + theme_bw()
        # mlt_df <- melt(tapply(cluster_df$clustermean, list(cluster_df$condition), mean))
        mlt_df <- melt(tapply(cluster_df$clustermean,
                              list(cluster_df$AuditoryEntropy,
                                   cluster_df$VisualEntropy), mean))
        mlt_df$within_err <- melt(within_err)$value
        names(mlt_df) <- c('AuditoryEntropy', 'VisualEntropy', 'value', 'within_err')
        
        # ggplot(mlt_df, aes(Var1, value)) + geom_bar(stat='identity', position='dodge')
        # ggplot(mlt_df, aes(Var1, value, group=Var2)) + geom_bar(aes(fill=Var2), stat='identity', position='dodge') + scale_fill_grey(start=.25, end=.75) + theme_bw()
        # ggplot(mlt_df, aes(Var1, value, group=Var2, color=Var2)) + geom_line() + geom_point(size=5) + theme_bw()
        
        plt_cnt = plt_cnt+1
        
        # bar plot
        bp <- ggplot(mlt_df, aes(AuditoryEntropy, value,
                                 group=VisualEntropy, fill=VisualEntropy)) +
            geom_bar(stat='identity', position=position_dodge(.9), alpha=.9) +
            geom_errorbar(aes(ymin=value-within_err, ymax=value+within_err),
                          position=position_dodge(.9), width=.5) +
            scale_fill_grey() + theme_bw() + ggtitle(paste(main_ef, 'cluster', i))

        # below has symbols but no error bars
 #       bp <- ggplot(mlt_df, aes(AuditoryEntropy, value,
 #                                group=VisualEntropy, shape=VisualEntropy,
 #                                linetype=VisualEntropy)) +
 #           geom_line() + geom_point(size=8) +
 #           ggtitle(paste(main_ef, 'cluster', i)) + theme_bw()
        
        # below has the error bars + position 'dodge'
#        bp <- ggplot(mlt_df, aes(AuditoryEntropy, value,
#                                 group=VisualEntropy,
#                                 shape=VisualEntropy, linetype=VisualEntropy,
#                                 ymin=value-within_err, ymax=value+within_err)) +
#            geom_line(position=position_dodge(.2)) + geom_point(size=8, position=position_dodge(.2)) +
#            geom_errorbar(width=.1, position=position_dodge(.2)) +
#            ggtitle(paste(main_ef, 'cluster', i)) + theme_bw()

#        bp <- ggplot(mlt_df, aes(AuditoryEntropy, value, group=VisualEntropy, shape=VisualEntropy, linetype=VisualEntropy)) + geom_line() + geom_point(size=8) + geom_errorbar(aes(ymin=value-within_err, ymax=value+within_err), width=.15) + ggtitle(paste(main_ef, 'cluster', i)) + theme_bw()
        print(bp)
        plots[[plt_cnt]] <- bp  # add each plot into plot list
    }
}

pdf('cluster_conditions_effect_plots2x2_p.005_bars_errbrs.pdf')
# pdf('cluster_conditions_effect_plots2x2_linepoint_errbrs.pdf')
for (n in seq(total_unique_clusters))
{
    print(plots[[n]])
}
dev.off()
