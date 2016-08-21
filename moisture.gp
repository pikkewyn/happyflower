#set terminal pngcairo size 450,362 enhanced font 'Verdana,10'
set terminal png font 'Verdana,10'
set output "/home/janek/public_html/moisture.png"
#set grid
set grid y
set title "how dry is your flower"
set xlabel "time"
set ylabel "value"
set xdata time
set timefmt "%d-%m_%H:%M"
set xtics rotate by 45 offset -0.8,-1.8

plot  "/home/janek/moisture/moisture.log" using 1:2 notitle with lines
