from PIL import Image, ImageGrab
from pytesseract import pytesseract
import re
import pandas as pd

def is_number(n):
    try:
        int(n)
        return True
    except ValueError:
        return False
        
def cleanList(inputList):
    '''A function that simply takes an input list and cleans it to the desired specifications. This cleaning process includes removing empty items, combining lines separate by bills, and removing the subheaders in the itemized bill with no attached charge.'''
    
    #remove empty list items
    inputList = [i for i in inputList if i]
    outputList = []

    #Combine Lines separated by bill
    i = 0
    while i < len(inputList) - 1:
        if is_number(inputList[i+1][0]) or inputList[i+1][0] == '$':
            outputList.append(inputList[i] + ' ' + inputList[i+1])
            i += 2
        else:
            outputList.append(inputList[i])
            i += 1

    #Remove unnecessary subheaders
    outputList = [j for j in outputList if re.search(r'\d', j)]
    return outputList

def billToList(itemizedBill):
    '''Uses Pytesseract to convert the selected image to text; --psm refers to the strictness of the line formatting. with a value of 6, any text on the same horizontal line in the image will be considered to be on the same text line'''
    text = pytesseract.image_to_string(image_path, config='--psm 6')
    return text.splitlines()

def splitList(outputList):
    #split each item into Title, Rate, Charge
    structuredList = []
    index = None
    part1 = []
    part2 = []
    for i in outputList:
        for j, char in enumerate(i):
            if char == '$':
                index = j
                break
        if index is not None:
            part1 = i[:index]
            part2 = i[index:]

        index = None
        for k, char in enumerate(part1):
            if is_number(char) == True:
                index = k
                break
        if index is not None:
            part1a = part1[:index]
            part1b = part1[index:]
            structuredList.append([part1a, part1b, part2])  
        else:
            structuredList.append([part1, part2])
    return structuredList

def getTitles(structuredList):
    #get titles
    titles = []
    for i in structuredList:
        titles.append(i[0])
    return titles

def getCharges(structuredList):
    #get Charges
    charges = []
    for i in structuredList:
        charges.append(i[-1])
    return charges
    

################################################################################################################################

TitlesMasterList = []
ChargesMasterList = []

### DEFINE LARGE LOOP

for iter in range(15):

    image_path = r"ExampleBills/ExampleBill" + str(iter) + ".png"

    #input("Image being processed is: ExampleBill" + str(iter) + ".png")

    outputList = cleanList(billToList(image_path))

    structuredList = splitList(outputList)

    titles = getTitles(structuredList)

    charges = getCharges(structuredList)

    for i in titles:
        if i not in TitlesMasterList:
            TitlesMasterList.append(i)
            tempList = []
            for i in range(iter):
                tempList.append(0)
            ChargesMasterList.append(tempList)

    for ind, j in enumerate(TitlesMasterList):
        if j in titles:
            ChargesMasterList[ind].append(charges[titles.index(j)])
        else:
            ChargesMasterList[ind].append('0')


##Make DATAFRAME

data = {}

for ind, k in enumerate(TitlesMasterList):
    data[k] = ChargesMasterList[ind]

dataframe = pd.DataFrame(data)

print(dataframe)

dataframe.to_csv('Output.csv', index=False)
# Displaying the extracted text 
#print(structuredList)
#print()
#print(TitlesMasterList)
#print()
#print(ChargesMasterList)


###
### ARCHIVE
###

###################

#def extractText(clip):
#    text = pytesseract.image_to_string(img, config='--psm 6')
#    return text.splitlines()

###################

# Defining paths to tesseract.exe 
#path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

###################
# Opening the image & storing it in an image object 
#img = ImageGrab.grabclipboard()
  
# Providing the tesseract executable 
# location to pytesseract library 
#pytesseract.tesseract_cmd = path_to_tesseract 
