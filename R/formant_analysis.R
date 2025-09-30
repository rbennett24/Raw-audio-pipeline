
#####################
# NEED TO REGENERATE fasttrack.formants,
# AND MAKE SURE THAT THE PHONE AND STRESS COLUMNS ARE BEHAVING AS INTENDED.
#####################

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
formants.homebrewed <- read.csv("formant_tracks.txt",sep="\t") %>% as_tibble()
formants.homebrewed$phone <- formants.homebrewed$vowel.code
formants.homebrewed <- formants.homebrewed %>% select(-vowel.code)

######################################
# Compare FastTrak data to the hand-extracted formant data, and merge as desired.
######################################
fasttrack.formants <- vroom("./corpus/fasttrack.csv") %>% select(c(F1,F2,F3,
                                                                   F1_s,F2_s,F3_s, # Smoothed formant values
                                                                   time,
                                                                   file_name,id,group,
                                                                   label))
fasttrack.formants
formants.homebrewed


# This is time-intensive, so unless you want to actually work with the original CSV files for some reason, just load this:
# # load("FastTrack_formant_data.Rdata")
# 
# ################################################## #################################################
# #  Note that the dataframe which is loaded here (<formants>) includes the log-additive regression
# # normalized formant values as well.
# 
# formant.csv.files <- fs::dir_ls(path = "csvs/",glob="*.csv")
# csvs<-vroom(formant.csv.files,id="filename")
# csvs
# 
# csvs <- csvs %>% select(c(time,f1,f2,f3,filename))
# csvs <- csvs %>% mutate(file = sub(".csv","",filename))
# csvs <- csvs %>% mutate(file = sub("csvs/","",file)) %>% select(-c(filename))
# csvs
# 
# # Get interval code from file info CVS
# fileInfo <- vroom("file_information.csv")
# fileInfo
# 
# fileInfo <- fileInfo %>% mutate(file = gsub("([[:digit:]]_)*.wav$","",file))
# fileInfo
# 
# 
# fasttrack.formants <- left_join(csvs,(fileInfo %>% select(file,label,number)),by="file")
# fasttrack.formants$fileTMP <- fasttrack.formants$file
# fasttrack.formants <- fasttrack.formants %>% separate(fileTMP,into=c("speaker","filenum","vnum.infile"),sep="_") %>% select(-c(filenum,vnum.infile))
# 
# fasttrack.formants
# 
# 
# ################
# # Add normalized time
# fasttrack.formants <- fasttrack.formants %>% group_by(file) %>% mutate(step = ((time-min(time))/(max(time)-min(time))*100))
# 
# # Pivot longer
# fasttrack.formants <- fasttrack.formants %>% pivot_longer(cols=c(f1,f2,f3),names_to = "formant",values_to="freq")
# fasttrack.formants <- fasttrack.formants %>% mutate(formant = toupper(formant))
# fasttrack.formants
# 
# # Rename some columns
# fasttrack.formants$phone <- fasttrack.formants$label
# fasttrack.formants <- fasttrack.formants %>% select(-label)
# 
# fasttrack.formants$token.code <- fasttrack.formants$file
# fasttrack.formants <- fasttrack.formants %>% select(-file)
# 
# save(file="FastTrack_formant_data.Rdata",fasttrack.formants)
# 
# ################################################## #################################################
# 
# 
# fasttrack.formants


# Compare formant measurements across methods
nrow(fasttrack.formants)
nrow(formants.homebrewed)
qqplot(fasttrack.formants$freq,
       formants.homebrewed$freq)
 
# Use the Fast Track data:
formants <- fasttrack.formants
formants

###########################################################################


######################################
# Get some summary stats
######################################
formants %>% group_by(formant) %>% summarize(mean=mean(freq,na.rm=T),
                                             median=median(freq,na.rm=T))

formants %>% group_by(pone,formant) %>% summarize(mean=mean(freq,na.rm=T),
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

formants <- formants %>% mutate(vqual = factor(vqual),
                                stress = factor(stress),
                                speaker = factor(as.character(speaker)),
                                token.code = factor(token.code),
                                )

formants <- formants %>% pivot_wider(names_from = formant,values_from=freq)
formants <- formants %>% mutate(F1.norm=F1/F3,
                                F2.norm=F2/F3)

midpoints <- formants %>% filter(step == median(step,na.rm=T))
midpoints <- midpoints %>% group_by(speaker,vqual) %>% summarize_at(c("F1.norm","F2.norm","F1","F2","F3"),mean) # I powerfully do not understand why simple summarize() doesn't work here

midpoints.monop <- midpoints %>% filter(str_length(vqual)==1) # Monophthongs only

formants.spk<-ggplot(data = midpoints.monop) + 
  geom_label(aes(x=F2,y=F1,color=vqual,label=vqual),alpha=0.4)+
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


