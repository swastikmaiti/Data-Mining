
The required libraries inlcude
1. numpy
2. asarray from numpy
3. matplotlib.pyplot


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

The anomaly detection problem is approched using concept of Kth nearest neighbor. If the
distance of Kth nerest neighbor is greater than theshold distance hereby referred to as r, 
then the point is an outlier. To determine the hyperparemter "r" first all the Kth nerest
neighbor distances are calculated. Then the 95th percentile has been used as the value of r
since the expected number of outlier is around 5 percent. The value of k is taken as 4. 

The input to the Program are:
1. anomaly-s118.dat

The output files are
1. answer-s118.dat
2. answer-s118.txt

Execution:-

Makefile - Go to the folder location and run the command $ make
	   This will execute the program and produce the output files.



