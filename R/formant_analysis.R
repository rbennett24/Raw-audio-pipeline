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
computer = "510fu"

setwd(paste0("C:/Users/",computer,"/Dropbox/GIT/Raw_audio_pipeline/Raw-audio-pipeline/samples/mfa_aligned/")) # Where files are stored.

outDir<-paste0("C:/Users/",computer,"/Dropbox/GIT/Raw_audio_pipeline/Raw-audio-pipeline/samples/") # Where files are saved.

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

# # Formant measurements produced by a handmade script
# # Note that this does not include filenames or word-level coding right now.
# formants.homebrewed <- read.csv("formant_tracks.txt",sep="\t") %>% as_tibble()
# formants.homebrewed$phone <- formants.homebrewed$vowel.code
# formants.homebrewed <- formants.homebrewed %>% select(-vowel.code)


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


# ###########
# # Compare different formant measurement techniques
# 
# # Pivot wider to compare
# formants.homebrewed <- formants.homebrewed %>% pivot_wider(names_from = formant,values_from = freq)
# formants.homebrewed
# 
# fasttrack.formants
# 
# # Compare formant measurements across methods
# nrow(fasttrack.formants) # Many more measurements
# nrow(formants.homebrewed)
# 
# # Looks like FastTrack probably tracks F1 better
# qqplot(fasttrack.formants$F1,
#        formants.homebrewed$F1)
# 
# # F2 seems pretty comparable?
# qqplot(fasttrack.formants$F2,
#        formants.homebrewed$F2)
# 

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


######################################
# Add some factors
formants <- formants %>% mutate(vqual = substr(phone,1,2),
                                stress = substr(phone,3,3),
                                )

summary(factor(formants$stress))
summary(factor(formants$vqual))

formants <- formants %>% filter(stress > 0) # Primary/secondary stress

formants$vqual <- recode(formants$vqual,
                          "AA" = "ɑ",
                          "AE" = "æ",
                          "AH" = "ʌ",
                          "AO" = "ɔ",
                          "AY" = "a͡ɪ",
                          "EH" = "ɛ",
                          "ER" = "ɝ",
                          "EY" = "e͡ɪ",
                          "IH" = "ɪ",
                          "IY" = "i",
                          "OW" = "o͡ʊ",
                          "OY" = "ɔ͡ɪ",
                          "UH" = "ʊ",
                          "UW" = "i"
                          )

formants$speaker <- str_split(formants$file_name,"_",simplify=T)[,1]
  
formants <- formants %>% mutate_at(c("vqual","stress","speaker"),as.factor)

formants <- formants %>% pivot_wider(names_from = formant.smoothed,values_from=freq)
formants <- formants %>% mutate(F1.norm=F1/F3,
                                F2.norm=F2/F3)
formants


# Take average values over middle 10%
midpoints <- formants %>% group_by(speaker,vqual) %>% filter(step >= 45 &  step <=55) %>% summarize_at(c("F1","F2","F3","F1.norm","F2.norm"),mean)
midpoints


midpoints.monop <- midpoints %>% filter(str_length(vqual)==1) # Monophthongs only

formants.spk <- ggplot(data = midpoints.monop) + 
  geom_label(aes(x=F2,y=F1,color=vqual,label=vqual),alpha=0.4)+
  scale_y_reverse(expand = expansion(mult = c(0.2, 0.2))) + # wider axis padding
  scale_x_reverse(expand = expansion(mult = c(0.1, 0.1))) + # wider axis padding
  theme_bw(base_size = 12)+
  theme(axis.text = element_text(size=12))+
  facet_wrap(.~speaker,ncol=3)+
  guides(color="none")+
  coord_fixed()

# formants.spk


output_file<-paste0(outDir,"sample_formants.png")
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


