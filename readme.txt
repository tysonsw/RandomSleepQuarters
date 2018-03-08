This program was created for a larp to help decide who gets to sleep where.
The roomrandomizer.py has been created to be run with python 3.

The program takes only csv files that are seperated by ; and is in latin text.

The csv files can have columns in any order but the columns containing the needs of the participants 
must be in the same order for the roomoutline file.
The csv file must then contain an "x" (small x without quotation marks)in the column for the need that the participant has.

For example:
If the participant file has the following structure:
Name,Address,E-mail,Need poweroutlet, has child.

Then the roomoutline file must have "Need poweroutlet" and "Has child" in the same order. There can be other columns between them but the order they appear must be the same.

The example files provided has for example people working with Media.
In the participant file these have x for their Need column Media.
In the roomoutline file the Barracks has been decided that there is the only place media people can only sleep.
So when the program checks the need of the participant and finds an x in the need for Media, 
they will then be assigned to the Barracks since these are the only ones that meet that need.

The files can have any name, you tell the program what the name is of your files.
