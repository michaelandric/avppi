# plotting the coef effects for significant clusters
setwd('/Users/andric/Documents/workspace/AVPPI/nii')
library(dplyr)
library(ggplot2)
library(gridExtra)
# below brings in 'multiplot' function
# http://www.cookbook-r.com/Graphs/Multiple_graphs_on_one_page_(ggplot2)/
source('/Users/andric/Documents/workspace/AVPPI/code/mult_gplot.R')

subjects <- c()
s_nums <- seq(1, 19)
s_nums <- s_nums[s_nums != 3]
s_nums <- s_nums[s_nums != 11]

for (s in s_nums)
{
    subjects <- c(subjects, paste('ss', s, sep=''))
}

nr <- 262245   # corresponding common space number of voxels

effects <- c('Aentr', 'Ventr', 'Aentr_intxn')

# read in the subj data for later use
for (ef in effects)
{
    subj_mat <- matrix(ncol=length(subjects), nrow=nr)
    for (i in 1:length(subjects))
    {
        ss <- subjects[i]
        subj_mat[, i] <- read.table(paste
                                    (ss,'_effects_dec/',ef,'_',ss,'_coef+tlrc.txt',
                                     sep=''))$V1
    }
    ef_mat_name <- paste('subj_mat_', ef, sep='')
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
                     ('group_effects_dec/clust_',ef,'_flt2_msk_mema_mask+tlrc.txt',
                      sep=''))$V1
    cl_var_name <- paste('clust_',ef,sep='')
    assign(cl_var_name, cl)
    unique_clusters <- length(unique(cl[cl > 0]))
    total_unique_clusters <- total_unique_clusters + unique_clusters
    for (i in 1:unique_clusters)
    {
        condition_vec <- rep(effects, each=length(subjects))
        subjects_vec <- rep(subjects, length(effects))
        subj_mean_vec <- c()
        for (ef in effects)   # could change to conditions
        {
            m <- get(paste('subj_mat_', ef, sep=''))
            for (s in 1:length(subjects))
            {
                subj_mean_vec <- c(subj_mean_vec, mean(m[which(cl == i), s]))
            }
        }
        cluster_df <- tbl_df(data.frame
                             (subj_mean_vec, condition_vec, subjects_vec))
        names(cluster_df) <- c('clustermean', 'effect', 'subj')
        plt_cnt = plt_cnt+1
        bp <- ggplot(cluster_df, aes(effect, clustermean, fill=effect)) +
            geom_boxplot(outlier.size=3) + ggtitle(paste(main_ef, 'cluster', i)) +
            xlab('effect') + ylab('means') + theme_bw()
        print(bp)
        plots[[plt_cnt]] <- bp  # add each plot into plot list
    }
}

pdf('cluster_effect_plots.pdf')
for (n in seq(total_unique_clusters))
{
    print(plots[[n]])
}
dev.off()

#pdf('cluster_effect_plots.pdf')
i = 1
plot = list() 
for (n in seq(total_unique_clusters)) {
    ### process data for plotting here ####
    plot[[i]] = plots[[n]]
    if (i %% 4 == 0) { ## print 9 plots on a page
        print (do.call(grid.arrange,  plot))
        plot = list() # reset plot 
        i = 0 # reset index
    }
    i = i + 1
}
if (length(plot) != 0) {  ## capture remaining plots that have not been written out
    print (do.call(grid.arrange,  plot))
}
#dev.off()

# qplot(x=effect, y=clustermean, data=cluster_df, fill=effect, stat='identity', geom='bar')
