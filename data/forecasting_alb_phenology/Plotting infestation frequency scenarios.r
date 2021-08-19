installed.packages("extrafont")

library(ggplot2)
library(extrafont)
library(grid)

library(rstudioapi)
setwd(dirname(getActiveDocumentContext()$path))
getwd()

y1 <- read.csv(file = "infestation_frequency_curr.csv", header = TRUE, stringsAsFactors = FALSE)
y2 <- read.csv(file = "infestation_frequency_pcm.csv", header = TRUE, stringsAsFactors = FALSE)
y3 <- read.csv(file = "infestation_frequency_gfdl.csv", header = TRUE, stringsAsFactors = FALSE)

y1$month <- factor(y1$month, levels = y1$month)

tiff("infestation frequency scenarios.tiff", units="in", width=5, height=5, res=300)
ggplot() +
  geom_point(data = y1, aes(x = ecoregion, y = years, group=1, color="black")) +
  geom_line(data = y1, aes(x = ecoregion, y = years, group=1, color="black")) +
  geom_hline(yintercept=4.6, linetype="dashed", color = "black") +
  annotation_custom(textGrob("4.6", gp = gpar(col = "black")),xmin=0, xmax=0,ymin=4.6, ymax=4.6) +
  geom_point(data = y2, aes(x = ecoregion, y = years, group=1, color="orange")) +
  geom_line(data = y2, aes(x = ecoregion, y = years, group=1, color="orange")) +
  geom_hline(yintercept=3.9, linetype="dashed", color = "orange") +
  geom_point(data = y3, aes(x = ecoregion, y = years, group=1, color="red")) +  
  geom_line(data = y3, aes(x = ecoregion, y = years, group=1, color="red")) +
  labs(x ="Ecoregions", y = "Estimated infestation frequency (in years)") +
  scale_y_continuous(breaks= c(2, 2.5, 3.0, 3.5, 3.9, 4.0, 4.5, 4.6, 5.0, 5.5, 6.0)) + #seq(1,6,0.5)) +
  #ylim(2,6) +
  scale_color_identity(name = "Scenarios",
                       breaks = c("black", "orange", "red"),
                       labels = c("Currrent", "Warmer and wetter", "Hotter and drier"),
                       guide = "legend") +
  theme(panel.background = element_blank(),
        panel.grid.major = element_line(color="grey", size = (0.2)),
        #panel.grid.minor = element_line(color="grey", size = (0.2)),
        axis.text = element_text(family="Times New Roman"),
        axis.title.x = element_text(family="Times New Roman"),
        axis.title.y = element_text(family="Times New Roman"),
        legend.position = c(0.75, 0.25),
        legend.title = element_text(family="Times New Roman"),
        legend.text = element_text(family="Times New Roman"),
        legend.background = element_rect(color="white"),
        legend.key = element_blank(),
        axis.line = element_line(colour = "black"))
dev.off()
