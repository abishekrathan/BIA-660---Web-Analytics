# Assignment-3

# Abishek Lakshmirathan

import datetime
import csv
from collections import OrderedDict, defaultdict
import operator
from math import sqrt
class DataFrame(object):
    @classmethod
    def from_csv(cls, file_path, delimiting_character=',', quote_character='"'):
        with open(file_path, 'rU') as infile:
            reader = csv.reader(infile, delimiter=delimiting_character, quotechar=quote_character)

            data_collection = []

            for index, row in enumerate(reader):
                data_collection.append(row)

            return cls(list_of_lists=data_collection)

    # Task 3

    @classmethod
    def get_column_type(self, column, col_collection):
        is_bool = True
        for col in col_collection:
            try:
                if isinstance(col, bool) is False:
                    is_bool = False
            except ValueError:
                is_bool = False
        if is_bool:
            return bool
        is_int = True
        for col in col_collection:
            try:
                if isinstance(col, int) is False:
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

                        if not (isinstance(col, datetime.datetime)):
                            is_date = False
                    except ValueError:
                        is_date = False
            if is_date:

                return datetime
            else:
                raise TypeError('This operation cannot be performed on string values')
        return None

    # Task 4
    @classmethod
    def add_rows(self, list_of_lists):
        length = len(self.data[0])
        for row in list_of_lists:
            if (len(row) == length):
                self.data.append(row)
            else:
                raise ValueError('The length of the row does not match to that of the existing data')
        df.data = [OrderedDict(zip(df.header, row)) for row in df.data]

    # Task 5
    @classmethod
    def add_columns(self, list_of_values, col_name):
        length_rows_data = len(df.data)
        length_values = len(list_of_values)
        if (length_rows_data == length_values):
            for index, headername in enumerate(df.header):
                df.data[index][col_name] = list_of_values[index]
            df.header.append(col_name)
        else:
            raise ValueError('The length of the column does not match to that of the existing data')

    # Task 2
    # Stripping whitespaces
    def __init__(self, list_of_lists, header=True):

        for each_list in list_of_lists:
            for index, word in enumerate(each_list):
                each_list[index] = str(word).strip()
        for price_col in list_of_lists[1:]:
            price_col[2] = int(price_col[2])
        for data_col in list_of_lists[1:]:
            data_col[0] = datetime.datetime.strptime(data_col[0], '%m/%d/%y %H:%M')
        for data_col in list_of_lists[1:]:
            data_col[8] = datetime.datetime.strptime(data_col[8], '%m/%d/%y %H:%M')
        for data_col in list_of_lists[1:]:
            data_col[9] = datetime.datetime.strptime(data_col[9], '%m/%d/%y %H:%M')
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
        # if item is a string or unicode object
        elif isinstance(item, (str, unicode)):

            return Series([row[item] for row in self.data])

        # for rows and columns
        # if item is a tuple
        elif isinstance(item, tuple):
            if isinstance(item[0], list) or isinstance(item[1], list):
                if isinstance(item[0], list):
                    row_collection = [row for index, row in enumerate(self.data) if index in item[0]]
                else:
                    row_collection = self.data[item[0]]
                if isinstance(item[1], list):
                    if all([isinstance(thing, int) for thing in item[1]]):
                        return [
                            [column_value for index, column_value in enumerate([value for value in row.itervalues()]) if
                             index in item[1]] for row in row_collection]
                    elif all([isinstance(thing, (str, unicode)) for thing in item[1]]):
                        return [[row[column_name] for column_name in item[1]] for row in row_collection]
                    else:
                        raise TypeError('What the hell is this')
                else:
                    return [[value for value in row.itervalues()][item[1]] for row in row_collection]
            else:
                if isinstance(item[1], (int, slice)):
                    return [[value for value in row.itervalues()][item[1]] for row in self.data[item[0]]]
                elif isinstance(item[1], (str, unicode)):
                    return [row[item[1]] for row in self.data[item[0]]]
                else:
                    raise TypeError('I don\'t know how to handle this...')

        # only for lists of column names
        elif isinstance(item, list):

            list_of_true_rows = []
            for index,val in enumerate(item):
                if val:
                    list_of_true_rows.append(self.data[index])
            return list_of_true_rows
        else:
            return [[row[column_name] for column_name in item] for row in self.data]


    def get_rows_where_column_has_value(self, column_name, value, index_only=False):
        if index_only:
            return [index for index, row_value in enumerate(self[column_name]) if row_value == value]
        else:
            return [row for row in self.data if row[column_name] == value]





    @classmethod
    def min(self, column, col_contents):

        col_type = self.get_column_type(column, col_contents)
        if col_type == int or col_type == datetime:
            return min(col_contents)
        else:
            return None

    @classmethod
    def max(self, column, col_contents):

        col_type = self.get_column_type(column, col_contents)
        if col_type == int or col_type == datetime:
            return max(col_contents)
        else:
            return None

    @classmethod
    def sum(self, column, col_contents):
        summation = 0
        col_type = self.get_column_type(column, col_contents)
        if col_type == int :
            for i in col_contents:
                summation = summation + i
            return summation
        else:
            return "summation cannot be performed on datetime"

    @classmethod
    def avg(self, column, col_contents):
        summation = 0
        length = len(col_contents)
        col_type = self.get_column_type(column, col_contents)
        if col_type == int or col_type == datetime:
            for i in col_contents:
                summation = summation + i
            return summation / length
        else:
            return None

    @classmethod
    def median(self, column, col_contents):

        length = len(col_contents)
        sorted_list = col_contents.sort(reverse=False)
        col_type = self.get_column_type(column, col_contents)
        if col_type == int or col_type == datetime:
            if length % 2 == 0:

                median = (sorted_list[length/2]+sorted_list[(length/2) + 1])/2
            else:
                median = sorted_list[length/2 + 1]
        return median

    @classmethod
    def stddev(self, column, col_contents):
        length = len(col_contents)
        sorted_list = col_contents.sort(reverse=False)
        summation = 0
        dist = 0
        col_type = self.get_column_type(column, col_contents)
        if col_type == int:
            for i in sorted_list:
                summation = summation + i
            mean = summation/length

            for x in sorted_list:
                dist = dist + ((x-mean)**2)

            stdev = sqrt(dist/length)
            return stdev
        else:
            return "This operation cannot be performed on types other than int"



            # Assignment 3

            # Task 1

    def sort_by(self, reverse_list, column_list):
        for column in column_list:
            for reverse in reverse_list:
                col_contents = [row[column] for row in self.data]
                col_type = self.get_column_type(column, col_contents)
                if col_type == int:

                    sort = sorted(self.data, key=operator.itemgetter(column), reverse=reverse)

                else:
                    if col_type == datetime:
                        sort = sorted(self.data, key=operator.itemgetter(column), reverse=reverse)
                return sort

    def group_by(self, column_1, column_2, agg_func):
        col_1_contents = [row[column_1] for row in self.data]
        col_2_contents = [row[column_2] for row in self.data]
        zipped_list = zip(col_1_contents, col_2_contents)
        grouped_data_frame = defaultdict(list)

        col_1_set = set(col_1_contents)

        for col_1_attr, col_2_attr in zipped_list:
            for attribute_type in col_1_set:
                key = attribute_type

                if col_1_attr == key:
                    grouped_data_frame[key].append(col_2_attr)
        if str(agg_func) == "min":
            for key in col_1_set:
                print key, "-", df.min(column_2, grouped_data_frame[key])
                continue
        else:
            if str(agg_func) == "max":
                for key in col_1_set:
                    print key, "-", df.max(column_2, grouped_data_frame[key])
                    continue
            else:
                if str(agg_func) == "sum":
                    for key in col_1_set:
                        print key, "-", df.sum(column_2, grouped_data_frame[key])
                        continue
                else:
                    if str(agg_func) == "avg":
                        for key in col_1_set:
                            print key, "-", df.avg(column_2, grouped_data_frame[key])
                            continue

                    else:
                        if str(agg_func) == "median":
                            for key in col_1_set:
                                print key, "-", df.avg(column_2, grouped_data_frame[key])
                                continue
                        else:
                            if str(agg_func) == "stddev":
                                for key in col_1_set:
                                    print key, "-", df.avg(column_2, grouped_data_frame[key])
                                    continue
                            else:

                                return "Pass any one of the aggregate functions: min,max,sum,avg,median,stddev"

        return "Group by and aggregate function execution complete..."



class Series(list):

        def __init__(self, list_of_values):
            self.data = list_of_values

        def __eq__(self, other):
            ret_list = []

            for item in self.data:
                if isinstance(other, int):
                    ret_list.append(int(item) == other)
            return ret_list

        def __gt__(self, other):
            ret_list = []
            for item in self.data:
                ret_list.append(item > other)
            return ret_list

        def __ge__(self, other):
            ret_list = []
            for item in self.data:
                ret_list.append(item >= other)

            return ret_list

        def __lt__(self, other):
            ret_list = []
            for item in self.data:
                ret_list.append(item < other)

            return ret_list

        def __le__(self, other):
            ret_list = []
            for item in self.data:
                ret_list.append(item <= other)

            return ret_list

        def __ne__(self, other):
            ret_list = []
            for item in self.data:
                ret_list.append(item != other)

            return ret_list

infile = open('SalesJan2009.csv')
lines = infile.readlines()
lines = lines[0].split('\r')

data = [l.split(',') for l in lines]
things = lines[559].split('"')
data[559] = things[0].split(',')[:-1] + [things[1].replace(',', '')] + things[-1].split(',')[1:]

df = DataFrame(list_of_lists=data, header=True)

# Testing
# sorting Task 1
print "sorting task 1"
print df.sort_by([False,False], ["Transaction_date","Price"])
#
# group by Task 3
print "groupby task 3"
print df.group_by("Payment_Type","Price", "max")

#boolean indexing Task 2
print "bool indexing task 2"
print df[df['Price'] > 3600]
