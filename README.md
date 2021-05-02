# AI-project Loic Dehan, Karim Hako, Jorne Ceulemans

Tested on python 3.8.8, ubuntu 18.04 

# arguments: csv input, csv output, timelimit, randomseed, threads

python main.py ./csv/100_5_14_25.csv ./csv_solutions/100_5_14_25_solution.csv 300 81310 1

python main.py ./csv/100_5_19_25.csv ./csv_solutions/100_5_19_25_solution.csv 300 6410 1

python main.py ./csv/210_5_33_25.csv ./csv_solutions/210_5_33_25_solution.csv 300 848 1

python main.py ./csv/210_5_44_25.csv ./csv_solutions/210_5_44_25_solution.csv 300 1610 1

python main.py ./csv/360_5_71_25.csv ./csv_solutions/360_5_71_25_solution.csv 300 898512 1


java -jar validator.jar ./csv/100_5_14_25.csv ./csv_solutions/100_5_14_25_solution.csv

java -jar validator.jar ./csv/100_5_19_25.csv ./csv_solutions/100_5_19_25_solution.csv

java -jar validator.jar ./csv/210_5_33_25.csv ./csv_solutions/210_5_33_25_solution.csv

java -jar validator.jar ./csv/210_5_44_25.csv ./csv_solutions/210_5_44_25_solution.csv

java -jar validator.jar ./csv/360_5_71_25.csv ./csv_solutions/360_5_71_25_solution.csv
