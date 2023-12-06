import csv
import os
####################   TAKES HTML THAT IS FORMATTED IN A TABLE AND RETURNS A CSV   #####################
###  YOUR TXT FILE MUST BEGIN WITH AN HTML TAG, EXAMPLES: <TD>, <TR>, <TABLE>  ###

# this will remove any html elements from .txt file and return a .csv file
# also it will convert &amp; to a "&"
# this  SHOULD account for NULL values, it will create an empty string to append to the list

# you will need to have or create the "input" and "output" folders in the same folder as this code
# copy the html into a .txt file inside the input folder
# follow prompts in CLI



def html_to_csv():
    file_list = os.listdir("input")                                                        
    new_text = input(f"\n\nType file name from list to use: \n{file_list}\n\t")                 # lists the files that are in the input folder for easier selection by user
    file_name_check = True
    while file_name_check:                                                                      # this loop makes sure that file name typed exists in the input folder
        if file_list.count(new_text) > 0:
            file_name_check = False
        else:
            print("\n**********     FILE NOT IN 'input' FOLDER     **********")
            new_text = input(f"\n\nType file name from list to use: \n{file_list}\n\t")            
    num_fields = int(input("How many fields (columns) are there?\n\t"))                          # the number of columns will be used later during the writing phase of the csv file
    try:
        with open(("input/" + new_text), "r") as new_file:                                      # opens and reads the file converting the entirety to a string
            s = str(new_file.read())         
            remove_new_lines = s.replace('\n', ' ')                                              # removes any new line escape sequences
            remove_tabs = remove_new_lines.replace('\t',' ')                                     # removes any tab escape sequences
            listified = []                                                                       # this will be list of all words or NULL values to be entered into the csv
            word = ""                                                                            # holds the word to be added to listified
            discard = ""                                                                         # holds the characters that will be removed from the txt file  example:  <td>
            counter = 0                                                                          # used to create sub strings of s to help find NULL values
            for char in remove_tabs:                                                             # loop over all of the chars in the string - remove_tabs
                if char == "<":                                                                  # starts looking for starting character in an HTML tag
                    counter += 1                                                                 # increases counter 
                    if len(word) > 0:                                                            # checks for if a word has been assembled to add to the list
                        if "&amp;" in word:                                                      # looks for the HTML character reference for an ampersand and replaces it with the character "&" (other character references could be added)
                            fix_char = word.replace("&amp;", "&")                                # the replacement happens here
                            listified.append(fix_char)                                           # corrected string is added to listified
                        else:
                            listified.append(word)                                               # otherwise just the word needs to be appended to listified
                    #print(f"New Discard start\t\t{counter}\t{discard}\t{word}")
                    word = ""                                                                    # word gets reset
                    discard += char                                                              # the discard string starts being built
                elif len(discard) > 0 and char != ">":                                           # this is to build the discard string
                    counter += 1                                                                 # increases counter to be used as an index later
                    discard += char                                                              # adds current char to discard
                    #print(f"continue to discard\t\t{counter}\t{discard}\t{word}")
                elif char == ">" and word == "":                                                 # find the end of a discard string and checks for a NULL value 
                    counter += 1                                                                 # increass counter to be used as an index later
                    discard += char                                                              # adds current char to the discard string
                    sub_s = discard[:1] + "/" + discard[1:]                                      # creates the closing tag version of the discard string
                    sub_s_2 = remove_tabs[counter:counter + len(sub_s)]                          # finds the string in remove_tabs at the current counter and plus the length of sub_s
                    #print("Sub_s: ",sub_s,"\t\tSub_s_2: ",sub_s_2)
                    if sub_s == sub_s_2 and sub_s != "</tr>":                                    # checks for similarity of sub_s and sub_s_2 and makes sure that it isn't just an empty row in the table
                        listified.append("")                                                     # adds an empty string to listified, which can be translated to a NULL value by a DBMS
                    discard = ""                                                                 # discard gets reset
                    #print(f"End discard\t\t{counter}\t{discard}\t{word}")
                elif char == " " and word == "":                                                 # this will ignore blank spaces when building discard strings
                    counter += 1                                                                 # increments the counter
                    #print(f"Blank space between rows\t\t{counter}\t{discard}\t{word}")
                    continue                                                                     # continues the loop again
                elif discard == "" and counter > 0:                                              # checks if discard is empty and that this isn't the first character of the txt file
                    counter += 1                                                                 # increments counter
                    word += char                                                                 # builds the word that will be added to listified
                    #print(f"Building new word\t\t{counter}\t{discard}\t{word}")
                else:                                                                            # helps with diagnostics for why the program failed to parse the txt file
                    print(f'I ran {counter} times. Then I broke.')                               # can give you an idea of where the parser failed
                    return                                                                       # stops the loop
            for index in range(0,num_fields):                                                    # loops over the strings in listified that will become the column names
                listified[index] = listified[index].lower()                                      # changes the string to lower case
                listified[index] = listified[index].replace(" ", "_")                            # joins the words with an "_" to remove spaces
            #print(f"\n\n{listified}\n\n")
            print(f"html_to_csv parser ran {counter} times and is complete\n\n")                 # lets the user know the parser is finished
    except:                                                                                      # another exit point for the program is the file could not be found
        print("could not find the file")
        return        
    try:
        output_list = os.listdir("output")                                                                                                 # stores the list of files in "output"
        output_file_name = input(f"\n\n**********     CURRENT FILES IN 'output':\n\t{output_list}\n\nNew file name:\n\t")                  # prints the list of files in the "output" folder and asks for the file name you wish to be used
        new_file_check = True                                                                                                               # holds boolean value for the while loop
        while new_file_check:                                                                                                               # the loop checks the validity of the file name
            file_ext_check = output_file_name[-4:]                                                                                          # holds the last 4 characters of the file name that was input
            if file_ext_check != ".csv":                                                                                                    # checks for the .csv extension at the end of the file
                output_file_name = input("\nYou must use the '.csv' file extension. Re-type the filename:\n\t")                             # asks you to retype the file name if the file extension doesn't match
                continue                                                                                                                    # starts loop again
            if output_list.count(output_file_name) > 0:                                                                                     # checks if you have used a file name that already exists
                keep_name = input("\nThis will overwrite the old file.\nDo you wish to continue? (Y/N)\n\t")                                # you can choose to overwrite the file or type a new file name
                if keep_name.lower() == "y":                                                                                                # checks user input 
                    new_file_check = False                                                                                                  # if "y" the new_file_check is complete
                else:                                                                                                                       # if "n" or anything else 
                    output_file_name = input(f"\n\n**********     CURRENT FILES IN 'output':\n\t{output_list}\n\nNew file name:\n\t")      # this prompts user for a new file name
                    continue                                                                                                                # starts file name checker loop again
            else:                                                                                                                           # if the file name is new
                new_file_check = False                                                                                                      # sets new_file_check to False to end loop
        with open(("output/"+ output_file_name),"w") as f:                                                                                 # creates or opens a csv file of the name from output_file_name
            fields = []                                                                                                                     # stores the strings to be used as the column / field names
            for num in range(num_fields):                                                                                                   # loops over listified
                fields.append(listified[num])                                                                                               # appends the strings to be used as the column / field names to fields
            #print(fields)
            output_writer = csv.DictWriter(f, fieldnames = fields)                                                                          # tells where DictWriter to write the fieldnames and what they are from fields
            output_writer.writeheader()                                                                                                     # this writes the fieldnames as column headers
            counter = 0                                                                                                                     # the counter here is used to tell the user how many rows of data were written to the csv file
            for index in range(0,len(listified),len(fields)):                                                                               # loops over all words in listified at an interval of the number of fields
                #print(index)
                if index == 0:                                                                                                              # checks index value, this will skip over the head
                    counter += len(fields)                                                                                                  # adds the length of fields to the counter
                    continue                                                                                                                # starts the loop again
                elif index >= len(fields) and counter < (len(listified) - 1):                                                               # checks that the index is between the first record that will populate the csv and the start of the last row of data
                    row_data = {}                                                                                                           # this will store one record to be entered into the csv as a dictionary 
                    for n in range(len(fields)):                                                                                            # loops over the strings in listified to be added as a dictionary to row_data
                        row_data[fields[n]] = listified[index + n]                                                                          # appends the dictionary value to row_data
                    #print(row_data) 
                    output_writer.writerow(row_data)                                                                                        # writes the row to the csv
                    counter += len(fields)                                                                                                  # increments the counter
                    #print(f"added row\t\tindex: {index}")
                else:                                                                                                                       # helps the user diagnose a failure of the csv writer
                    print(f"I populated the file with {counter//len(fields)} rows of data and then failed")
                    return                                                                                                                  # exits the program if an error occurred
            print(f"\nI wrote {counter//len(fields)} rows to {output_file_name}.\n\n")                                                      # lets the user know when the csv file is written                                            
    except:
        print("I wasn't able to populate the csv file.")                                                                                    # lets the user know an error has occurred during the writing process


html_to_csv()                                                                                                                               # runs the function html_to_csv()

