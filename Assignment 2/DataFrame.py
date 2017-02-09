# Assignment-2

# Abishek Lakshmirathan

import datetime
import csv
from collections import OrderedDict
from math import sqrt

class DataFrame(object):

    @classmethod

    def from_csv(cls, file_path, delimiting_character=',', quote_character='"'):
        with open(file_path, 'rU') as infile:
            reader = csv.reader(infile, delimiter=delimiting_character, quotechar=quote_character)
            data_collection = []
            for index, row in enumerate(reader):
                if index == 559:
                    row[2] = row[2].replace(',', '')
                data_collection.append(row)
            return cls(list_of_lists=data_collection)


    # Task 3

    @classmethod
    def get_column_type(self, column, col_collection):
        is_int = True
        for col in col_collection:
            try:
                if isinstance(int(col), int) is False:
                    is_int = False
            except ValueError:
                is_int = False
        if is_int:
            return int
        else:

            # Checking if all items of the column are dates
            is_date = True
            # try:
            for col in col_collection:
                if isinstance(col, int):
                   is_date = False
                else:
                    try:
                        if not (isinstance(datetime.datetime.strptime(col, '%m/%d/%y %H:%M'), datetime.datetime)):
                            is_date = False
                    except ValueError:
                        is_date = False
            if is_date:

            # converting each entry into Datetime objects

                for index, entry in enumerate(col_collection):
                    col_collection[index] = datetime.datetime.strptime(entry, '%m/%d/%y %H:%M')
                return datetime
            else:
                raise TypeError('The values in the column are strings and this operation cannot be performed.')
        return None


    @classmethod
    def min(self, column):
        col_collection = [row[column] for row in df.data]
        col_type=self.get_column_type(column, col_collection)
        if col_type == int:
            return min(col_collection)
        elif col_type == datetime:
            return min(col_collection)
        else:
            return None

    @classmethod
    def max(self, column):
        col_collection = [row[column] for row in df.data]
        col_type = self.get_column_type(column, col_collection)
        if col_type == int:
            return max(col_collection)
        elif col_type == datetime:
            return max(col_collection)
        else:
            return None

    @classmethod
    def median(self, column):
        col_collection = [row[column] for row in df.data]
        col_type = self.get_column_type(column, col_collection)
        if col_type == int or col_type == datetime:
            col_collection = sorted(col_collection)
            if len(col_collection) % 2 == 1:
                median = (len(col_collection)+1)/2
                return col_collection[median]
            else:
                median1 = len(col_collection)/2
                median2 = median1+1
                return col_collection[(median1 + median2)/2]
        else:
            raise TypeError('The values in the column are strings and this operation cannot be performed.')

    @classmethod
    def mean(self, column):
        col_collection = [row[column] for row in df.data]
        col_type = self.get_column_type(column, col_collection)
        sum=0
        if col_type == int:
            for col in col_collection:
                sum = sum + int(col)
            mean = sum/len(col_collection)
            return mean
        else:
            raise TypeError('The values in the column are strings and this operation cannot be performed.')


    @classmethod
    def sum(self, column):
        col_collection = [row[column] for row in df.data]
        col_type = self.get_column_type(column, col_collection)
        summation=0
        if col_type == int:
            for col in col_collection:
                summation = summation + int(col)
            return summation
        else:
            raise TypeError('The values in the column are strings and this operation cannot be performed.')

    @classmethod
    def std(self, column):
        col_collection = [row[column] for row in df.data]
        col_type = self.get_column_type(column, col_collection)
        sum = 0
        if (col_type == int):
            for col in col_collection:
                sum=sum+int(col)
            num_items = len(col_collection)
            mean = sum / num_items
            differences = [int(x) - mean for x in col_collection]
            sq_differences=0
            for d in differences:
                lis = [d ** 2 for d in differences]
            for item in lis:
                sq_differences = sq_differences + item
            return sqrt(sq_differences/num_items)
        else:
            raise TypeError('The values in the column are strings and this operation cannot be performed.')

    # Task 4
    @classmethod
    def add_rows(self, list_of_lists):
        length=len(df.data[0])
        for row in list_of_lists:
            if(len(row) == length):
                df.data.append(row)
            else:
                raise ValueError('The length of the row does not match to that of the existing data')
        df.data=[OrderedDict(zip(df.header, row)) for row in df.data]

    # Task 5
    @classmethod
    def add_columns(self,list_of_values,col_name):
        length_rows_data = len(df.data)
        length_values = len(list_of_values)
        if(length_rows_data == length_values):
            for index, headername in enumerate(df.header):
                df.data[index][col_name]=list_of_values[index]
            df.header.append(col_name)
        else:
            raise ValueError('The length of the column does not match to that of the existing data')

    # Task 2
    # Stripping whitespaces
    def __init__(self, list_of_lists, header=True):
        for each_list in list_of_lists:
            for index, word in enumerate(each_list):
                each_list[index] = word.strip()
        if header:
            # Assigning header
            self.header = list_of_lists[0]
            self.data = list_of_lists[1:]
        else:
            self.header = ['column' + str(index + 1) for index, column in enumerate(list_of_lists)]
            self.data = list_of_lists

        # Task 1
        # header name uniqueness

        is_unique = (all(list_of_lists[0].count(x) == 1 for x in list_of_lists[0]))
        if not is_unique:
            raise TypeError('Elements in the header are not unique!')
        self.data = [OrderedDict(zip(self.header, row)) for row in self.data]

    def __getitem__(self, item):
        # for rows only
        if isinstance(item, (int, slice)):
            return self.data[item]

        # for columns only
        elif isinstance(item, (str, unicode)):
            return [row[item] for row in self.data]

        # for rows and columns
        elif isinstance(item, tuple):
            if isinstance(item[0], list) or isinstance(item[1], list):
                if isinstance(item[0], list):
                    row_collection = [row for index, row in enumerate(self.data) if index in item[0]]
                else:
                    row_collection = self.data[item[0]]
                if isinstance(item[1], list):
                    if all([isinstance(thing, int) for thing in item[1]]):
                        return [[column_value for index, column_value in enumerate([value for value in row.itervalues()]) if index in item[1]] for row in row_collection]
                    elif all([isinstance(thing, (str, unicode)) for thing in item[1]]):
                        return [[row[column_name] for column_name in item[1]] for row in row_collection]
                    else:
                        raise TypeError('Exception has occurred')
                else:
                    return [[value for value in row.itervalues()][item[1]] for row in row_collection]
            else:
                if isinstance(item[1], (int, slice)):
                    return [[value for value in row.itervalues()][item[1]] for row in self.data[item[0]]]
                elif isinstance(item[1], (str, unicode)):
                    return [row[item[1]] for row in self.data[item[0]]]
                else:
                    raise TypeError('I don\'t know how to handle this...')

        # for lists of column names
        elif isinstance(item, list):
            return [[row[column_name] for column_name in item] for row in self.data]

    def get_rows_where_column_has_value(self, column_name, value, index_only=False):
        if index_only:
            return [index for index, row_value in enumerate(self[column_name]) if row_value==value]
        else:
            return [row for row in self.data if row[column_name] == value]

infile = open('SalesJan2009.csv')
lines = infile.readlines()
lines = lines[0].split('\r')
data = [l.split(',') for l in lines]
things = lines[559].split('"')
data[559] = things[0].split(',')[:-1] + [things[1].replace(',', '')] + things[-1].split(',')[1:]
df = DataFrame(list_of_lists=data)
