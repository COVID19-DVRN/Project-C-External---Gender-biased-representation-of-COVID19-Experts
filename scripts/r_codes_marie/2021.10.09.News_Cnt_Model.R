news_cnt_df <- read.csv("C:/Users/Utilisateur/.../08_01_01_entity_race_gender_expertise_news_count.csv")

head(news_cnt_df)
names(news_cnt_df)

table(news_cnt_df$sex)
table(news_cnt_df$pronoun)
table(news_cnt_df$race)
table(news_cnt_df$urm)
table(news_cnt_df$pronoun_urm)
table(news_cnt_df$public_health_researcher)
table(news_cnt_df$practitioner)
table(news_cnt_df$non_public_health_researcher)
table(news_cnt_df$policymaker)
table(news_cnt_df$industry_expert)
table(news_cnt_df$celebrity)
table(news_cnt_df$journalist)
table(news_cnt_df$expertise_label_by_relative_expertise)
table(news_cnt_df$expertise_label_by_relative_reach)

news_cnt_df$news_count_gt_1 <- ifelse(news_cnt_df$news_count > 1,1,0)
news_cnt_df$news_count_gt_2 <- ifelse(news_cnt_df$news_count > 2,1,0)

news_cnt_df$urm_10 <- ifelse(news_cnt_df$urm == "Yes",1,0)
news_cnt_df$female_10 <- ifelse(news_cnt_df$sex == "Female",1,0)
news_cnt_df$main_prof_pm_10 <- ifelse(news_cnt_df$expertise_label_by_relative_expertise == "policymaker",1,0)
news_cnt_df$main_prof_ph_10 <- ifelse(news_cnt_df$expertise_label_by_relative_expertise == "public_health_researcher",1,0)
news_cnt_df$main_prof_celebrity_10 <- ifelse(news_cnt_df$expertise_label_by_relative_expertise == "celebrity",1,0)
news_cnt_df$main_prof_journalist_10 <- ifelse(news_cnt_df$expertise_label_by_relative_expertise == "journalist",1,0)
news_cnt_df$main_prof_ie_10 <- ifelse(news_cnt_df$expertise_label_by_relative_expertise == "industry_expert",1,0)
news_cnt_df$main_prof_practitioner_10 <- ifelse(news_cnt_df$expertise_label_by_relative_expertise == "practitioner",1,0)
news_cnt_df$main_prof_nph_10 <- ifelse(news_cnt_df$expertise_label_by_relative_expertise == "non_public_health_researcher",1,0)
news_cnt_df$main_prof_celebrity_journalist_ie_10 <- ifelse(news_cnt_df$main_prof_journalist_10 == 1 | news_cnt_df$main_prof_ie_10 == 1 | news_cnt_df$main_prof_celebrity_10 == 1,1,0)

news_cnt_df$reach_prof_pm_10 <- ifelse(news_cnt_df$expertise_label_by_relative_reach == "policymaker",1,0)
news_cnt_df$reach_prof_ph_10 <- ifelse(news_cnt_df$expertise_label_by_relative_reach == "public_health_researcher",1,0)
news_cnt_df$reach_prof_celebrity_10 <- ifelse(news_cnt_df$expertise_label_by_relative_reach == "celebrity",1,0)
news_cnt_df$reach_prof_journalist_10 <- ifelse(news_cnt_df$expertise_label_by_relative_reach == "journalist",1,0)
news_cnt_df$reach_prof_ie_10 <- ifelse(news_cnt_df$expertise_label_by_relative_reach == "industry_expert",1,0)
news_cnt_df$reach_prof_practitioner_10 <- ifelse(news_cnt_df$expertise_label_by_relative_reach == "practitioner",1,0)
news_cnt_df$reach_prof_nph_10 <- ifelse(news_cnt_df$expertise_label_by_relative_reach == "non_public_health_researcher",1,0)
news_cnt_df$reach_prof_celebrity_journalist_ie_10 <- ifelse(news_cnt_df$reach_prof_journalist_10 == 1 | news_cnt_df$reach_prof_ie_10 == 1 | news_cnt_df$reach_prof_celebrity_10 == 1,1,0)

news_cnt_df$non_urm_she <- ifelse(news_cnt_df$pronoun_urm == "non_urm_she",1,0)
news_cnt_df$non_urm_he <-  ifelse(news_cnt_df$pronoun_urm == "non_urm_he",1,0) # reference
news_cnt_df$urm_or_they <- ifelse(news_cnt_df$non_urm_she == 0 & news_cnt_df$non_urm_he == 0,1,0)
news_cnt_df$white <- ifelse(news_cnt_df$race == "White/European",1,0) # reference
news_cnt_df$non_white <- ifelse(news_cnt_df$white == 0,1,0)
news_cnt_df$non_public_health_researcher_10 <- ifelse(news_cnt_df$non_public_health_researcher == "Yes",1,0)
news_cnt_df$public_health_researcher_10 <- ifelse(news_cnt_df$public_health_researcher == "Yes",1,0)
news_cnt_df$practitioner_10 <- ifelse(news_cnt_df$practitioner == "Yes",1,0)
news_cnt_df$policymaker_10 <- ifelse(news_cnt_df$policymaker == "Yes",1,0)
news_cnt_df$industry_expert_10 <- ifelse(news_cnt_df$industry_expert == "Yes",1,0)
news_cnt_df$celebrity_10 <- ifelse(news_cnt_df$celebrity == "Yes",1,0)
news_cnt_df$journalist_10 <-ifelse(news_cnt_df$journalist == "Yes",1,0)
news_cnt_df$indexpert_celebrity_10 <- ifelse(news_cnt_df$industry_expert_10 == 1 | news_cnt_df$celebrity_10 == 1,1,0)
news_cnt_df$indexpert_celebrity_journalist_10 <- ifelse(news_cnt_df$indexpert_celebrity_10 == 1 | news_cnt_df$journalist_10 == 1, 1, 0)
# reference: non public health researcher
quantile(news_cnt_df$news_count,probs=seq(0,1,0.01))
# 61%: 1.00, 62%: 1.16, 63%: 2.00

news_cnt_df_nothey_available <- news_cnt_df[news_cnt_df$expertise_label_by_relative_expertise != 'not_available' & news_cnt_df$pronoun != "They",]
dim(news_cnt_df_nothey_available)

# Intersection of race/gender and profession

# non_urm_she & PH , non-urm-she & policy maker
news_cnt_df$non_urm_she_ph <- ifelse(news_cnt_df$non_urm_she == 1 & news_cnt_df$public_health_researcher_10 == 1,1,0)
news_cnt_df$non_urm_she_policymaker <- ifelse(news_cnt_df$non_urm_she == 1 & news_cnt_df$policymaker_10 == 1,1,0)

# urm_or_they & PH, urm_or_they & policy maker
news_cnt_df$urm_or_they_ph <- ifelse(news_cnt_df$urm_or_they == 1 & news_cnt_df$public_health_researcher_10 == 1,1,0)
news_cnt_df$urm_or_they_policymaker <- ifelse(news_cnt_df$urm_or_they == 1 & news_cnt_df$policymaker_10 == 1,1,0)

# Intersection of professions
# policy maker & PH researcher (1), PH researcher & practitioner (2)
news_cnt_df$policymaker_ph <- ifelse(news_cnt_df$policymaker_10 == 1 & news_cnt_df$public_health_researcher_10 == 1,1,0)
news_cnt_df$ph_practitioner <- ifelse(news_cnt_df$practitioner_10 == 1 & news_cnt_df$public_health_researcher_10 == 1,1,0)

# policy maker but not PH researcher (3), PH researcher but not practitioner (4) -- complement of other binary indicators
# other professions: ind experts, journalists, celebrities -- let us not consider interactions for these occupations

### Part 1: outcome = # of mentions > 2 ###

## No collapse ##

# Model with (1) interactions between two professions and (2) interactions between race/gender and profession
# > 1
# industry expert, celebrity, and journalist kept separate
log_reg_gt1_interaction2 <- glm(news_count_gt_1 ~  non_urm_she + urm_or_they + 
                   policymaker_10 +  
                   public_health_researcher_10 +
                   practitioner_10 + 
                   #non_public_health_researcher_10 +
                   industry_expert_10 + 
                   celebrity_10 + 
                   journalist_10 +
                   # professional interactions
                   policymaker_ph + ph_practitioner + public_health_researcher:practitioner +
                   # race/gender and profession
                   non_urm_she_ph + 
                   non_urm_she_policymaker + 
                   urm_or_they_ph + 
                   urm_or_they_policymaker, data = news_cnt_df, family = "binomial")
summary(log_reg_gt1_interaction2)
confint.default(log_reg_gt1_interaction2)

#mod1b <- lrm(y ~ x) need to investigate this further

cor(log_reg_gt1_interaction2$fitted.values, news_cnt_df$news_count_gt_1)

# Simple - No interaction
log_reg_gt1_simple_nointeraction <- glm(news_count_gt_1 ~ urm_10 + female_10 +
                                          main_prof_pm_10 +
                                        main_prof_ph_10 +
                                        main_prof_celebrity_10 +
                                        main_prof_journalist_10 +
                                        main_prof_ie_10 +
                                        main_prof_practitioner_10,
                                        data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt1_simple_nointeraction)
exp(coef(log_reg_gt1_simple_nointeraction))
confint.default(log_reg_gt1_simple_nointeraction)
exp(cbind(OR = coef(log_reg_gt1_simple_nointeraction), confint(log_reg_gt1_simple_nointeraction)))
cor(log_reg_gt1_simple_nointeraction$fitted.values, news_cnt_df_nothey_available$news_count_gt_1)
cor(log_reg_gt1_simple_nointeraction$fitted.values, news_cnt_df_nothey_available$news_count_gt_1,method='spearman')
cor(log_reg_gt1_simple_nointeraction$fitted.values, news_cnt_df_nothey_available$news_count_gt_1,method='kendall')
PseudoR2(log_reg_gt1_simple_nointeraction,c("AldrichNelson","Nagelkerke"))


# Univariate
log_reg_gt1_simple_nointeraction <- glm(news_count_gt_1 ~ female_10 ,
                                        data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt1_simple_nointeraction)
exp(coef(log_reg_gt1_simple_nointeraction))
confint.default(log_reg_gt1_simple_nointeraction)
exp(cbind(OR = coef(log_reg_gt1_simple_nointeraction), confint(log_reg_gt1_simple_nointeraction)))
cor(log_reg_gt1_simple_nointeraction$fitted.values, news_cnt_df_nothey_available$news_count_gt_1)
cor(log_reg_gt1_simple_nointeraction$fitted.values, news_cnt_df_nothey_available$news_count_gt_1,method='spearman')
cor(log_reg_gt1_simple_nointeraction$fitted.values, news_cnt_df_nothey_available$news_count_gt_1,method='kendall')
PseudoR2(log_reg_gt1_simple_nointeraction,c("AldrichNelson","Nagelkerke"))

public_health_researcher_10 <- ifelse(news_cnt_df$public_health_researcher == "Yes",1,0)
news_cnt_df$practitioner_10 <- ifelse(news_cnt_df$practitioner == "Yes",1,0)
news_cnt_df$policymaker_10 <- ifelse(news_cnt_df$policymaker == "Yes",1,0)
news_cnt_df$industry_expert_10 <- ifelse(news_cnt_df$industry_expert == "Yes",1,0)
news_cnt_df$celebrity_10 <- ifelse(news_cnt_df$celebrity == "Yes",1,0)
news_cnt_df$journalist_10 <-ifelse(news_cnt_df$journalist == "Yes",1,0)
news_cnt_df$indexpert_celebrity_10 <- ifelse(news_cnt_df$industry_expert_10 == 1 | news_cnt_df$celebrity_10 == 1,1,0)
news_cnt_df$indexpert_celebrity_journalist_10
# 
log_reg_gt1_simple_nointeraction <- glm(news_count_gt_1 ~ urm_10 + female_10 +
                                          main_prof_pm_10 + 
                                          main_prof_ph_10 +
                                          main_prof_celebrity_10 +
                                          main_prof_journalist_10 + 
                                          main_prof_ie_10 + 
                                          main_prof_practitioner_10,
                                        data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt1_simple_nointeraction)
exp(coef(log_reg_gt1_simple_nointeraction))
confint.default(log_reg_gt1_simple_nointeraction)
cor(log_reg_gt1_simple_nointeraction$fitted.values, news_cnt_df_nothey_available$news_count_gt_1)
cor(log_reg_gt1_simple_nointeraction$fitted.values, news_cnt_df_nothey_available$news_count_gt_1,method='spearman')
cor(log_reg_gt1_simple_nointeraction$fitted.values, news_cnt_df_nothey_available$news_count_gt_1,method='kendall')
PseudoR2(log_reg_gt1_simple_nointeraction_reach,c("AldrichNelson","Nagelkerke"))

# Simple - No interaction - Reach
log_reg_gt1_simple_nointeraction_reach <- glm(news_count_gt_1 ~ urm_10 + female_10 +
                                          reach_prof_pm_10 +
                                          reach_prof_ph_10 +
                                          reach_prof_celebrity_10 +
                                          reach_prof_journalist_10 +
                                          reach_prof_ie_10 +
                                          reach_prof_practitioner_10,
                                        data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt1_simple_nointeraction_reach)
exp(coef(log_reg_gt1_simple_nointeraction_reach))
confint.default(log_reg_gt1_simple_nointeraction_reach)
cor(log_reg_gt1_simple_nointeraction_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_1)
cor(log_reg_gt1_simple_nointeraction_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_1,method='spearman')
cor(log_reg_gt1_simple_nointeraction_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_1,method='kendall')
PseudoR2(log_reg_gt1_simple_nointeraction_reach,c("AldrichNelson","Nagelkerke"))


# Simple - No interaction - Collapse
log_reg_gt1_simple_nointeraction_collapse <- glm(news_count_gt_1 ~ urm_10 + female_10 +
                                                   main_prof_pm_10 +
                                                   main_prof_ph_10 +
                                                   main_prof_celebrity_journalist_ie_10 +
                                                   main_prof_practitioner_10,
                                                 data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt1_simple_nointeraction_collapse)
exp(coef(log_reg_gt1_simple_nointeraction_collapse))
confint.default(log_reg_gt1_simple_nointeraction_collapse)
cor(log_reg_gt1_simple_nointeraction_collapse$fitted.values, news_cnt_df_nothey_available$news_count_gt_1)
cor(log_reg_gt1_simple_nointeraction_collapse$fitted.values, news_cnt_df_nothey_available$news_count_gt_1,method='spearman')
cor(log_reg_gt1_simple_nointeraction_collapse$fitted.values, news_cnt_df_nothey_available$news_count_gt_1,method='kendall')
PseudoR2(log_reg_gt1_simple_nointeraction_collapse,c("AldrichNelson","Nagelkerke"))


# Simple - No interaction - Collapse - Reach
log_reg_gt1_simple_nointeraction_collapse_reach <- glm(news_count_gt_1 ~ urm_10 + female_10 +
                                                   reach_prof_pm_10 +
                                                   reach_prof_ph_10 +
                                                   reach_prof_celebrity_journalist_ie_10 +
                                                   reach_prof_practitioner_10,
                                                 data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt1_simple_nointeraction_collapse_reach)
exp(coef(log_reg_gt1_simple_nointeraction_collapse_reach))
confint.default(log_reg_gt1_simple_nointeraction_collapse_reach)
cor(log_reg_gt1_simple_nointeraction_collapse_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_1)
cor(log_reg_gt1_simple_nointeraction_collapse_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_1,method='spearman')
cor(log_reg_gt1_simple_nointeraction_collapse_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_1,method='kendall')
PseudoR2(log_reg_gt1_simple_nointeraction_collapse_reach,c("AldrichNelson","Nagelkerke"))


# Simple - Inreraction sex/URM
log_reg_gt1_simple_interaction_sexurm <- glm(news_count_gt_1 ~ urm_10 + female_10 +urm_10:female_10 +
                                               main_prof_pm_10 +
                                               main_prof_ph_10 +
                                               main_prof_celebrity_10 +
                                               main_prof_journalist_10 +
                                               main_prof_ie_10  +
                                               main_prof_practitioner_10,
                                             data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt1_simple_interaction_sexurm)
confint.default(log_reg_gt1_simple_interaction_sexurm)
cor(log_reg_gt1_simple_interaction_sexurm$fitted.values, news_cnt_df_nothey_available$news_count_gt_1)

# Simple - Inreraction sex/URM - Reach
log_reg_gt1_simple_interaction_sexurm_reach <- glm(news_count_gt_1 ~ urm_10 + female_10 +urm_10:female_10 +
                                               reach_prof_pm_10 +
                                               reach_prof_ph_10 +
                                               reach_prof_celebrity_10 +
                                               reach_prof_journalist_10 +
                                               reach_prof_ie_10  +
                                               reach_prof_practitioner_10,
                                             data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt1_simple_interaction_sexurm_reach)
confint.default(log_reg_gt1_simple_interaction_sexurm_reach)
cor(log_reg_gt1_simple_interaction_sexurm_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_1)

# Simple - Inreraction sex/URM - Collapse
log_reg_gt1_simple_interaction_sexurm_collapse <- glm(news_count_gt_1 ~ urm_10 + female_10 +urm_10:female_10 +
                                          main_prof_pm_10 +
                                          main_prof_ph_10 +
                                          main_prof_celebrity_journalist_ie_10 +
                                          main_prof_practitioner_10,
                                        data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt1_simple_interaction_sexurm_collapse)
confint.default(log_reg_gt1_simple_interaction_sexurm_collapse)
cor(log_reg_gt1_simple_interaction_sexurm_collapse$fitted.values, news_cnt_df_nothey_available$news_count_gt_1)

# Simple - Inreraction sex/URM - Collapse - Reach
log_reg_gt1_simple_interaction_sexurm_collapse_reach <- glm(news_count_gt_1 ~ urm_10 + female_10 +urm_10:female_10 +
                                                        reach_prof_pm_10 +
                                                        reach_prof_ph_10 +
                                                        reach_prof_celebrity_journalist_ie_10 +
                                                        reach_prof_practitioner_10,
                                                      data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt1_simple_interaction_sexurm_collapse_reach)
confint.default(log_reg_gt1_simple_interaction_sexurm_collapse_reach)
cor(log_reg_gt1_simple_interaction_sexurm_collapse_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_1)


# Simple - Interaction sex/professional affiliations
log_reg_gt1_simple_interaction_sexprof <- glm(news_count_gt_1 ~ urm_10 + female_10 +
                                         main_prof_pm_10 +
                                         main_prof_ph_10 +
                                         main_prof_celebrity_10 +
                                         main_prof_journalist_10 +
                                         main_prof_ie_10 +
                                         main_prof_practitioner_10 + 
                                           female_10:main_prof_pm_10 + 
                                           female_10:main_prof_ph_10 +
                                           female_10:main_prof_practitioner_10,
                                       data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt1_simple_interaction_sexprof)
confint.default(log_reg_gt1_simple_interaction_sexprof)
cor(log_reg_gt1_simple_interaction_sexprof$fitted.values, news_cnt_df_nothey_available$news_count_gt_1)

# Simple - Interaction sex/professional affiliations - Reach
log_reg_gt1_simple_interaction_sexprof_reach <- glm(news_count_gt_1 ~ urm_10 + female_10 +
                                                reach_prof_pm_10 +
                                                reach_prof_ph_10 +
                                                reach_prof_celebrity_10 +
                                                reach_prof_journalist_10 +
                                                reach_prof_ie_10 +
                                                reach_prof_practitioner_10 + 
                                                female_10:reach_prof_pm_10 + 
                                                female_10:reach_prof_ph_10 +
                                                female_10:reach_prof_practitioner_10,
                                              data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt1_simple_interaction_sexprof_reach)
confint.default(log_reg_gt1_simple_interaction_sexprof_reach)
cor(log_reg_gt1_simple_interaction_sexprof_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_1)

# Simple - Interaction sex/professional affiliations - Collapse
log_reg_gt1_simple_interaction_sexprof_collapse <- glm(news_count_gt_1 ~ urm_10 + female_10 +
                                                main_prof_pm_10 +
                                                main_prof_ph_10 +
                                                main_prof_celebrity_journalist_ie_10 +
                                                main_prof_practitioner_10 + 
                                                female_10:main_prof_pm_10 + 
                                                female_10:main_prof_ph_10 +
                                                female_10:main_prof_practitioner_10,
                                              data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt1_simple_interaction_sexprof_collapse)
confint.default(log_reg_gt1_simple_interaction_sexprof_collapse)
cor(log_reg_gt1_simple_interaction_sexprof_collapse$fitted.values, news_cnt_df_nothey_available$news_count_gt_1)

# Simple - Interaction sex/professional affiliations - Collapse - Reach
log_reg_gt1_simple_interaction_sexprof_collapse_reach <- glm(news_count_gt_1 ~ urm_10 + female_10 +
                                                         reach_prof_pm_10 +
                                                         reach_prof_ph_10 +
                                                         reach_prof_celebrity_journalist_ie_10 +
                                                         reach_prof_practitioner_10 + 
                                                         female_10:reach_prof_pm_10 + 
                                                         female_10:reach_prof_ph_10 +
                                                         female_10:reach_prof_practitioner_10,
                                                       data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt1_simple_interaction_sexprof_collapse_reach)
confint.default(log_reg_gt1_simple_interaction_sexprof_collapse_reach)
cor(log_reg_gt1_simple_interaction_sexprof_collapse_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_1)

# Simple - Interaction URM/professional affiliations
log_reg_gt1_simple_interaction_urmprof <- glm(news_count_gt_1 ~ urm_10 + female_10 +
                                                main_prof_pm_10 +
                                                main_prof_ph_10 +
                                                main_prof_celebrity_10 +
                                                main_prof_journalist_10 +
                                                main_prof_ie_10 +
                                                main_prof_practitioner_10 + 
                                               urm_10:main_prof_pm_10 + 
                                               urm_10:main_prof_ph_10 +
                                               urm_10:main_prof_practitioner_10,
                                              data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt1_simple_interaction_urmprof)
confint.default(log_reg_gt1_simple_interaction_urmprof)
cor(log_reg_gt1_simple_interaction_urmprof$fitted.values, news_cnt_df_nothey_available$news_count_gt_1)

# Simple - Interaction URM/professional affiliations
log_reg_gt1_simple_interaction_urmprof_reach <- glm(news_count_gt_1 ~ urm_10 + female_10 +
                                                reach_prof_pm_10 +
                                                reach_prof_ph_10 +
                                                reach_prof_celebrity_10 +
                                                reach_prof_journalist_10 +
                                                reach_prof_ie_10 +
                                                reach_prof_practitioner_10 + 
                                                urm_10:reach_prof_pm_10 + 
                                                urm_10:reach_prof_ph_10 +
                                                urm_10:reach_prof_practitioner_10,
                                              data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt1_simple_interaction_urmprof_reach)
confint.default(log_reg_gt1_simple_interaction_urmprof_reach)
cor(log_reg_gt1_simple_interaction_urmprof_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_1)

# Simple - Interaction URM/professional affiliations - Collapse
log_reg_gt1_simple_interaction_urmprof_collapse <- glm(news_count_gt_1 ~ urm_10 + female_10 +
                                                main_prof_pm_10 +
                                                main_prof_ph_10 +
                                                main_prof_celebrity_journalist_ie_10 +
                                                main_prof_practitioner_10 + 
                                                urm_10:main_prof_pm_10 + 
                                                urm_10:main_prof_ph_10 +
                                                urm_10:main_prof_practitioner_10,
                                              data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt1_simple_interaction_urmprof_collapse)
confint.default(log_reg_gt1_simple_interaction_urmprof_collapse)
cor(log_reg_gt1_simple_interaction_urmprof_collapse$fitted.values, news_cnt_df_nothey_available$news_count_gt_1)

# Simple - Interaction URM/professional affiliations - Collapse - Reach
log_reg_gt1_simple_interaction_urmprof_collapse_reach <- glm(news_count_gt_1 ~ urm_10 + female_10 +
                                                         reach_prof_pm_10 +
                                                         reach_prof_ph_10 +
                                                         reach_prof_celebrity_journalist_ie_10 +
                                                         reach_prof_practitioner_10 + 
                                                         urm_10:reach_prof_pm_10 + 
                                                         urm_10:reach_prof_ph_10 +
                                                         urm_10:reach_prof_practitioner_10,
                                                       data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt1_simple_interaction_urmprof_collapse_reach)
confint.default(log_reg_gt1_simple_interaction_urmprof_collapse_reach)
cor(log_reg_gt1_simple_interaction_urmprof_collapse_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_1)


# Same model but without the race/gender and profession interactions
log_reg_gt1_interaction1 <- glm(news_count_gt_1 ~  non_urm_she + urm_or_they + 
                                  policymaker_10 +  
                                  public_health_researcher_10 +
                                  practitioner_10 + 
                                  #non_public_health_researcher_10 +
                                  industry_expert_10 + 
                                  celebrity_10 + 
                                  journalist_10 +
                                  # professional interactions
                                  policymaker_ph + ph_practitioner, 
                                data = news_cnt_df, family = "binomial")
summary(log_reg_gt1_interaction1)
confint.default(log_reg_gt1_interaction1)

cor(log_reg_gt1_interaction1$fitted.values, news_cnt_df$news_count_gt_1)

# Same model but without any type of interactions 
log_reg_gt1_nointeraction <- glm(news_count_gt_1 ~  non_urm_she + urm_or_they + 
                                  policymaker_10 +  
                                  public_health_researcher_10 +
                                  practitioner_10 + 
                                  #non_public_health_researcher_10 +
                                  industry_expert_10 + 
                                  celebrity_10 + 
                                  journalist_10, 
                                data = news_cnt_df, family = "binomial")
summary(log_reg_gt1_nointeraction)
confint.default(log_reg_gt1_nointeraction)

cor(log_reg_gt1_nointeraction$fitted.values, news_cnt_df$news_count_gt_1)

## Collapse 1 ##

# Model with (1) interactions between two professions and (2) interactions between race/gender and profession
# > 1
# industry expert OR celebrity, journalist kept separate
log_reg_collapse1_gt1_interaction2 <- glm(news_count_gt_1 ~ non_urm_she + urm_or_they +  
                     public_health_researcher_10 +
                     practitioner_10 + 
                     policymaker_10 +
                     indexpert_celebrity_10 + 
                     journalist_10 +
                       # professional interactions
                       policymaker_ph + ph_practitioner +
                       # race/gender and profession
                       non_urm_she_ph + 
                       non_urm_she_policymaker + 
                       urm_or_they_ph + 
                       urm_or_they_policymaker, data = news_cnt_df, family = "binomial")
summary(log_reg_collapse1_gt1_interaction2)
confint.default(log_reg_collapse1_gt1_interaction2)

cor(log_reg_collapse1_gt1_interaction2$fitted.values, news_cnt_df$news_count_gt_1)

# Same model but without the race/gender and profession interactions
log_reg_collapse1_gt1_interaction1 <- glm(news_count_gt_1 ~ non_urm_she + urm_or_they +  
                                            public_health_researcher_10 +
                                            practitioner_10 + 
                                            policymaker_10 +
                                            indexpert_celebrity_10 + 
                                            journalist_10 +
                                            # professional interactions
                                            policymaker_ph + ph_practitioner, 
                                          data = news_cnt_df, family = "binomial")
summary(log_reg_collapse1_gt1_interaction1)
confint.default(log_reg_collapse1_gt1_interaction1)

cor(log_reg_collapse1_gt1_interaction1$fitted.values, news_cnt_df$news_count_gt_1)


# Same model but without any type of interactions 
log_reg_collapse1_gt1_nointeraction <- glm(news_count_gt_1 ~ non_urm_she + urm_or_they + 
                                            public_health_researcher_10 +
                                            practitioner_10 + 
                                            policymaker_10 +
                                            indexpert_celebrity_10 + 
                                            journalist_10, 
                                          data = news_cnt_df, family = "binomial")
summary(log_reg_collapse1_gt1_nointeraction)
confint.default(log_reg_collapse1_gt1_nointeraction)

cor(log_reg_collapse1_gt1_nointeraction$fitted.values, news_cnt_df$news_count_gt_1)


# Notes from meeting
# TV news: journalist not celebrities
# Look at the interaction between public health researcher/practitioner

## Collapse 2 ## 

# Model with (1) interactions between two professions and (2) interactions between race/gender and profession
# > 1
# industry expert OR celebrity OR journalist
log_reg_collapse2_gt1_interaction2 <- glm(news_count_gt_1 ~ non_urm_she + urm_or_they + 
                               public_health_researcher_10 +
                               practitioner_10 + 
                               policymaker_10 +
                               indexpert_celebrity_journalist_10 +
                               # professional interactions
                               policymaker_ph + ph_practitioner +
                               # race/gender and profession
                               non_urm_she_ph + 
                               non_urm_she_policymaker +
                               urm_or_they_ph + 
                               urm_or_they_policymaker,
                             data = news_cnt_df, family = "binomial")
summary(log_reg_collapse2_gt1_interaction2)
confint.default(log_reg_collapse2_gt1_interaction2)

cor(log_reg_collapse2_gt1_interaction2$fitted.values, news_cnt_df$news_count_gt_1)


# Same model but without the race/gender and profession interactions
log_reg_collapse2_gt1_interaction1 <- glm(news_count_gt_1 ~ non_urm_she + urm_or_they + 
                                            public_health_researcher_10 +
                                            practitioner_10 + 
                                            policymaker_10 +
                                            indexpert_celebrity_journalist_10 +
                                            # professional interactions
                                            policymaker_ph + ph_practitioner,
                                          data = news_cnt_df, family = "binomial")
summary(log_reg_collapse2_gt1_interaction1)
confint.default(log_reg_collapse2_gt1_interaction1)

cor(log_reg_collapse2_gt1_interaction1$fitted.values, news_cnt_df$news_count_gt_1)

# Same model but without any type of interactions 
log_reg_collapse2_gt1_nointeraction <- glm(news_count_gt_1 ~ non_urm_she + urm_or_they + 
                                            public_health_researcher_10 +
                                            practitioner_10 + 
                                            policymaker_10 +
                                            indexpert_celebrity_journalist_10,
                                          data = news_cnt_df, family = "binomial")
summary(log_reg_collapse2_gt1_nointeraction)
confint.default(log_reg_collapse2_gt1_nointeraction)

cor(log_reg_collapse2_gt1_nointeraction$fitted.values, news_cnt_df$news_count_gt_1)

### Part 2: outcome = # of mentions > 2 ###

## No collapse ##

# Model with (1) interactions between two professions and (2) interactions between race/gender and profession
# > 2
# industry expert, celebrity, and journalist kept separate
log_reg_gt2_interaction2 <- glm(news_count_gt_2 ~ non_urm_she + urm_or_they + 
                     policymaker_10 +
                     public_health_researcher_10 +
                     practitioner_10 + 
                     industry_expert_10 + 
                     celebrity_10 + 
                     journalist_10 +
                     # professional interactions
                     policymaker_ph + ph_practitioner +
                     # race/gender and profession
                     non_urm_she_ph + 
                     non_urm_she_policymaker +
                     urm_or_they_ph + 
                     urm_or_they_policymaker, data = news_cnt_df, family = "binomial")
summary(log_reg_gt2_interaction2)
confint.default(log_reg_gt2_interaction2)

cor(log_reg_gt2_interaction2$fitted.values, news_cnt_df$news_count_gt_2)

# Simple - No interaction
log_reg_gt2_simple_nointeraction <- glm(news_count_gt_2 ~ urm_10 + female_10 + 
                                               main_prof_pm_10 +
                                               main_prof_ph_10 +
                                               main_prof_celebrity_10 +
                                               main_prof_journalist_10 +
                                               main_prof_ie_10 +
                                               main_prof_practitioner_10,
                                             data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt2_simple_nointeraction)
exp(coef(log_reg_gt2_simple_nointeraction))
confint.default(log_reg_gt2_simple_nointeraction)
cor(log_reg_gt2_simple_nointeraction$fitted.values, news_cnt_df_nothey_available$news_count_gt_2)
cor(log_reg_gt2_simple_nointeraction$fitted.values, news_cnt_df_nothey_available$news_count_gt_2,method='spearman')
cor(log_reg_gt2_simple_nointeraction$fitted.values, news_cnt_df_nothey_available$news_count_gt_2,method='kendall')
PseudoR2(log_reg_gt2_simple_nointeraction,c("AldrichNelson","Nagelkerke"))

# Simple - No interaction - Reach
log_reg_gt2_simple_nointeraction_reach <- glm(news_count_gt_2 ~ urm_10 + female_10 + 
                                          reach_prof_pm_10 +
                                          reach_prof_ph_10 +
                                          reach_prof_celebrity_10 +
                                          reach_prof_journalist_10 +
                                          reach_prof_ie_10 +
                                          reach_prof_practitioner_10,
                                        data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt2_simple_nointeraction_reach)
exp(coef(log_reg_gt2_simple_nointeraction_reach))
confint.default(log_reg_gt2_simple_nointeraction_reach)
cor(log_reg_gt2_simple_nointeraction_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_2)
cor(log_reg_gt2_simple_nointeraction_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_2,method='spearman')
cor(log_reg_gt2_simple_nointeraction_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_2,method='kendall')
PseudoR2(log_reg_gt2_simple_nointeraction_reach,c("AldrichNelson","Nagelkerke"))

# Simple - No interaction - Collapse
log_reg_gt2_simple_nointeraction_collapse <- glm(news_count_gt_2 ~ urm_10 + female_10 + 
                                          main_prof_pm_10 +
                                          main_prof_ph_10 +
                                          main_prof_celebrity_journalist_ie_10  +
                                          main_prof_practitioner_10,
                                        data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt2_simple_nointeraction_collapse)
exp(coef(log_reg_gt2_simple_nointeraction_collapse))
confint.default(log_reg_gt2_simple_nointeraction_collapse)
cor(log_reg_gt2_simple_nointeraction_collapse$fitted.values, news_cnt_df_nothey_available$news_count_gt_2)
cor(log_reg_gt2_simple_nointeraction_collapse$fitted.values, news_cnt_df_nothey_available$news_count_gt_2,method='spearman')
cor(log_reg_gt2_simple_nointeraction_collapse$fitted.values, news_cnt_df_nothey_available$news_count_gt_2,method='kendall')
PseudoR2(log_reg_gt2_simple_nointeraction_collapse,c("AldrichNelson","Nagelkerke"))

# Simple - No interaction - Collapse - Reach
log_reg_gt2_simple_nointeraction_collapse_reach <- glm(news_count_gt_2 ~ urm_10 + female_10 + 
                                                   reach_prof_pm_10 +
                                                   reach_prof_ph_10 +
                                                   reach_prof_celebrity_journalist_ie_10  +
                                                   reach_prof_practitioner_10,
                                                 data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt2_simple_nointeraction_collapse_reach)
exp(coef(log_reg_gt2_simple_nointeraction_collapse_reach))
confint.default(log_reg_gt2_simple_nointeraction_collapse_reach)
cor(log_reg_gt2_simple_nointeraction_collapse_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_2)
cor(log_reg_gt2_simple_nointeraction_collapse_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_2,method='spearman')
cor(log_reg_gt2_simple_nointeraction_collapse_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_2,method='kendall')
PseudoR2(log_reg_gt2_simple_nointeraction_collapse_reach,c("AldrichNelson","Nagelkerke"))


# Simple - Sex/URM
log_reg_gt2_simple_interaction_sexurm <- glm(news_count_gt_2 ~ urm_10 + female_10 + urm_10*female_10+
                                                main_prof_pm_10 +
                                                main_prof_ph_10 +
                                                main_prof_celebrity_10 +
                                                main_prof_journalist_10 +
                                                main_prof_ie_10 +
                                                main_prof_practitioner_10,
                                              data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt2_simple_interaction_sexurm)
confint.default(log_reg_gt2_simple_interaction_sexurm)
cor(log_reg_gt2_simple_interaction_sexurm$fitted.values, news_cnt_df_nothey_available$news_count_gt_2)

# Simple - Sex/URM - Reach
log_reg_gt2_simple_interaction_sexurm_reach <- glm(news_count_gt_2 ~ urm_10 + female_10 + urm_10*female_10+
                                               reach_prof_pm_10 +
                                               reach_prof_ph_10 +
                                               reach_prof_celebrity_10 +
                                               reach_prof_journalist_10 +
                                               reach_prof_ie_10 +
                                               reach_prof_practitioner_10,
                                             data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt2_simple_interaction_sexurm_reach)
confint.default(log_reg_gt2_simple_interaction_sexurm_reach)
cor(log_reg_gt2_simple_interaction_sexurm_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_2)


# Simple - Sex/URM - Collapse
log_reg_gt2_simple_interaction_sexurm_collapse <- glm(news_count_gt_2 ~ urm_10 + female_10 + urm_10*female_10+
                                               main_prof_pm_10 +
                                               main_prof_ph_10 +
                                               main_prof_celebrity_journalist_ie_10 +
                                               main_prof_practitioner_10,
                                             data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt2_simple_interaction_sexurm_collapse)
confint.default(log_reg_gt2_simple_interaction_sexurm_collapse)
cor(log_reg_gt2_simple_interaction_sexurm_collapse$fitted.values, news_cnt_df_nothey_available$news_count_gt_2)


# Simple - Sex/URM - Collapse - Reach
log_reg_gt2_simple_interaction_sexurm_collapse_reach <- glm(news_count_gt_2 ~ urm_10 + female_10 + urm_10*female_10+
                                                        reach_prof_pm_10 +
                                                        reach_prof_ph_10 +
                                                        reach_prof_celebrity_journalist_ie_10 +
                                                        reach_prof_practitioner_10,
                                                      data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt2_simple_interaction_sexurm_collapse_reach)
confint.default(log_reg_gt2_simple_interaction_sexurm_collapse_reach)
cor(log_reg_gt2_simple_interaction_sexurm_collapse_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_2)

# Simple - Sex/prof
log_reg_gt2_simple_interaction_sexprof <- glm(news_count_gt_2 ~ urm_10 + female_10 +
                                                main_prof_pm_10 +
                                                main_prof_ph_10 +
                                                main_prof_celebrity_10 +
                                                main_prof_journalist_10 +
                                                main_prof_ie_10 +
                                                main_prof_practitioner_10 + 
                                                female_10:main_prof_pm_10 + 
                                                female_10:main_prof_ph_10 +
                                                female_10:main_prof_practitioner_10,
                                              data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt2_simple_interaction_sexprof)
confint.default(log_reg_gt2_simple_interaction_sexprof)
cor(log_reg_gt2_simple_interaction_sexprof$fitted.values, news_cnt_df_nothey_available$news_count_gt_2)

# Simple - Sex/prof - Reach
log_reg_gt2_simple_interaction_sexprof_reach <- glm(news_count_gt_2 ~ urm_10 + female_10 +
                                                reach_prof_pm_10 +
                                                reach_prof_ph_10 +
                                                reach_prof_celebrity_10 +
                                                reach_prof_journalist_10 +
                                                reach_prof_ie_10 +
                                                reach_prof_practitioner_10 + 
                                                female_10:reach_prof_pm_10 + 
                                                female_10:reach_prof_ph_10 +
                                                female_10:reach_prof_practitioner_10,
                                              data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt2_simple_interaction_sexprof_reach)
confint.default(log_reg_gt2_simple_interaction_sexprof_reach)
cor(log_reg_gt2_simple_interaction_sexprof_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_2)


# Simple - Sex/prof - Collapse
log_reg_gt2_simple_interaction_sexprof_collapse <- glm(news_count_gt_2 ~ urm_10 + female_10 +
                                                main_prof_pm_10 +
                                                main_prof_ph_10 +
                                                main_prof_celebrity_journalist_ie_10  +
                                                main_prof_practitioner_10 + 
                                                female_10:main_prof_pm_10 + 
                                                female_10:main_prof_ph_10 +
                                                female_10:main_prof_practitioner_10,
                                              data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt2_simple_interaction_sexprof_collapse)
confint.default(log_reg_gt2_simple_interaction_sexprof_collapse)
cor(log_reg_gt2_simple_interaction_sexprof_collapse$fitted.values, news_cnt_df_nothey_available$news_count_gt_2)

# Simple - Sex/prof - Collapse - Reach
log_reg_gt2_simple_interaction_sexprof_collapse_reach <- glm(news_count_gt_2 ~ urm_10 + female_10 +
                                                         reach_prof_pm_10 +
                                                         reach_prof_ph_10 +
                                                         reach_prof_celebrity_journalist_ie_10  +
                                                         reach_prof_practitioner_10 + 
                                                         female_10:reach_prof_pm_10 + 
                                                         female_10:reach_prof_ph_10 +
                                                         female_10:reach_prof_practitioner_10,
                                                       data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt2_simple_interaction_sexprof_collapse_reach)
confint.default(log_reg_gt2_simple_interaction_sexprof_collapse_reach)
cor(log_reg_gt2_simple_interaction_sexprof_collapse_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_2)

# Simple - URM/prof
log_reg_gt2_simple_interaction_urmprof <- glm(news_count_gt_2 ~ urm_10 + female_10 +
                                                main_prof_pm_10 +
                                                main_prof_ph_10 +
                                                main_prof_celebrity_10 +
                                                main_prof_journalist_10 +
                                                main_prof_ie_10 +
                                                main_prof_practitioner_10 + 
                                                urm_10:main_prof_pm_10 + 
                                                urm_10:main_prof_ph_10 +
                                                urm_10:main_prof_practitioner_10,
                                              data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt2_simple_interaction_urmprof)
confint.default(log_reg_gt2_simple_interaction_urmprof)
cor(log_reg_gt2_simple_interaction_urmprof$fitted.values, news_cnt_df_nothey_available$news_count_gt_2)

# Simple - URM/prof - Reach
log_reg_gt2_simple_interaction_urmprof_reach <- glm(news_count_gt_2 ~ urm_10 + female_10 +
                                                reach_prof_pm_10 +
                                                reach_prof_ph_10 +
                                                reach_prof_celebrity_10 +
                                                reach_prof_journalist_10 +
                                                reach_prof_ie_10 +
                                                reach_prof_practitioner_10 + 
                                                urm_10:reach_prof_pm_10 + 
                                                urm_10:reach_prof_ph_10 +
                                                urm_10:reach_prof_practitioner_10,
                                              data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt2_simple_interaction_urmprof_reach)
confint.default(log_reg_gt2_simple_interaction_urmprof_reach)
cor(log_reg_gt2_simple_interaction_urmprof_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_2)


# Simple - URM/prof - Collapse
log_reg_gt2_simple_interaction_urmprof_collapse <- glm(news_count_gt_2 ~ urm_10 + female_10 +
                                                main_prof_pm_10 +
                                                main_prof_ph_10 +
                                                main_prof_celebrity_journalist_ie_10  +
                                                main_prof_practitioner_10 + 
                                                urm_10:main_prof_pm_10 + 
                                                urm_10:main_prof_ph_10 +
                                                urm_10:main_prof_practitioner_10,
                                              data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt2_simple_interaction_urmprof_collapse)
confint.default(log_reg_gt2_simple_interaction_urmprof_collapse)
cor(log_reg_gt2_simple_interaction_urmprof_collapse$fitted.values, news_cnt_df_nothey_available$news_count_gt_2)

# Simple - URM/prof - Collapse - Reach
log_reg_gt2_simple_interaction_urmprof_collapse_reach <- glm(news_count_gt_2 ~ urm_10 + female_10 +
                                                         main_prof_pm_10 +
                                                         main_prof_ph_10 +
                                                         main_prof_celebrity_journalist_ie_10  +
                                                         main_prof_practitioner_10 + 
                                                         urm_10:main_prof_pm_10 + 
                                                         urm_10:main_prof_ph_10 +
                                                         urm_10:main_prof_practitioner_10,
                                                       data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt2_simple_interaction_urmprof_collapse_reach)
confint.default(log_reg_gt2_simple_interaction_urmprof_collapse_reach)
cor(log_reg_gt2_simple_interaction_urmprof_collapse_reach$fitted.values, news_cnt_df_nothey_available$news_count_gt_2)





# Same model but without the race/gender and profession interactions
log_reg_gt2_interaction1 <- glm(news_count_gt_2 ~ non_urm_she + urm_or_they +  
                                  policymaker_10 +
                                  public_health_researcher_10 +
                                  practitioner_10 + 
                                  industry_expert_10 + 
                                  celebrity_10 + 
                                  journalist_10 +
                                  # professional interactions
                                  policymaker_ph + ph_practitioner, 
                                data = news_cnt_df, family = "binomial")
summary(log_reg_gt2_interaction1)
confint.default(log_reg_gt2_interaction1)

cor(log_reg_gt2_interaction1$fitted.values, news_cnt_df$news_count_gt_2)


# Same model but without any type of interactions
log_reg_gt2_nointeraction <- glm(news_count_gt_2 ~ non_urm_she + urm_or_they + 
                                   policymaker_10 +
                                  public_health_researcher_10 +
                                  practitioner_10 + 
                                  industry_expert_10 + 
                                  celebrity_10 + 
                                  journalist_10,
                                data = news_cnt_df, family = "binomial")
summary(log_reg_gt2_nointeraction)
confint.default(log_reg_gt2_nointeraction)

cor(log_reg_gt2_nointeraction$fitted.values, news_cnt_df$news_count_gt_2)


## Collapse 1 ##

# Model with (1) interactions between two professions and (2) interactions between race/gender and profession
# > 2
# industry expert OR celebrity, but journalist kept separate
log_reg_collapse1_gt2_interaction2 <- glm(news_count_gt_2 ~ non_urm_she + urm_or_they + 
                               policymaker_10 +
                               public_health_researcher_10 +
                               practitioner_10 + 
                               indexpert_celebrity_10 + 
                               journalist_10 +
                               # professional interactions
                               policymaker_ph + ph_practitioner +
                               # race/gender and profession
                               non_urm_she_ph + 
                               non_urm_she_policymaker +
                               urm_or_they_ph + 
                               urm_or_they_policymaker, data = news_cnt_df, family = "binomial")
summary(log_reg_collapse1_gt2_interaction2)
confint.default(log_reg_collapse1_gt2_interaction2)

cor(log_reg_collapse1_gt2_interaction2$fitted.values, news_cnt_df$news_count_gt_2)


# Same model but without the race/gender and profession interactions
log_reg_collapse1_gt2_interaction1 <- glm(news_count_gt_2 ~ non_urm_she + urm_or_they + 
                                            policymaker_10 +
                                            public_health_researcher_10 +
                                            practitioner_10 + 
                                            indexpert_celebrity_10 + 
                                            journalist_10 +
                                            # professional interactions
                                            policymaker_ph + ph_practitioner, 
                                          data = news_cnt_df, family = "binomial")
summary(log_reg_collapse1_gt2_interaction1)
confint.default(log_reg_collapse1_gt2_interaction1)

cor(log_reg_collapse1_gt2_interaction1$fitted.values, news_cnt_df$news_count_gt_2)


# Same model but without any type of interactions 
log_reg_collapse1_gt2_nointeraction <- glm(news_count_gt_2 ~ non_urm_she + urm_or_they + 
                                            policymaker_10 +
                                            public_health_researcher_10 +
                                            practitioner_10 + 
                                            indexpert_celebrity_10 + 
                                            journalist_10,
                                          data = news_cnt_df, family = "binomial")
summary(log_reg_collapse1_gt2_nointeraction)
confint.default(log_reg_collapse1_gt2_nointeraction)

cor(log_reg_collapse1_gt2_nointeraction$fitted.values, news_cnt_df$news_count_gt_2)


## Collapse 2 ##

# Model with (1) interactions between two professions and (2) interactions between race/gender and profession
# > 2
# industry expert OR celebrity OR journalist
log_reg_collapse2_gt2_interaction2 <- glm(news_count_gt_2 ~ non_urm_she + urm_or_they +
                               policymaker_10 +
                               public_health_researcher_10 +
                               practitioner_10 + 
                               indexpert_celebrity_journalist_10 +
                               # professional interactions
                               policymaker_ph + ph_practitioner +
                               # race/gender and profession
                               non_urm_she_ph + 
                               non_urm_she_policymaker +
                               urm_or_they_ph + 
                               urm_or_they_policymaker,
                             data = news_cnt_df, family = "binomial")
summary(log_reg_collapse2_gt2_interaction2)
confint.default(log_reg_collapse2_gt2_interaction1)

cor(log_reg_collapse2_gt2_interaction2$fitted.values, news_cnt_df$news_count_gt_2)


# Same model but without the race/gender and profession interactions
log_reg_collapse2_gt2_interaction1 <- glm(news_count_gt_2 ~ non_urm_she + urm_or_they +
                                            policymaker_10 +
                                            public_health_researcher_10 +
                                            practitioner_10 + 
                                            indexpert_celebrity_journalist_10 +
                                            # professional interactions
                                            policymaker_ph + ph_practitioner,data=news_cnt_df, family = "binomial")
summary(log_reg_collapse2_gt2_interaction1)
confint.default(log_reg_collapse2_gt2_interaction1)

cor(log_reg_collapse2_gt2_interaction1$fitted.values, news_cnt_df$news_count_gt_2)


# Same model but without any type of interactions
log_reg_collapse2_gt2_nointeraction <- glm(news_count_gt_2 ~ non_urm_she + urm_or_they +
                                            policymaker_10 +
                                            public_health_researcher_10 +
                                            practitioner_10 + 
                                            indexpert_celebrity_journalist_10, data=news_cnt_df,family = "binomial")
summary(log_reg_collapse2_gt2_nointeraction)
confint.default(log_reg_collapse2_gt2_nointeraction)

cor(log_reg_collapse2_gt2_nointeraction$fitted.values, news_cnt_df$news_count_gt_2)


quantile(news_cnt_df$news_count[news_cnt_df$non_urm_she == 1],probs=seq(0,1,0.025)) # [1-12]
quantile(news_cnt_df$news_count[news_cnt_df$urm_or_they == 1],probs=seq(0,1,0.025)) # [1-11]

quantile(news_cnt_df$news_count[news_cnt_df$public_health_researcher_10 == 1],probs=seq(0,1,0.025)) # [1-20]



m1 <- glm.nb(daysabs ~ math + prog, data = dat))

m3 <- glm(daysabs ~ math + prog, family = "poisson", data = dat)
pchisq(2 * (logLik(m1) - logLik(m3)), df = 1, lower.tail = FALSE)

(est <- cbind(Estimate = coef(m1), confint(m1)))

m3 <- glm(daysabs ~ math + prog, family = "poisson", data = dat)
pchisq(2 * (logLik(m1) - logLik(m3)), df = 1, lower.tail = FALSE)

#Below we will obtain the mean predicted number of events for values of math across its entire range for each level of prog and graph these.

newdata2 <- data.frame(
  math = rep(seq(from = min(dat$math), to = max(dat$math), length.out = 100), 3),
  prog = factor(rep(1:3, each = 100), levels = 1:3, labels =
                  levels(dat$prog)))

newdata2 <- cbind(newdata2, predict(m1, newdata2, type = "link", se.fit=TRUE))
newdata2 <- within(newdata2, {
  DaysAbsent <- exp(fit)
  LL <- exp(fit - 1.96 * se.fit)
  UL <- exp(fit + 1.96 * se.fit)
})

ggplot(newdata2, aes(math, DaysAbsent)) +
  geom_ribbon(aes(ymin = LL, ymax = UL, fill = prog), alpha = .25) +
  geom_line(aes(colour = prog), size = 2) +
  labs(x = "Math Score", y = "Predicted Days Absent")


"fitdistr" (delignette - French)
function(lambda,x)
{
  exp(-lambda*x)
}

# ANOVA model

# matching process 

# intersectional profiles

# Female, non urm, public health researcher & practitioner
dim(news_cnt_df[news_cnt_df$public_health_researcher_10 == 1 & news_cnt_df$practitioner_10 == 1 & news_cnt_df$non_urm_she == 1,])
dim(news_cnt_df[news_cnt_df$celebrity_10 == 1 & news_cnt_df$urm == "No" & news_cnt_df$pronoun == "She",])
dim(news_cnt_df[news_cnt_df$celebrity_10 == 1 & news_cnt_df$urm == "Yes" & news_cnt_df$pronoun == "He",])
dim(news_cnt_df[news_cnt_df$industry_expert_10 == 1 & news_cnt_df$urm == "No" & news_cnt_df$pronoun == "She",])
dim(news_cnt_df[news_cnt_df$industry_expert_10 == 1 & news_cnt_df$urm == "Yes" & news_cnt_df$pronoun == "He",])
dim(news_cnt_df[news_cnt_df$journalist_10 == 1 & news_cnt_df$urm == "No" & news_cnt_df$pronoun == "She",])
dim(news_cnt_df[news_cnt_df$public_health_researcher_10 == 1 & news_cnt_df$practitioner_10 == 1 & news_cnt_df$pronoun == "He" & news_cnt_df$urm == "Yes",])
dim(news_cnt_df[news_cnt_df$journalist_10 == 1 & news_cnt_df$urm == "Yes" & news_cnt_df$pronoun == "He",])
dim(news_cnt_df[news_cnt_df$policymaker_10 == 1 & news_cnt_df$urm == "Yes" & news_cnt_df$pronoun == "He",])

dim(news_cnt_df[news_cnt_df$public_health_researcher_10 == 1 & news_cnt_df$pronoun == "She" & news_cnt_df$urm == "No",])
dim(news_cnt_df[news_cnt_df$policymaker_10 == 1 & news_cnt_df$public_health_researcher_10 == 1 & news_cnt_df$pronoun == "She" & news_cnt_df$urm == "No",])
dim(news_cnt_df[news_cnt_df$policymaker_10 == 1 & news_cnt_df$public_health_researcher_10 == 1 & news_cnt_df$pronoun == "He" & news_cnt_df$urm == "Yes",])
dim(news_cnt_df[news_cnt_df$celebrity_10 == 1 & news_cnt_df$pronoun == "He" & news_cnt_df$urm == "No",])
dim(news_cnt_df[news_cnt_df$policymaker_10 == 1 & news_cnt_df$pronoun == "She" & news_cnt_df$urm == "No",])
dim(news_cnt_df[news_cnt_df$practitioner_10 == 1 & news_cnt_df$pronoun == "She" & news_cnt_df$urm == "No",])
dim(news_cnt_df[news_cnt_df$practitioner_10 == 1 & news_cnt_df$pronoun == "He" & news_cnt_df$urm == "Yes",])
dim(news_cnt_df[news_cnt_df$industry_expert_10 == 1 & news_cnt_df$pronoun == "He" & news_cnt_df$urm == "No",])
dim(news_cnt_df[news_cnt_df$public_health_researcher_10 == 1 & news_cnt_df$pronoun == "He" & news_cnt_df$urm == "Yes",])
dim(news_cnt_df[news_cnt_df$journalist_10 == 1 & news_cnt_df$pronoun == "He" & news_cnt_df$urm == "No",])
dim(news_cnt_df[news_cnt_df$public_health_researcher_10 == 1 & news_cnt_df$practitioner_10 == 1 & news_cnt_df$pronoun == "He" & news_cnt_df$urm == "No",])

dim(news_cnt_df[news_cnt_df$policymaker_10 == 1 & news_cnt_df$pronoun == "He" & news_cnt_df$urm == "No",])
dim(news_cnt_df[news_cnt_df$practitioner_10 == 1 & news_cnt_df$pronoun == "He" & news_cnt_df$urm == "No",])
dim(news_cnt_df[news_cnt_df$public_health_researcher_10 == 1 & news_cnt_df$pronoun == "He" & news_cnt_df$urm == "No",])
dim(news_cnt_df[news_cnt_df$policymaker_10 == 1 & news_cnt_df$public_health_researcher_10 == 1 & news_cnt_df$pronoun == "He" & news_cnt_df$urm == "No",])

# non public health researcher
dim(news_cnt_df[news_cnt_df$non_public_health_researcher_10 == 1,]) # 917
# policymaker
dim(news_cnt_df[news_cnt_df$non_public_health_researcher_10 == 1 & news_cnt_df$policymaker_10 == 1,]) # 181
# practitioner
dim(news_cnt_df[news_cnt_df$non_public_health_researcher_10 == 1 & news_cnt_df$practitioner_10 == 1,]) # 37
# celebrity
dim(news_cnt_df[news_cnt_df$non_public_health_researcher_10 == 1 & news_cnt_df$celebrity_10 == 1,]) # 6
# journalist
dim(news_cnt_df[news_cnt_df$non_public_health_researcher_10 == 1 & news_cnt_df$journalist_10 == 1,]) # 38
# industry expert
# public health researcher


# Exclusive profiles

# Should we exclude "they/them" and "not_available"?

# Relative expertise
table(news_cnt_df$expertise_label_by_relative_expertise)
table(news_cnt_df$expertise_label_by_relative_reach)

# Non-public health researcher and something else
dim(news_cnt_df[news_cnt_df$non_public_health_researcher_10 == 1,]) # 917
table(news_cnt_df[news_cnt_df$non_public_health_researcher_10 == 1,"policymaker_10"]) # 181
table(news_cnt_df[news_cnt_df$non_public_health_researcher_10 == 1,"celebrity_10"]) # 6
table(news_cnt_df[news_cnt_df$non_public_health_researcher_10 == 1,"journalist_10"]) # 38
table(news_cnt_df[news_cnt_df$non_public_health_researcher_10 == 1,"industry_expert_10"]) # 193
table(news_cnt_df[news_cnt_df$non_public_health_researcher_10 == 1,"practitioner_10"]) # 37
# Sum: 455

# Non-public health researcher and nothing else
dim(news_cnt_df[news_cnt_df$non_public_health_researcher_10 == 1 & news_cnt_df$journalist_10 == 1 & news_cnt_df$policymaker_10 == 0 & news_cnt_df$industry_expert_10 == 0 & news_cnt_df$practitioner_10 == 0,])
# 21

# Journalist and something else
dim(news_cnt_df[news_cnt_df$journalist_10 == 1,]) # 334
table(news_cnt_df[news_cnt_df$journalist_10 == 1,"policymaker_10"]) # 44
table(news_cnt_df[news_cnt_df$journalist_10 == 1,"celebrity_10"]) # 17
table(news_cnt_df[news_cnt_df$journalist_10 == 1,"industry_expert_10"]) # 42
table(news_cnt_df[news_cnt_df$journalist_10 == 1,"practitioner_10"]) # 31
table(news_cnt_df[news_cnt_df$journalist_10 == 1,"public_health_researcher_10"]) # 35
# Sum: 169

# Journalist and nothing else
dim(news_cnt_df[news_cnt_df$journalist_10 == 1 & news_cnt_df$policymaker_10 == 0 & news_cnt_df$industry_expert_10 == 0 & news_cnt_df$practitioner_10 == 0 & news_cnt_df$public_health_researcher_10 == 0,])
# 234


# Practitioner and something else


# Practitioner and nothing else

# Celebrity and nothing else
# Policymaker and nothing else
# Non-public health researcher and nothing else
# Industry expert and nothing else

write.csv(news_cnt_df,"C:/Users/Utilisateur/Documents/2021.12.05.news_expert_characteristics.csv",row.names=FALSE)


# Simple - No interaction - Collapse
log_reg_gt1_sanity_check_collapse <- glm(news_count_gt_1 ~ urm_10 + female_10 + 
                                                   public_health_researcher_10 +
                                                   practitioner_10 +
                                                   policymaker_10  +
                                                   indexpert_celebrity_journalist_10,
                                                 data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt1_sanity_check_collapse)

log_reg_gt1_sanity_check_no_collapse <- glm(news_count_gt_1 ~ urm_10 + female_10 + 
                                           public_health_researcher_10 +
                                           practitioner_10 +
                                           policymaker_10  +
                                           industry_expert_10 +
                                           celebrity_10 +
                                           journalist_10,
                                         data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt1_sanity_check_no_collapse)

log_reg_gt2_sanity_check_collapse <- glm(news_count_gt_2 ~ urm_10 + female_10 + 
                                           public_health_researcher_10 +
                                           practitioner_10 +
                                           policymaker_10  +
                                           indexpert_celebrity_journalist_10,
                                         data=news_cnt_df_nothey_available, family="binomial")
summary(log_reg_gt2_sanity_check_collapse)


