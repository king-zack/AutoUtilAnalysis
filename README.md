# AR-PF

UCONN IAC AutoUtilAnalysis
Written by -- Zachary King; Max Nelson

This program was created to change the workflow of performing a utility analysis. It takes the itemized bill section of a utility bill and converts it into a csv which can easily be opened as a spreadsheet

Pytesseract is the driving library behind this program. After testing, it was found to be the most consistent of the image to text libraries as well as having the most indepth documentation

This program will eventually be expanded to support windows and mac. Additional testing may be needed for different utility bill formats. Eventually, the non-automated steps plan to be automated and the final version of this program will ba able to automatically perform a utility analysis if given the bills.

How to Use:

As of now, a folder must be created within the same directory as the program. In the folder, place screenshots of only the itemized section of the bill. It is paramount that these screenshots only contain this section and nothing more. 

Once these images are inputted into the folder, simply run the program. This will generate an output.csv file which can be read and adapted to a spreadhseet.

KNOWN ISSUES:

- Due to ink damage on a bill, the program may detect a character incorrectly. This is moreso a problem with letters than with numbers, but a total check feature will be implemented in the future.
