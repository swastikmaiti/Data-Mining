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

Question1:-

The required files are present inside folder named "Question1"

There must exist Internet connection to execute the program as it require covid dataset which is accessed via
api with following link "https://data.covid19india.org/v4/min/data.min.json"

The input files for the programs are
1. cowin_vaccine_data_districtwise.csv
2. neighbor-districts.json

The program produce 3 output file which are
1. neighbor-districts-modified.json which is the required output files as per the question requirement
2. neighbor-districts-modified2.json which is used by subsequent programs to compare districts names
3. distric_ids.csv which is used by subsequent programs to obtain district id of a ditrict

To execute the program run the "question1.sh" file

Question2:-

The required files are present inside folder named "Question2"

The input files for the programs are
1. neighbor-districts-modified.json which is obtained from Question1

The ouput files for the programs are
1. edge-graph.csv

When executed the program displays the output graph in edge list format

To execute the program run the "edge-generator.sh" file

Question3:-

The required files are present inside folder named "Question3"

The input files for the programs are
1. distric_ids.csv
2. districts.csv
3. neighbor-districts-modified2.json

The ouput files for the programs are
1. weekly-cases-time.csv
2. monthly-cases-time.csv
3. overall-cases-time.csv

To execute the program run the "case-generator.sh" file

Question4:-

The required files are present inside folder named "Question4"

The input files for the programs are
1. distric_ids.csv
2. districts.csv
3. neighbor-districts-modified2.json

The ouput files for the programs are
1. district_peaks.csv
2. state_peaks.csv
3. overall_peaks.csv

The week id in output files are the week number starting from 1 at which the peaks occurs
whereas the month id is the actual month(1 to 12 range) at which the peaks occurs.
The first week ends at 2020-03-21 which is Saturday  and second week ends at 2020-03-25 which
is Wednesady

To execute the program run the "peak-generator.sh" file

Question5:-

The required files are present inside folder named "Question5"

The input files for the programs are
1. cowin_vaccine_data_districtwise.csv

The ouput files for the programs are
1. weekly_district_vaccinated-count-time.csv
2. monthly_district_vaccinated-count-time.csv
3. overall_district_vaccinated-count-time.csv
4. weekly_state_vaccinated-count-time.csv
5. monthly_state_vaccinated-count-time.csv
6. overall_state_vaccinated-count-time.csv

To execute the program run the "vaccinated-count-generator.sh" file

Question6:-

The required files are present inside folder named "Question6"

The input files for the programs are
1. cowin_vaccine_data_districtwise.csv
2. census_data.csv

The ouput files for the programs are
1. district_vaccination-population-ratio.csv
2. state_vaccination-population-ratio.csv
3. overall_vaccination-population-ratio.csv

To execute the program run the "vaccine-population-ratio-generator.sh" file

Question7:-

The required files are present inside folder named "Question7"

The input files for the programs are
1. cowin_vaccine_data_districtwise.csv

The ouput files for the programs are
1. district_vaccine-type-ratio.csv
2. state_vaccine-type-ratio.csv
3. overall_vaccine-type-ratio.csv

To execute the program run the "vaccine-type-ratio-generator.sh" file

Question8:-

The required files are present inside folder named "Question8"

The input files for the programs are
1. cowin_vaccine_data_districtwise.csv
2. census_data.csv

The ouput files for the programs are
1. district_vaccinated-dose-ratio.csv
2. state_vaccinated-dose-ratio.csv
3. overall_vaccinated-dose-ratio.csv

To execute the program run the "vaccinated-ratio-generator.sh" file

Question9:-

The required files are present inside folder named "Question9"

The input files for the programs are
1. cowin_vaccine_data_districtwise.csv
2. census_data.csv

The ouput files for the programs are
1. complete-vaccination.csv

To execute the program run the "complete-vaccination-generator.sh" file

Question10:-

All the programs and their dependencies are included in folder named "Run_ALL"
This folder contain all the programs described above.
A top-level script "assign1.sh" that runs the entire assignment i.e execute all the programs sequentially.

There must exist Internet connection to execute the program as it require covid dataset which is accessed via
api with following link "https://data.covid19india.org/v4/min/data.min.json"

The input files for the programs are
1. cowin_vaccine_data_districtwise.csv
2. census_data.csv
3. districts.csv
4. neighbor-districts.json



