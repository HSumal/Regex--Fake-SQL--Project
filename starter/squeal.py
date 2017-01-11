from reading import *
from database import *

# Below, write:
# *The cartesian_product function
# *All other functions and helper functions
# *Main code that obtains queries from the keyboard,
#  processes them, and uses the below function to output csv results

# I know I only put one example for everything in this project, as they
# take up so much room and time, and I figured one example should be enough
# on top of how much of a summary I give of the function/method


def print_csv(table):
    '''(Table) -> NoneType
    Print a representation of table.
    '''
    dict_rep = table.get_dict()
    columns = list(dict_rep.keys())
    print(','.join(columns))
    # this how to get rows from my helpers and etc.
    rows = table.get_data()
    num_rows = len(rows[0])
    for i in range(num_rows):
        cur_column = []
        for column in columns:
            cur_column.append(dict_rep[column][i])
        print(','.join(cur_column))


def run_query(database, query):
    '''(Database, str) -> Table
    Take in a Database and a string on what is to be done to the Database
    in terms of Squeal syntax.
    We assume the query provided is correct and is legitimate

    REQ: query is correct (proper squeal syntax) and query choices
    are in database

    I know the below isn't a Database object, but it follows the same rules of
    what a Database looks like so that's the reason for using it so it is more
    easily seen what happens

    >>>d1 = {"movie" : {"m1.movie" : ["LOTR", "SWTOR"],
             "m1.money" : ["LOTS", "EVEN MORE"]},
    >>>     "oscar" : {"m2.movie" : ["Harry", "Potter"],
                       "m2.money" : ["Also", "Lots"]}}
    >>>t1 = run_query(d1, "select * from movie")
    >>>print_csv(t1)
    m1.movie,m1.money
    LOTR,LOTS
    SWTOR,EVEN MORE
    '''
    # convert query to a list so we can more easily access every word
    list_query = query.split()
    # Now figure out the places of 'from' and 'where' as select will always
    # be 0
    # first make a boolean for 'where' since it is optional and could cause
    # program to crash
    where_exists = False
    for i in range(len(list_query)):
        if('from' == list_query[i]):
            from_index = i
        # 'where' is in an elif as 'where' is an optional part of the query
        elif('where' == list_query[i]):
            where_exists = True
            where_index = i
            where_query = list_query[i + 1:]
    # if where exists, get list of table names by going up to where
    if(where_exists):
        table_name_list = list_query[from_index + 1: where_index]
    # otherwise go to end
    else:
        table_name_list = list_query[from_index + 1:]
    # split table names at comma as there is no space between them
    for i in range(len(table_name_list)):
        table_name_list = table_name_list[i].split(',')
    # get list of table columns
    column_list = list_query[1: from_index]
    # split column names at commas as there is no space between them
    for i in range(len(column_list)):
        select_query = column_list[i].split(',')
    # get the keys of the inputted database
    database_names = database.get_keys()
    # create a list that will hold the tables that are to be queried
    table_list = []
    # loop through the table_names, and if one of them are in the list
    # of database keys, then add that table from database to the list
    for i in range(len(table_name_list)):
        if(table_name_list[i] in database_names):
            table_list.append(database.get_table(table_name_list[i]))
    # if there is only one table in table_list, then we don't need to do
    # cartesian_product, and there cannot be a where clause
    if(len(table_list) == 1):
        # create the returning table
        end_table = Table()
        # call the select step
        end_table = select_table(table_list[0], select_query)
        # call the where step if where exists
        if(where_exists):
            end_table = where_table(end_table, where_query)
        return end_table
    # otherwise do the needed steps
    else:
        # create a table that will result from cartesian_product
        cartesian_table = Table()
        # cycle through the table_list and perform cartesian_product
        for i in range(len(table_list)):
            if(i == 0):
                cartesian_table = cartesian_product(table_list[i],
                                                    table_list[i + 1])
            else:
                cartesian_table = cartesian_product(cartesian_table,
                                                    table_list[i])
        # create the returning table
        end_table = Table()
        # call the select step
        end_table = select_table(cartesian_table, select_query)
        # call the where step if where exists
        if(where_exists):
            end_table = where_table(end_table, where_query)
        return end_table


def select_table(table_to_change, select_query):
    '''(Table, str) -> Table
    This function takes in a table and the query that selects columns
    and returns a table with these columns

    >>>t1 = {"m1.money" : ["Lots", "More"], "m1.movie" : ["LOTR", "SWTOR"]}
    >>>t2 = select_table(t1, "m1.money")
    >>>print(t2.get_dict())
    {"m1.money" : ["Lots", "More"]}
    '''
    # first check if select-query == '*' if so return table
    if(select_query[0] == '*'):
        return table_to_change
    else:
        # create the new table
        changed_table = Table()
        # get the keys of the table to change as these are the
        # columns in the query
        table_to_change_keys = table_to_change.get_keys()
        table_to_change_data = table_to_change.get_list()
        # create a dict to store the new table data in
        changed_table_dict = {}
        # loop through the keys and if they're in the query,
        # add the key and data
        # to the dict
        for key in table_to_change_keys:
            if(key in select_query):
                for i in range(len(table_to_change_data)):
                    if(key in table_to_change_data[i]):
                        table_to_change_data[i].remove(key)
                        changed_table_dict[key] = table_to_change_data[i]
        # since our helper takes in a list of dict, make a list
        changed_table_list = []
        changed_table_list.append(changed_table_dict)
        # call helper and return
        changed_table.join_table(changed_table_list)
        return changed_table


def where_table(table_to_change, where_query):
    '''(Table, str) -> Table
    This function takes in a table and the query that sets a condition on how
    the table is to be organized/set-up; and returns this table

    >>>t1 = {"m1.movie" : ["LOTR", "SWTOR"], "o1.movie" : ["WoW", "SWTOR"]}
    >>>t2 = where_table(t1, "m1.movie = m2.movie")
    >>>print(t2.get_dict())
    {"m1.movie" : ["SWTOR"], "o1.movie" : ["SWTOR"]}
    '''
    # create the new table
    changed_table = Table()
    # get the data of the table in row-form
    row_list = table_to_change.get_rows()
    # now figure out which 'where-query' we are dealing with
    if('=' in where_query[0]):
        # now split query at = sign so we know column names
        # now get the data of the two columns
        # if they do remove that row and add to new list
        # now make a dict out of the list
        # now make the returning table
        pass
    elif('>' in where_query):
        # now split uery at > sign so we know column names
        # now loop through data and see if column1 data > column2 data
        # if they do remove that row and add to new list
        # now make a dict out of the list
        # now make the returning table
        pass
    # return returning table
    return table_to_change


def cartesian_product(table1, table2):
    '''(Table, Table) -> Table
    This functions takes in two tables and assigns every row of table 1
    to every row of table two, this will cause the resulting table to have
    rows equal to table1.rows * table2.rows

    REQ: table1, and table2 have unique column names
    REQ: table1 and table2 have correct Table formatting
    column_name : list_of_data

    I know the below isn't a Table object, but it follows the same rules of
    what a Table looks like so that's the reason for using it so it is more
    easily seen what happens

    >>>t1 = {"m1.movie" : ["LOTR", "SWTOR"],
             "m1.money" : ["LOTS", "EVEN MORE"]}
    >>>t2 = {"m2.movie" : ["Harry", "Potter"], "m2.money" : ["Also", "Lots"]}
    >>>t3 = cartesian_product(t1, t2)
    >>>print(t3.get_dict())
    {"m1.movie" : ["LOTR", "LOTR", "SWTOR", "SWTOR"],
     "m1.money" : ["LOTS", "LOTS", "EVEN MORE", "EVEN MORE"]
     "m2.movie" : ["Harry", "Potter", "Harry", "Potter"]
     "m2.money" : ["Also", "Lots", "Also", "Lots"]}
    '''
    # get table data and keys
    t1_keys = table1.get_keys()
    t2_keys = table2.get_keys()
    t1_data = table1.get_data()
    t2_data = table2.get_data()
    # create a list to put the duplicate * 2 of t1_data in
    t1_data_dup = []
    # create a list in each place so it is an identical, empty list to
    # t1_data
    for i in range(len(t1_data)):
        t1_data_dup.append([])
    # go until we reach the length of t1
    for j in range(len(t1_data)):
        # go until the end of the column and add everything twice to
        # t1_data_dup
        for h in range(len(t1_data[j])):
            # add t2_length times
            for i in range(len(t2_data[0])):
                t1_data_dup[j].append(t1_data[j][h])
    # sort t1_data so everything with the same name is together
    # cycle through every dict in table2 and multiply it by the length
    # of one column in table1 as they are all the same length
    for j in range(len(t2_data)):
        t2_data[j] = t2_data[j] * len(t1_data[0])
    # create a dictionary that will be put into a list to call the join_table
    # method from the Table class
    t3_dict = {}
    # add data to t3_dict
    for i in range(len(t1_keys)):
        t3_dict[t1_keys[i]] = t1_data_dup[i]
    for i in range(len(t2_keys)):
        t3_dict[t2_keys[i]] = t2_data[i]
    # create list and dict
    t3_list = []
    t3_list.append(t3_dict)
    # create a table and make the actual new table
    t3 = Table()
    t3.join_table(t3_list)
    return t3

if(__name__ == "__main__"):
    exit = "hi, this is just here for reasons :P"
    while(exit):
        query = input("Enter a SQuEaL query, or a blank line to exit:")
        print(query)
        # if query is not empty perform run_query
        if(query):
            # create the database, and run_query on database and inputted
            # query
            database_to_query = read_database()
            queried_table = run_query(database_to_query, query)
            # print resulting table
            print_csv(queried_table)
        # let exit = query so if it is blank, loop won't re-enter
        exit = query

    # t1 = Table()
    # t2 = Table()
    # t1.set_dict({"m1.movie" : ["LOTR", "SWTOR", "ayy", "money"],
    #               "m1.money" : ["LOTS", "EVEN MORE", "dank", "moola"]})
    # t2.set_dict({"m2.movie" : ["Harry", "Potter"],
    #               "m2.money" : ["Also", "Lots"]})
    # t3 = cartesian_product(t1, t2)
    # print(t3.get_dict())
    # print(t3)
