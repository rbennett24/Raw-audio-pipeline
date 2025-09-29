######################################
# Packages
######################################
library(tidyverse)
library(stringr)
library(ragg)

######################################
# Set working directory
######################################
computer = "Tiamat"

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

# Formant measurements produced by a handmade script:
formants.homebrewed <- read.csv("formant_tracks.txt",sep="\t")
formants <- formants.homebrewed

######################################
# Get some summary stats
######################################
formants %>% group_by(formant) %>% summarize(mean=mean(freq,na.rm=T),
                                             median=median(freq,na.rm=T))

formants %>% group_by(vowel.code,formant) %>% summarize(mean=mean(freq,na.rm=T),
                                             median=median(freq,na.rm=T))


######################################
# Add some factors

formants <- formants %>% mutate(vqual = substr(vowel.code,1,2),
                                stress = substr(vowel.code,3,3),
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

formants <- formants %>% mutate(vqual = factor(vqual),
                                stress = factor(stress),
                                speaker = factor(as.character(speaker)),
                                token.code = factor(token.code),
                                )

formants <- formants %>% pivot_wider(names_from = formant,values_from=freq)
formants <- formants %>% mutate(F1.norm=F1/F3,
                                  F2.norm=F2/F3)

midpoints <- formants %>% filter(step == median(step,na.rm=T))
midpoints <- midpoints %>% group_by(speaker,vqual) %>% summarize_at(c("F1.norm","F2.norm"),mean) # I powerfully do not understand why simple summarize() doesn't work here

midpoints.monop <- midpoints %>% filter(str_length(vqual)==1) # Monophthongs only

formants.spk<-ggplot(data = midpoints.monop) + 
  geom_label(aes(x=F2.norm,y=F1.norm,color=vqual,label=vqual),alpha=0.4)+
  scale_y_reverse()+
  scale_x_reverse()+
  theme_bw(base_size = 12)+
  theme(axis.text = element_text(size=12))+
  facet_wrap(.~speaker)+
  guides(color="none")

formants.spk


output_file<-paste0(outDir,"sample_formants.png")
agg_png(file=output_file,
        width=9,height=6,units="in",
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
