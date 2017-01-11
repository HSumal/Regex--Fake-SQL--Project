# @authour: Harpreet Singh Sumal
# S#: 1002353099
# One small note, a lot of REQ statements are left blank, this is because
# these functions are only called as helpers, and the requirements
# must be fulfilled in the function they are being called from


class Table():
    '''A class to represent a SQuEaL table'''

    def __init__(self, data_dict={}):
        '''(Table, empty dict) -> NoneType
        Creates a Table

        >>>t1 = Table()
        '''
        # create the table instance variable and assign to empty dict
        self._table = data_dict

    def set_dict(self, new_dict):
        '''(Table, dict of {str: list of str}) -> NoneType

        Populate this table with the data in new_dict.
        The input dictionary must be of the form:
            column_name: list_of_values
        '''
        # assign the new_dict to the Table
        self._table = new_dict

    def get_dict(self):
        '''(Table) -> dict of {str: list of str}

        Return the dictionary representation of this table. The dictionary keys
        will be the column names, and the list will contain the values
        for that column.
        '''
        # return the dictionary that has the data for table
        return self._table

    def get_column(self, column_name):
        '''Table -> list of str
        Return the column with column name that belongs to the table
        '''
        return self._table[column_name]

    def get_keys(self):
        '''(Table) -> list of str
        Return all the keys for the dictionary assigned to the Table

        REQ: key_number >= 0 and key_number <= len(self._table)
        '''
        # I decided there was no need for the stored_key to be a self/instance
        # variabe
        # create a var to store keys
        stored_key = []
        # loop through keys in dictionary
        for key in self._table:
            # store key in stored_key
            stored_key.append(key)

        return stored_key

    def get_data(self):
        '''(Table) -> list of str
        Return a list of the data assigned to the table
        '''
        # I decided there was no need for the stored_key to be a self/instance
        # variable
        # create a list to store all the data
        stored_data = []
        # loop through each key
        for key in self._table:
            # store data of each key in list
            stored_data.append(self._table[key])

        return stored_data

    def get_list(self):
        '''(Table) -> list of list of str
        Return a list that represents that Table, with the last element of
        every list being the key
        '''
        # create return list
        return_list = []
        # add a list to return table the same amount of times as there
        # are columns
        # get the keys and data and add to return_list
        keys = self.get_keys()
        data = self.get_data()
        for i in range(len(keys)):
            return_list.append(data[i])
            return_list[i].append(keys[i])
        return return_list

    def get_rows(self):
        '''(Table) -> list of list of str
        Return a list that represents that Table, with the keys in the first
        row, and every row there
        '''
        # key list
        key_list = self.get_keys()
        # column list
        column_list = []
        for i in range(len(key_list)):
            column_list.append(self._table[key_list[i]])
        # row list
        row_list = []
        for i in range(len(key_list)):
            row_list.append([])
        # this extra append is to hold keys
        row_list.append([])
        for i in range(len(key_list)):
            row_list[0].append(key_list[i])
        row_list_indices_check = 1
        for i in range(len(column_list)):
            for j in range(len(column_list[i])):
                row_list[row_list_indices_check].append(column_list[i][j])

            row_list_indices_check += 1
        return row_list

    def join_table(self, table_list):
        '''(Table, list of dict) -> NoneType
        Take a list of dictionaries in the format of Table and put them
        together to make one large table

        REQ: table_list in format column_name : list_of_data
        '''
        # first reset the dictionary as we use the same table var in
        # read_table
        self._table = {}
        # loop through the length of table_list and add each table
        # to the instance var
        for i in range(len(table_list)):
            self._table.update(table_list[i])


class Database(Table):
    '''A class to represent a SQuEaL database'''

    def __init__(self):
        '''(Database, empty dict) -> NoneType
        Creates a Database

        >>>d1 = Database()
        '''
        # create the database instance variable and assign to the empty dict
        self._database = {}

    def set_dict(self, new_dict):
        '''(Database, dict of {str: Table}) -> NoneType

        Populate this database with the data in new_dict.
        new_dict must have the format:
            table_name: table
        '''
        # assign new_dict to the Database
        self._database = new_dict

    def get_dict(self):
        '''(Database) -> dict of {str: Table}

        Return the dictionary representation of this database.
        The database keys will be the name of the table, and the value
        with be the table itself.
        '''
        # return the database as it is already of type {str: Table}
        return self._database

    def get_keys(self):
        '''(Database) -> list of str
        Return all the keys for the dictionary assigned to the Database

        >>>d1 = Database()
        >>>d1.set_dict({"movies" :
                       {"m.title" : ["Titanic", "Lord of the Rings"]}})
        >>>key = d1.get_key()
        >>>print(key)
        "movies"
        '''
        # I decided there was no need for the stored_key to be a self
        # variabe
        # create a list to store keys
        stored_key = []
        # loop through keys in dictionary
        for key in self._database:
            # store key in the stored_key var
            stored_key.append(key)

        return stored_key

    def get_table(self, key):
        '''(Database, str) -> Table
        Return the table assigned to the given key of the Database

        REQ: key must belong to the Database used
        '''
        # return the table at key
        return self._database[key]

    def join_tables(self, list_of_tables, list_of_table_names):
        '''(Database, list of Tables, list of str) -> NoneType
        Create a database from a list of tables in the correct Table format

        REQ: list_of_tables in format column_name : list_of_data
        REQ: len(list_of_table_names) > 0   <-- This assums list is populated
        REQ: len(list_of_table_names) == len(list_of_table_names)
        '''
        # loop through the list of tables and add them to database
        for i in range(len(list_of_tables)):
            self._database[list_of_table_names[i]] = list_of_tables[i]
