#check my output file "My_output.ass"


#importing re module for regular expression
#and string module for string manipulation

import re
import string 

def process_ass(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:  #opening the input file in read mode with UTF-8 encoding
        lines = f.readlines() #reads all the lines from input file into a list called 'lines'

    dialogues = [] #initializing an empty list called dialogues to store dialogue lines

    # Extract dialogues and maintain the non-event sections
    for line in lines: #iterates over the each line in lines
        if line.startswith("Dialogue:"): #if line starts with dialogue append the line to the dialogue list
            dialogues.append(line) 

    # Prepare the new events section
    new_events = [] #initializing list of new_events for storing modified dialogue
    for i in range(len(dialogues)):   #iterates over indices of the dialogue list
        if dialogues[i].startswith("Dialogue:"):
            NumberOfWords = getLine(dialogues[i])  #to get number of words in current dialogue
            currentTime = getTime(dialogues[i]) #to get start and end time of the current dialogue
            
            # Add the previous line with updated time
            if (i - NumberOfWords) >= 0: #if there is previous line or dialogue 
                new_events.append(replaceTime(currentTime, changeStyle(dialogues[i - NumberOfWords], 'P'))) # need to change the style of previous line P and replace previous line time with current dialogue time
            else: #if there does not exist the previous line append the below dialogue 
                new_events.append(replaceTime(currentTime, "Dialogue: 0,0:00:00.00,0:00:1.00,P,,0,0,0,,...")) 
            
            # Add the current dialogue line
            new_events.append(dialogues[i])
            
            # Add the next line with updated time
            if (i + NumberOfWords) < len(dialogues): #if there exists the next line or dialogue 
                new_events.append(replaceTime(currentTime, changeStyle(dialogues[i + NumberOfWords], 'F'))) #need to change the style of previous line F and replace previous line time with current dialogue time
            else: #if there does not exist the next line or dialogue append the below dialogue 
                new_events.append(replaceTime(currentTime, "Dialogue: 0,0:00:00.00,0:00:1.00,F,,0,0,0,,..."))

        
            
            new_events.append("\n") #Appending a newline character to new_events

    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f: #Opens the output file in write mode with UTF-8 encoding
        for line in lines: #iterates over each line in lines list
            if line.startswith("Dialogue:"): #checks if line starts with Dialogue
                break  # stop writing when encountering the first Dialogue line
            f.write(line)  #write non dialogue lines 
        for line in new_events: #iterate over each line in "new_events"
            f.write(line.strip() + '\n') #write modified lines to the output file

def getLine(dialogue):
    splitDialog = dialogue.split(",,")[-1]  #splits the dialogue by ",,"and gets the last part 
    splitString = re.sub(r'\{[^}]*\}', '', splitDialog) #remove text within curly braces using regular expression
    noOfWords = sum([i.strip(string.punctuation).isalpha() for i in splitString.split()]) #Counts the number of words that contain alphabetic characters
    return noOfWords #returns the number of words in line 

def getTime(dialogue):
    splitTime = dialogue.split(",")[1] #Split the dialogue line by commas and get the second element (start time)
    splitTimeEnd = dialogue.split(",")[2] #Get the third element (end time)
    return [splitTime, splitTimeEnd] #returns a list containing the start and end times

def replaceTime(newTime, dialogue):
    arrayDiag = dialogue.split(",") #Split the dialogue line by commas into a list
    arrayDiag[1] = newTime[0] #Replaces the start time with the new start time
    arrayDiag[2] = newTime[1] #Replaces the end time with the new end time
    return ",".join(arrayDiag) # Join's the list back into a string and return it

def changeStyle(dialogue, new_style):
    parts = dialogue.split(",") # Split's dialogue into parts by commas
    parts[3] = new_style # Set's the 4th element (style) to the new style
    dialogue_text = ",".join(parts) # Join's the parts back into a comma-separated string
    dialogue_text = re.sub(r'\{[^}]*\}', '', dialogue_text)  # Remove's curly braces
    return dialogue_text  # Return's the updated dialogue


input_file = 'input_subtitles.ass'  # Change of input file path
output_file = 'My_output.ass'  # Change of output file path
process_ass(input_file, output_file)
