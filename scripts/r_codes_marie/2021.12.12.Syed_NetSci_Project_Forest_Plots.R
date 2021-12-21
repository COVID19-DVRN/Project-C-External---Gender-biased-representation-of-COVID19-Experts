library(ggforce)


# overview

specifications <- rep(c("No collapse, No interaction", 
                        "Collapse Expert/Celebrity/Journalist, No interaction"), 6)
length(specifications)

variables <- c(rep("Intercept",2), 
               rep("Female",2), 
               rep("Minority",2), 
               rep("Public health researcher",2), 
               rep("Policymaker",2),
               rep("Practitioner",2))
length(variables)

# point estimates 
exp(coef(log_reg_gt1_simple_nointeraction))
exp(coef(log_reg_gt1_simple_nointeraction_collapse))
exp(coef(log_reg_gt2_simple_nointeraction))
exp(coef(log_reg_gt2_simple_nointeraction_collapse))

# outcome 1
estimates <- c( 0.4128905,0.4122966,
                0.7239488,0.7280486,
                0.9546392,0.9558731, 
                2.1650638,2.1636709,
                1.8112869,1.8114418, 
                1.7642301,1.7628785)
length(estimates)

# outcome 2
estimates_outcome2 <- c(0.1381314 ,0.1379551,
                        0.71986343,0.7243603,
                        0.8464285,0.8462960,
                        3.0446063,3.0428214,
                        2.4520205,2.4523964,
                        2.4731970,2.4717617)

# confidence intervals
exp(confint.default(log_reg_gt1_simple_nointeraction))
exp(confint.default(log_reg_gt1_simple_nointeraction_collapse))
exp(confint.default(log_reg_gt2_simple_nointeraction))
exp(confint.default(log_reg_gt2_simple_nointeraction_collapse))

# lower bound of 95% CI
ci_lower <- c( 0.3539241,  0.3534163,
               0.6318350, 0.6355073,
               0.8107880, 0.8120023, 
               1.8209607, 1.8198210,
               1.4104200, 1.4105653, 
               1.3996330, 1.3985947)
length(ci_lower)

ci_lower_2 <- c(0.1112818, 0.1111386,
                0.6109061, 0.6147918 ,
                0.6946672,  0.6946895, 
                2.4103401,  2.4089552,
                1.7903752, 1.7906733, 
                1.8401456, 1.8391111)
length(ci_lower_2)

# upper bound of 95% CI
ci_upper <- c(0.4816811, 0.4809865,
              0.8294917,  0.8340656,
              1.1240127, 1.1252350, 
              2.5741914, 2.5724902,
              2.3260875, 2.3262457, 
              2.2238030, 2.2220453)
length(ci_upper)

ci_upper_2 <- c(0.1714590, 0.1712419,
                0.8482536, 0.8534562,
                1.0313445,  1.0309886, 
                3.8457759, 3.8434763,
                3.3581814,3.3586519, 
                3.3240324, 3.3220429)
length(ci_upper_2)

ci_upper_2 <- c(0.1714590, 0.1712419,
                0.8482536, 0.8534562,
                1.0313445,  1.0309886, 
                3.8457759, 3.8434763,
                3.3581814,3.3586519, 
                3.3240324, 3.3220429)
length(ci_upper_2)

# concatenation
outcome1 <- rep("# mentions > 1",12)
outcome2 <- rep("# mentions > 2",12)

all_estimates <- cbind(specifications, variables, estimates, ci_lower, ci_upper, outcome1)
all_estimates <- as.data.frame(all_estimates)
names(all_estimates) <- c("specification","variable","estimate","ci_lower","ci_upper","outcome")

all_estimates_2 <- cbind(specifications, variables, estimates_outcome2, ci_lower_2, ci_upper_2, outcome2)
all_estimates_2 <- as.data.frame(all_estimates_2)
names(all_estimates_2) <- c("specification","variable","estimate","ci_lower","ci_upper","outcome")

all_estimates <- rbind(all_estimates,all_estimates_2)
dim(all_estimates)

all_estimates$estimate <- as.numeric(all_estimates$estimate)
all_estimates$ci_lower <- as.numeric(all_estimates$ci_lower)
all_estimates$ci_upper <- as.numeric(all_estimates$ci_upper)

# limits for plot
min(all_estimates$ci_lower) # outcome 1: 0.3534163 / outcome 2: 0.1111386
max(all_estimates$ci_upper) # outcome 1: 2.574191 / outcome 2: 3.845776

# ordering
all_estimates$specification <- factor(all_estimates$specification,levels=c("No collapse, No interaction",
                                                                           "Collapse Expert/Celebrity/Journalist, No interaction"))

all_estimates$variable <- factor(all_estimates$variable,levels=c("Practitioner",
                                                                 "Policymaker",
                                                                 "Public health researcher",
                                                                 "Minority",
                                                                 "Female",
                                                                 "Intercept"))

# generating corresponding PDF files

pdf(file = "No_collapse_no_interaction.pdf")
all_estimates_no_collapse_no_interaction <- all_estimates[all_estimates$specification == "No collapse, No interaction",]
all_estimates_no_collapse_no_interaction <- all_estimates_no_collapse_no_interaction[all_estimates_no_collapse_no_interaction$outcome == "# mentions > 1",]
p <- ggplot(all_estimates_no_collapse_no_interaction, aes(y = variable, x = estimate, label=estimate)) +
  geom_point(size = 4) +
  scale_x_continuous(limits = c(0.0, 4.0))+
  geom_errorbar(aes(xmax = ci_upper, xmin = ci_lower)) + 
  geom_vline(xintercept=1,col="blue") + 
  xlab("Odds Ratio") + 
  ylab("Variable") + 
  geom_label(size=3)
print(p)
dev.off()

pdf(file = "Collapse_no_interaction.pdf")
all_estimates_collapse_no_interaction <- all_estimates[all_estimates$specification == "Collapse Expert/Celebrity/Journalist, No interaction",]
all_estimates_collapse_no_interaction <- all_estimates_collapse_no_interaction[all_estimates_collapse_no_interaction$outcome == "# mentions > 1",]
p <- ggplot(all_estimates_collapse_no_interaction, aes(y = variable, x = estimate, label=estimate)) +
  geom_point(size = 4) +
  scale_x_continuous(limits = c(0.0, 4.0))+
  geom_errorbar(aes(xmax = ci_upper, xmin = ci_lower)) + 
  geom_vline(xintercept=1,col="blue") + 
  xlab("Odds Ratio") + 
  ylab("Variable") + 
  geom_label(size=3)
print(p)
dev.off()

pdf(file = "No_collapse_no_interaction_outcome2.pdf")
all_estimates_no_collapse_no_interaction <- all_estimates[all_estimates$specification == "No collapse, No interaction",]
all_estimates_no_collapse_no_interaction <- all_estimates_no_collapse_no_interaction[all_estimates_no_collapse_no_interaction$outcome == "# mentions > 2",]
p <- ggplot(all_estimates_no_collapse_no_interaction, aes(y = variable, x = estimate, label=estimate)) +
  geom_point(size = 4) +
  scale_x_continuous(limits = c(0.0, 4.0))+
  geom_errorbar(aes(xmax = ci_upper, xmin = ci_lower)) + 
  geom_vline(xintercept=1,col="blue") + 
  xlab("Odds Ratio") + 
  ylab("Variable") + 
  geom_label(size=3)
print(p)
dev.off()

pdf(file = "Collapse_no_interaction_outcome2.pdf")
all_estimates_collapse_no_interaction <- all_estimates[all_estimates$specification == "Collapse Expert/Celebrity/Journalist, No interaction",]
all_estimates_collapse_no_interaction <- all_estimates_collapse_no_interaction[all_estimates_collapse_no_interaction$outcome == "# mentions > 2",]

p <- ggplot(all_estimates_collapse_no_interaction, aes(y = variable, x = estimate, label=estimate)) +
  geom_point(size = 4) +
  scale_x_continuous(limits = c(0.0, 4.0))+
  geom_errorbar(aes(xmax = ci_upper, xmin = ci_lower)) + 
  geom_vline(xintercept=1,col="blue") + 
  xlab("Odds Ratio") + 
  ylab("Variable") + 
  geom_label(size=3)
print(p)
dev.off()