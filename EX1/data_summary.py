# Ofir Duchovne - 315532242
# Shoval Zohar - 206182784

import csv
import os
import json


class DataSummary:

    accepted_delimiters = ['.', ':', '|', '-', ';', '#', '*', ',']

    def __init__(self, datafile, metafile):
        """
        Initializes the DataSummary object
        """
        self.data = []
        if not metafile or not datafile:
            raise Exception("ValueError: No datafile or metafile specified")
        if not os.path.isfile(datafile) or not os.path.isfile(metafile):
            raise Exception('ValueError: File not found')

        with open(metafile, 'r') as f:
            rawfeatures = dict(next(csv.DictReader(f)))
            # print(self.features)
            self.features = { x:{"__values":list(),"type":rawfeatures[x]} for x in rawfeatures }
            # print(self.features)
           
        with open(datafile, 'r') as f:
            rawdata = json.load(f)
            for record in rawdata["data"]:
                newrecord = dict()
                for feature in self.features.keys():
                    if feature not in record.keys():
                        newrecord[feature] = None
                    else:
                        if self.features[feature]['type'] == 'string':
                            newrecord[feature] = record[feature]
                        else:
                            newrecord[feature] = float(record[feature])
                    self.features[feature]['__values'].append(newrecord[feature])
                self.data.append(newrecord)

    def __getitem__(self, index):
        """
        Returns a record by index or a list of values o a feature by name
        """
        if type(index) is int:
            try:
                return self.data[index].copy()
            except IndexError:
                raise IndexError("Index out of range")
        elif type(index) is str:
            try:
                return self.features[index]['__values'].copy()
            except KeyError:
                raise KeyError("Key not found")

    def values_without_nulls(self, feature):
        """
        feature: the name of the feature
        Returns a list of values for a feature without nulls
        """
        if feature not in self.features.keys():
            raise KeyError("Key not found")
        return [x for x in self.features[feature]['__values'] if x is not None]

    def sum(self,feature):
        """
        feature: the name of the feature
        Returns a number, the sum of all values for a feature
        """
        if feature not in self.features.keys():
            raise KeyError("Feature not found")
        if self.features[feature]['type'] == 'string':
            raise TypeError("TypeError: Type must be numeric")
        return sum(self.values_without_nulls(feature))

    def count(self,feature):
        """
        feature: the name of the feature
        Returns the number of records for a feature
        """
        if feature not in self.features.keys():
            raise KeyError("Feature not found")
        return len(self.values_without_nulls(feature))

    def mean(self,feature):
        """
        feature: the name of the feature
        Returns a number, the mean of all values for a feature
        """
        if feature not in self.features.keys():
            raise KeyError("Feature not found")
        if self.features[feature]['type'] == 'string':
            raise TypeError("TypeError: Type must be numeric")
        valuesWithoutNulls = self.values_without_nulls(feature)
        return sum(valuesWithoutNulls)/len(valuesWithoutNulls)

    def min(self,feature):
        """
        feature: the name of the feature
        Returns a number, the minimum of all values for a feature
        """
        if feature not in self.features.keys():
            raise KeyError("Feature not found")
        if self.features[feature]['type'] == 'string':
            raise TypeError("TypeError: Type must be numeric")
        return min(self.values_without_nulls(feature))

    def max(self,feature):
        """
        feature: the name of the feature
        Returns a number, the maximum of all values for a feature
        """
        if feature not in self.features.keys():
            raise KeyError("Feature not found")
        if self.features[feature]['type'] == 'string':
            raise TypeError("TypeError: Type must be numeric")
        return max(self.values_without_nulls(feature))

    def unique(self,feature):
        """
        feature: the name of the feature
        Returns a list of unique values for a feature
        """
        if feature not in self.features.keys():
            raise KeyError("Feature not found")
        to_return = list(set(self.values_without_nulls(feature)))
        to_return.sort()
        return to_return

    def mode(self,feature):
        """
        feature: the name of the feature
        Returns a list of the most frequent values for a feature
        """
        if feature not in self.features.keys():
            raise KeyError("Feature not found")
        temp = {value:self.values_without_nulls(feature).count(value) for value in self.unique(feature)}
        return [v for v in temp.keys() if temp[v] == max(temp.values())]

    def empty(self,feature):
        """
        feature: the name of the feature
        Returns a number, the count of null values for a feature
        """
        if feature not in self.features.keys():
            raise KeyError("Feature not found")
        return len([x for x in self.features[feature]['__values'] if x is None])

    def to_csv(self,filename,delimiter=','):
        """
        filename: the name of the file to write to
        delimiter: the delimiter to use in the file
        accepts a delimiter from the accepted_delimiters list: ['.', ':', '|', '-', ';', '#', '*', ',']
        Writes the data to a csv file
        """
        if delimiter not in self.accepted_delimiters:
            delimiter = ','        
        with open(filename, 'w') as f:
            writer = csv.writer(f, delimiter=delimiter)
            writer.writerow(self.features.keys())
            for record in self.data:
                writer.writerow([record[x] for x in self.features.keys()])
