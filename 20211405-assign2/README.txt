----PROGRAM ENVIRONMENT----

All the programs are written in python3 using ANACONDA IDE.
To execute the program the machine should have python3 and all the requred libraries.

The required libraries inlcude
1. pandas
2. requests
3. csv
4. json
5. OrderedDict from collections
6. datetime
7. timedelta from datetime
8. math

For Scripting purpose I have used Ubuntu Terminal available for download from Microsoft Store.
Ubuntu on Windows allow to use Ubuntu Terminal and run Ubuntu command line utilities including bash,
ssh, git, etc.

For writing the script I have used nano editor and I have called the .py files within each script to
execite the program.

The panda library for python has been download for scripting using the following set of commands in sequence
$ sudo add-apt-repository universe
$ sudo apt-get update
$ sudo apt-get install python3-pandas 

----PROGRAMS----

standard error of the distribution of the difference in two independent sample proportions
for hypothesis test is calculated as follows:

SE(p1-p2) = sqrt( ( P_pool(1-P_pool)/n1 ) + ( P_pool(1-P_pool)/n2 ) )
P_pool = overall proportion
P_pool = (Group1 success + Group 2 sucess)/ Total Population
n1 and n2 are Population in Group1 and Group2 respectively

Null hypothesis is p1-p2 = 0
Hypothesis test performed are two tailed hypothesis test.



Question1:-

The required files are present inside folder named "Question1"


The input files for the programs are
1. census_data.csv
2. DDW-C18-0000.csv

The program produce 3 output file which are
1. percent-india-a
2. percent-india-b

To execute the program run the "percent-india.sh" file

Question2:-

The required files are present inside folder named "Question2"

The input files for the programs are
1. census_data.csv
2. DDW-C18-0000.csv

The ouput files for the programs are
1. gender-india-a.csv
2. gender-india-b.csv
3. gender-india-c.csv

When executed the program displays the output graph in edge list format

To execute the program run the "gender-india.sh" file

Question3:-

The required files are present inside folder named "Question3"

The input files for the programs are
1. census_data.csv
2. DDW-C18-0000.csv

The ouput files for the programs are
1. geography-india-a.csv
2. geography-india-b.csv
3. geography-india-c.csv

To execute the program run the "geography-india.sh" file

Question4:-

The required files are present inside folder named "Question4"

The input files for the programs are
1. census_data.xlsx
2. DDW-C18-0000.xlsx

The ouput files for the programs are
1. 3-to-2-ratio.csv
2. 2-to-1-ratio.csv

To execute the program run the "3-to-2-ratio.sh" file and "2-to-1-ratio.sh" file

Question5:-

The required files are present inside folder named "Question5"

The input files for the programs are
1. DDW-0000C-14.xlsx
2. DDW-C18-0000.xlsx

The ouput files for the programs are
1. age-india-a.csv
2. age-india-b.csv

To execute the program run the "age-india.sh" file

Question6:-

The required files are present inside folder named "Question6"

The input files for the programs are
1. DDW-0000C-08.xlsx
2. DDW-C19-0000.xlsx

The ouput files for the programs are
1. literacy-india-a.csv
2. literacy-india-b.csv

To execute the program run the "literacy-india.sh" file

Question7:-

The required files are present inside folder named "Question7"

The input files for the programs are
1. All "DDW-C17-0100-....." .xlsx files

The ouput files for the programs are
1. region-india-a.csv
2. region-india-b.csv

To execute the program run the "region-india.sh" file

Question8:-

The required files are present inside folder named "Question8"

The input files for the programs are
1. DDW-0000C-14.xlsx
2. DDW-C18-0000.xlsx

The ouput files for the programs are
1. age-gender-a.csv
2. age-gender-b.csv
3. age-gender-c.csv


To execute the program run the "age-gender.sh" file

Question9:-

The required files are present inside folder named "Question9"

The input files for the programs are
1. DDW-0000C-08.xlsx
2. DDW-C19-0000.xlsx

The ouput files for the programs are
1. literacy-gender-a.csv
2. literacy-gender-b.csv
3. literacy-gender-c.csv

To execute the program run the "literacy-gender.sh" file

Question10:-

All the programs and their dependencies are included in folder named "Question10"
This folder contain all the programs described above.
A top-level script "assign2.sh" that runs the entire assignment i.e execute all the programs sequentially.




