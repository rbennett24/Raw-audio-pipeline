######################################
# Packages
######################################
library(tidyverse)
library(stringr)
library(ragg)
library(vroom)

######################################
# Set working directory
######################################
computer = "Tiamat"

setwd(paste0("C:/Users/",computer,"/Dropbox/GIT/Raw_audio_pipeline/Raw-audio-pipeline/spanish/mfa_aligned/")) # Where files are stored.

outDir<-paste0("C:/Users/",computer,"/Dropbox/GIT/Raw_audio_pipeline/Raw-audio-pipeline/spanish/") # Where files are saved.

######################################
# Choose a colorblind friendly palette
######################################
colorSetCB=palette.colors(n = 8,palette = "R4")
colorSet<-colorSetCB[c(1,2,4,3,8,6)]

showColor<-function(pal){
  
  hist(seq(0,length(pal)),col=pal,breaks=length(pal))
  
}

# Check color schemes if desired.
# showColor(colorSetCB)
# showColor(colorSet)


######################################
# Read in data
######################################

######################################
# Compare FastTrak data to the hand-extracted formant data.
######################################
fasttrack.formants <- vroom("./fasttrack.csv") %>% select(c(F1,F2,F3,
                                                                   F1_s,F2_s,F3_s, # Smoothed formant values
                                                                   time,
                                                                   file_name,id,group,
                                                                   label))

# Make non-numeric columns factors
fasttrack.formants <- fasttrack.formants %>% mutate_at(c("file_name","id","group","label"),as.factor)
fasttrack.formants <- fasttrack.formants %>% rename("phone" = "label")
fasttrack.formants

# Read in .TextGrid info, and merge
fasttrack.formants.tg <- vroom("./fasttrack_TextGrid_data.csv") %>% mutate_all(as.factor)

summary(fasttrack.formants$phone) # Just vowel intervals
summary(fasttrack.formants.tg$phone) # All intervals

summary(subset(fasttrack.formants,!(id %in% unique(fasttrack.formants.tg$id)))) # No missing IDs

# Left join formant measurements
fasttrack.formants <- left_join(fasttrack.formants,fasttrack.formants.tg)
rm(fasttrack.formants.tg)


################
# Add normalized time
fasttrack.formants <- fasttrack.formants %>% group_by(id) %>% mutate(step = ((time-min(time))/(max(time)-min(time))*100))

save(file="FastTrack_formant_data.Rdata",fasttrack.formants)


######################################
# We decide to use the smoothed formant values.
fasttrack.formants <- fasttrack.formants %>% select(-c(F1,F2,F3)) %>% # Drop raw formants
                      pivot_longer(c(F1_s,F2_s,F3_s),
                                   names_to = "formant.smoothed",
                                   values_to = "freq"
                                   )

fasttrack.formants <- fasttrack.formants %>% mutate(formant.smoothed = case_match(formant.smoothed,"F1_s" ~ "F1","F2_s" ~ "F2","F3_s" ~ "F3"))


######################################
# Get some summary stats
######################################
formants <- fasttrack.formants
formants

formants %>% group_by(formant.smoothed) %>% summarize(mean=mean(freq,na.rm=T),
                                             median=median(freq,na.rm=T))

formants %>% group_by(phone,formant.smoothed) %>% summarize(mean=mean(freq,na.rm=T),
                                                  median=median(freq,na.rm=T))

# Get rid of vowel nasality
vnas <- "̃"
formants <- formants %>% mutate(phone = str_replace(phone,vnas,"")) %>% mutate(phone = factor(phone))
summary(formants$phone)

######################################
# Add some factors

formants$speaker <- str_split(formants$file_name,"_",simplify=T)[,1]
  
formants <- formants %>% mutate_at(c("speaker"),as.factor)

formants <- formants %>% pivot_wider(names_from = formant.smoothed,values_from=freq)
formants <- formants %>% mutate(F1.norm=F1/F3,
                                F2.norm=F2/F3)
formants

# Take average values over middle 10%
midpoints <- formants %>% group_by(speaker,phone) %>% filter(step >= 45 &  step <=55) %>% summarize_at(c("F1","F2","F3","F1.norm","F2.norm"),mean)
midpoints


formants.spk <- ggplot(data = midpoints) + 
  geom_label(aes(x=F2,y=F1,color=phone,label=phone),alpha=0.4)+
  scale_y_reverse(expand = expansion(mult = c(0.2, 0.2))) + # wider axis padding
  scale_x_reverse(expand = expansion(mult = c(0.1, 0.1))) + # wider axis padding
  theme_bw(base_size = 12)+
  theme(axis.text = element_text(size=12))+
  facet_wrap(.~speaker,ncol=3)+
  guides(color="none")+
  coord_fixed()


formants.spk


output_file<-paste0(outDir,"sample_formants_spanish.png")
agg_png(file=output_file,
        width=10,height=7,units="in",
        res=250)
  print(formants.spk)
dev.off()



# # Look at some trajectories
# raw.formants.spk<-ggplot(data = formants %>% filter(stress==1))+
#   geom_smooth(aes(x=step,y=F1.norm,color=speaker,group=speaker))+
#   scale_y_reverse()+
#   theme_bw(base_size = 24)+
#   theme(axis.text = element_text(size=12))+
#   facet_wrap(.~vqual)
# 
# raw.formants.spk
