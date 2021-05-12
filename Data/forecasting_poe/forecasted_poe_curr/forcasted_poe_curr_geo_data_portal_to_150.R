#This script loads a geo data portal climate file of historical climate and randomly assigns years to future climate for current climate only.  
#The ouput format of this script is the output of Amelia. 
#File structure:  You need to stip the first couple rows of the data in excel before running this and rename first columns with eco# like "1MEAN(degreesC)"
#Note directory that file is being written to and from.
#make sure to "mean" temp, and "sum" precip
#This script takes NA values and remove the entire rows they come from.

GCM<-"current"#only use this script for current climate, a1fi, or b1.
climate_variable<-"precip"

number_of_years_of_data<-31
dir<-setwd("J:/ClimateChangeData/MI_climate_change_data/MI_hayhoe_data/")
input_file<-paste("MI_9_",GCM,"_",climate_variable,".csv",sep="")
dta<-read.csv(input_file) #This is the input file changed by above


dta[is.na(dta)]<-NA  #Names no data values "NA"
dta <- dta[!is.na(dta[,2:6]),] #This damn line took me all day to figure out. It simply removes rows with NA.

eco_cli_parameter1<-dta[,2]
eco_cli_parameter2<-dta[,3]
eco_cli_parameter3<-dta[,4]
eco_cli_parameter4<-dta[,5]
eco_cli_parameter5<-dta[,6]
eco_cli_parameter6<-dta[,7]
eco_cli_parameter7<-dta[,8]
eco_cli_parameter8<-dta[,9]
eco_cli_parameter9<-dta[,10]


day<-dta[,1]
d2 <- as.POSIXlt(day)  # Note lt not ct
m_year <- d2$year + 1900 # year as a four digit integer
month <- d2$mon + 1  # month as we normally think of it
m <- (d2$year -100) * 12 + month  # months since jan 2000   # this gives you a unique integer for each month in your dataset starting with 1.
year_random<-tapply(m_year,m,mean)
ym <- paste(year_random, month, sep="-") # this gives you a unique yyyy-mm for each month in your dataset

jdayc<-c(15,46,76,107,137,168,198,229,259,290,321,351)
jday<-rep(jdayc,number_of_years_of_data)



###########################USE this below for temperature.
#e_1_cli_par<-tapply(eco_cli_parameter1 ,m, mean)
#e_2_cli_par<-tapply(eco_cli_parameter2 ,m, mean)
#e_3_cli_par<-tapply(eco_cli_parameter3 ,m, mean)
#e_4_cli_par<-tapply(eco_cli_parameter4 ,m, mean)
#e_5_cli_par<-tapply(eco_cli_parameter5 ,m, mean)
#e_6_cli_par<-tapply(eco_cli_parameter6 ,m, mean)
#e_7_cli_par<-tapply(eco_cli_parameter7 ,m, mean)
#e_8_cli_par<-tapply(eco_cli_parameter8 ,m, mean)
#e_9_cli_par<-tapply(eco_cli_parameter9 ,m, mean)


#####################USE this below for precipitation. 
e_1_cli_par<-tapply(eco_cli_parameter1 ,m, sum)*(0.1) ###0.1 (to convert from mm to cm)
e_2_cli_par<-tapply(eco_cli_parameter2 ,m, sum)*(0.1)
e_3_cli_par<-tapply(eco_cli_parameter3 ,m, sum)*(0.1)
e_4_cli_par<-tapply(eco_cli_parameter4 ,m, sum)*(0.1)
e_5_cli_par<-tapply(eco_cli_parameter5 ,m, sum)*(0.1)
e_6_cli_par<-tapply(eco_cli_parameter6 ,m, sum)*(0.1)
e_7_cli_par<-tapply(eco_cli_parameter7 ,m, sum)*(0.1)
e_8_cli_par<-tapply(eco_cli_parameter8 ,m, sum)*(0.1)
e_9_cli_par<-tapply(eco_cli_parameter9 ,m, sum)*(0.1)

cli_par<-cbind(year_random,jday,e_1_cli_par,e_2_cli_par,e_3_cli_par,e_4_cli_par,e_5_cli_par,e_6_cli_par,e_7_cli_par,e_8_cli_par,e_9_cli_par)

#to build the random year table--ONLY TO BE USED ONCE.
#rand_years_list<-NULL#clear the random list matrix.
#for (j in 0:149){#for all 150 years.
#  future_year<-(2000+j)#define the future year.
#  rand_year<-sample(cli_par[1,1]:cli_par[372,1],1)#randomly choose a sample year from all the historical climate data.  
#  rand_and_future<-cbind(future_year,rand_year)#bind the future year to the random year.
#  rand_years_list<-rbind(rand_years_list,rand_and_future)#bind the matrix together.
#  }
#  write.csv(rand_years_list,file="random_year_list.csv",row.names = F)#write the random year cross walk to file.

#to use the final random table build only once per set of climate variables...
final_random_cross_walk<-read.csv("random_year_list_final.csv")#read the final random year cross walk.
f_year_matrix<-NULL#clear the future year matrix.
for (i in 0:149){#for 150 future years
  year<-rep(2000+i,12)#define the future year.
  sub<-subset(cli_par,cli_par[,1]==final_random_cross_walk[i+1,2])#select the data from that sample year  
  f_year_row<-cbind(year,sub)#bind the future year with the data from the historical year.
  f_year_matrix<-rbind(f_year_matrix,f_year_row)#bind the data from this loop with all the loops.
  }
head(f_year_matrix)

out_file<-paste("J:/amelia/outputs/Michigan/",GCM,"_",climate_variable,".csv",sep="")
write.csv(f_year_matrix, file = out_file, row.names=FALSE)
