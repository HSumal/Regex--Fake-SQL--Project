# Functions for reading tables and databases

import glob
from database import *

# a table is a dict of {str:list of str}.
# The keys are column names and the values are the values
# in the column, from top row to bottom row.

# A database is a dict of {str:table},
# where the keys are table names and values are the tables.

# YOU DON'T NEED TO KEEP THE FOLLOWING CODE IN YOUR OWN SUBMISSION
# IT IS JUST HERE TO DEMONSTRATE HOW THE glob CLASS WORKS. IN FACT
# YOU SHOULD DELETE THE PRINT STATEMENT BEFORE SUBMITTING

# Write the read_table and read_database functions below


def read_table(csv_file_name):
    '''(str) -> Table
    Returns a Table of the data in the inputted csv file. The CSV file
    must be a file with data seperated by commas.

    The first line should contains the keys, and every line here-after
    should follow a pattern of the first-index per. line should be assigned
    to the first key

    REQ: csv_file_name == a csv file in the same directory as reading, database
    and squeal py

    >>>t1 = read_table("books.csv")
    >>>print(t1.get_dict())
    {"book.title" : ["Godel Escher Bach", "What if?", "Thing Explainer",
                     "Alan turing: The Enigma"],
     "book.year" : ["1979", "2014", "2015", "2014"],
     "book.author" : ["Douglas Hofstadter", "Randall Munor", "Randall Munroe",
                      "Andrew Hodges"]
    '''
    # create a list to store each word seperated at the comma
    words_seperated_at_comma = []
    # create a list to store the keys
    key_list = []
    # open file
    csv_file = open(csv_file_name, "r")
    # read all the line
    all_lines = csv_file.readlines()
    # get the length of each line (words per line), as it indicates the number
    # of keys and is useful in general, to do this we must do it in the
    # loop so create a counter that will get the length of only the first line
    line_counter = 0
    for next_line in all_lines:
        # split at each comma
        next_line = next_line.split(',')
        # get the length of the first line
        if(line_counter == 0 and len(next_line) > 0):
            len_of_each_line = len(next_line)
        # increment line counter
        line_counter += 1
        # loop through the line and add each index as an int to deck
        for i in range(0, len(next_line), 1):
            # first check if there is a word at i
            # and if not, do not add it to word list
            if(next_line[i].isspace()):
                del next_line[i]
                break
            # first check if word has '\n'
            elif('\n' in str(next_line[i])):
                # get the length of word
                len_of_word = len(next_line[i])
                # slice until last two spaces to remove '\n'
                next_line[i] = next_line[i][0: len_of_word - 1]
            words_seperated_at_comma.append(str(next_line[i]))
    # assign the keys to the key list by slicing up to the length of one line,
    # from the beginning as the first line will contain the keys
    key_list = words_seperated_at_comma[0: len_of_each_line]
    # slice the word list to remove the keys
    words_seperated_at_comma = words_seperated_at_comma[len_of_each_line:]
    # remove whitespace before and after words
    for i in range(len(words_seperated_at_comma)):
        words_seperated_at_comma[i] = words_seperated_at_comma[i].strip(' ')
    # create a list to contain the value of one column
    data_list = []
    # create a list that will contain dicts in the form of tables
    dict_list = []
    # create counter to place words in data_list
    counter_to_place = 0
    # loop through the amount of keys
    for i in range(len(key_list)):
        # add a list which will be the value of table
        data_list.append([])
        # loop through word list
        for j in range(i, len(words_seperated_at_comma), len(key_list)):
            # add word at correct position
            data_list[i].insert(counter_to_place, words_seperated_at_comma[j])
            # increment counter
            counter_to_place += 1
    # loop through dictionary list for same reasons as above
    for i in range(len(key_list)):
        dict_list.append(dict())
        dict_list[i] = {key_list[i]: data_list[i]}
    # create return_table
    return_table = Table()
    # call join helper method I created
    return_table.join_table(dict_list)
    # close file
    csv_file.close()
    return return_table


def read_database():
    '''(NoneType) -> Database
    returns a Database with the data set in tables for all the
    .csv files in the directory

    REQ: all csv files to be worked on are in the same directory as this file

    An example is not possible for this, but to give a visual of what will
    happen, refer to the function read_table. It will have dictionaries like
    those that are returned from read_table, mapped to the key which is its
    filename without the .csv extension
    '''
    # get all the file names
    file_name_list = glob.glob('*.csv')
    # get all the table names by stripping the .csv
    file_names = []
    for i in range(len(file_name_list)):
        # get the length of the name
        len_of_each_name = len(file_name_list[i])
        # slice word and add to name list so it removes the .csv
        file_names.append(file_name_list[i][0: len_of_each_name - 4])
    # make a list of tables with organized data by calling read_table
    table_list = []
    for i in range(len(file_name_list)):
        table_list.append(read_table(file_name_list[i]))
    # construct the dictionary that will hold the database by calling helper
    # function
    return_database = Database()
    return_database.join_tables(table_list, file_names)
    return return_database
