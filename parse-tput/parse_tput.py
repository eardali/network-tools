#!/usr/bin/python3

#---------README---------
#searches for *.txt, iperf result files and parses by regex
#outputs *.csv file (sec, tput)
#input file name is used as output file name, extension changed
#iperf result must be gathered by -P flag, it searches accordingly, [SUM] lines
#update iperf time interval per requirement, i variable
#creates a plot, time vs tput
#emrea, July 2021

import os
import re
import statistics
import matplotlib
import matplotlib.pyplot as plt

i = 1 #-i arg of iperf when getting result txt file

#tput_regex = "\[SUM\].+(?:(?:M|G)Bytes)+\s+(\d+.\d+).+(?:(?:M|G)bits\/sec)"
#tput_regex = "\[SUM\].+(?:(?:M|G)Bytes)+\s+(\d+.\d+).+(?:(?:M|G)bits\/sec\s+$)" 
tput_regex = r"\[SUM\].+(?:(?:M|G|)Bytes)+\s+(\d+.\d+).+(?:(?:M|G|)bits\/sec\s+(?:\d+|)\s+$)"
#use "$" to stop before any other string, hence avoid to catch result summary lines at the end
#update to catch in DL direction in which result followed by retry column (i think this happen in Linux versions of iperf3)

unit_regex = r"\[SUM\].+(?:(?:M|G|)Bytes)+\s+\d+.\d+.+(M|K)bits\/sec\s+(?:\d+|)\s+$"
#this is to catch if unit is bits/sec, or Kbits/sec or Mbits/sec, normally it should be Mbits/sec, however rarely it may occurs in other way, in this case calculate Mbits/sec

infile_ext = ".txt" #iperf results txt
outfile_ext = ".csv"
figfile_ext = ".png"

dirPath = os.path.dirname(os.path.realpath(__file__))


for fileName in os.listdir(dirPath):   
    hit = 0 #total regex hit
    K_hit = 0 #hit for non-M, Kbits/sec hits
    b_hit = 0 #hit for non-M, bits/sec hits
    if fileName.endswith(infile_ext):
        print("Parsing file: %s" % fileName)
        tput_results=[]
        file = open(os.path.join(dirPath,fileName), 'r')
        for line in file:
            result = re.findall(tput_regex, line)
            if result:
                hit = hit+1
                unit = re.findall(unit_regex, line)
                if unit:
                    if unit[0] == "M": #Mbits/sec, expected unit
                        tput_results.append(result[0].replace(".", ",")) #replace dot with coma, for excel calculations
                    else: #Kbits/sec
                        K_hit = K_hit+1
                        value = float(result[0])/1024 #these calculations introduce some error compared original iperf value, i couldn't figure out why?
                        tput_results.append(str(value).replace(".", ","))
                else: #no unit means bits/sec
                     b_hit = b_hit+1
                     value = float(result[0])/(1024*1024)
                     tput_results.append(str(value).replace(".", ","))
        
        file.close()
        print("Number of total hits: %s, Kbits/sec hits: %s, bits/sec hits: %s" %(hit, K_hit, b_hit))
        
        if not (hit==0 and K_hit==0 and b_hit==0):    
            #write results to csv file
            outfname = fileName.replace(infile_ext, outfile_ext)
            file = open(os.path.join(dirPath,outfname), 'w')        
            
            file.write(";;Results Count;%s;Kbps Count;%s;bps Count;%s\n" %(hit, K_hit, b_hit))
            file.write("sec;tput(Mbps);avr(Mbps);=average(B:B);min;=min(B:B);max;=max(B:B);stdev;=stdev.s(B:B)\n")
            sec = i
            secs = []
            for tput in tput_results:
                file.write("%s;%s\n" %(sec, tput))
                secs.append(sec)
                sec = sec + i
                    
            file.close()
            
            #plot figures and save
            figfname = fileName.replace(infile_ext, figfile_ext)
            figsizeX = 16
            figsizeY = 9
            #fig, [axs1, axs2, axs3] = plt.subplots(3)

            tput_results_f = [float(s.replace(',','.')) for s in tput_results] 
               
            fig, axs1 = plt.subplots(figsize=(figsizeX,figsizeY))
            
            #(min_val, max_val, avr_val) = (min(tput_results_f), max(tput_results_f), round(float(sum(tput_results_f))/len(tput_results_f),2))
            (min_val, max_val, avr_val, stdev_val) = (min(tput_results_f), max(tput_results_f), round(statistics.mean(tput_results_f),2), round(statistics.stdev(tput_results_f),2))
            stats = "(avg: %s, min: %s, max: %s, stdev: %s Mbps)"  %(avr_val, min_val, max_val, stdev_val)
            axs1.plot(secs, tput_results_f, 'b-', label = 'tput')
            #start, end = axs1.get_xlim()
            #axs1.xaxis.set_ticks(np.arange(start, end, 15))
            #axs1.tick_params(axis='x', labelsize=6, labelrotation=45)
            axs1.set(xlabel='time (s)', ylabel='Tput (Mbps)', title= figfname.replace(figfile_ext, ' ')+stats)
            axs1.set_ylim(ymin=0)
            axs1.grid()
            axs1.legend(fontsize=10)
            plt.tight_layout()

            fig_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),figfname)
            fig.savefig(fig_file)
            
            fig.clf()
            plt.close()
            
        else:
             print("Seems no hit in %s, may be collected without -P flag?" % fileName)