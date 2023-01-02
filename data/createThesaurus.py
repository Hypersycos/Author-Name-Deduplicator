import csv
import difflib

def checkDuplicates(file,retainLetters=True):
    with open(file, newline='',encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        copies = []
        lastNames = ["abcdefghijklmnopsampletext "]
        possibleTypos = []
        for row in reader:
            newString = ""
            for char in row[1]:
                if not char in "-":
                    newString = newString + char
            comparisonString = ""
            for char in lastNames[0]:
                if not char in "-":
                    comparisonString = comparisonString + char
            if compare(row[1],lastNames[0]) < 4:
                possibleTypos.append([row[1],lastNames[0]])
            if len(newString)>len(comparisonString):
                if newString[:len(comparisonString)] == comparisonString:
                    lastNames.append(row[1])
                    if possibleTypos[-1][0] == row[1]:
                        del possibleTypos[-1]
                else:
                    if len(lastNames)>1:
                        copies.append(lastNames)
                    lastNames = [row[1]]
            else:
                if comparisonString[:len(newString)] == newString:
                    lastNames.insert(0,row[1])
                    if len(possibleTypos)>0 and possibleTypos[-1][0] == row[1]:
                        del possibleTypos[-1]
                else:
                    if len(lastNames)>1:
                        copies.append(lastNames)
                    lastNames = [row[1]]
        if len(lastNames)>1:
            copies.append(lastNames)
        print(str(len(possibleTypos))+" possible typos found.\n")
        i = 1
        for item in possibleTypos:
            print(str(i)+": Is "+item[0]+" the same as "+item[1]+"?")
            i += 1
        print("\nIf you wish to apply corrections, type the number of each correction followed by a comma (e.g. '5,8')")
        print("Otherwise, just press enter")
        Input = input()
        corrections = []
        new = ""
        for char in Input:
            if char == ",":
                corrections.append(new)
                new = ""
            else:
                if not char == " ":
                    new = new + char
        if not new == "":
            corrections.append(new)
        for i in range(0,len(corrections)):
            corrections[i] = int(corrections[i])-1
        for i in range(len(possibleTypos)-1,-1,-1):
            if not i in corrections:
                del possibleTypos[i]
        for item in possibleTypos:
            done = False
            for destination in copies:
                if item[1] in destination:
                    destination.append(item[0])
                    done = True
                    break
                elif item[0] in destination:
                    destination.append(item[1])
                    done = True
                    break
            if not done:
                copies.append(item)
        saveFile(copies,"thesaurus_authors_new.txt")
        print("\nNew file 'thesaurus_authors_new.txt' created!")

def saveFile(thing,name):
    with open(name,'w',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter = '\t')
        writer.writerow(["label","replace by"])
        for item in thing:
            for label in item:
                if not item[0] == label:
                    writer.writerow([label,item[0]])

def compare(item1,item2):
    return sum([i[0] != ' '  for i in difflib.ndiff(item1, item2)]) 

print("Enter file name (including extension, e.g. '.txt.')")
checkDuplicates(input())
