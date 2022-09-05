
The required libraries inlcude
1. pandas
2. csv
3. OrderedDict from collections
4. collections
5. Counter from collections
6. numpy
7. sys

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

The classification problem is approached using Decision Tree(Monothetic) structure. To decide the split at
every node Information Gain is used as the measure of purity of daughter nodes. To prevent 
high variance the minimum size of leaf node is limited to 10 or dominant class proprtion is
atleast 0.80, the depth of the tree is also limited to 20. The hyperparameter min leaf node size
of 10 is taken after performing validation test by splitting the data into tain and validation data
in the ratio 95:5

The training accuracy on the total dataset is 0.85. The total dataset is finally used for training as
the test data will be used separtely.

The input to the Program are:
1. training-s118.csv
2. test file (provided in command line while executing)

The output files are
1. classifier-s118.txt
2. classifier-s118.csv

Two different output files are produced due to ambuguity in the format to be used in output file.

Execution:-

Requirements:- The test files has to be present in the same folder. Go to th folder then

There are two executable file

1.Makefile :- run the following code

	      make file=<test-file-name> for example if the test file name is test-s118.csv
	      then execute as $ make file=test-s118

2.classifier-s118 :- run the following code
		    
		     ./classifier-s118.sh <test-file-name> or example if the test file name is test-s118.csv
	      	     then execute as $./classifier-s118.sh test-s118

Both the execution will produce the same results.



	      