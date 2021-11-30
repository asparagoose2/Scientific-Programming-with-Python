import csv
import os
import json


class DataSummary:

    def __init__(self, datafile, metafile):
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
        if feature not in self.features.keys():
            raise KeyError("Key not found")
        return [x for x in self.features[feature]['__values'] if x is not None]

    def sum(self,feature):
        if feature not in self.features.keys():
            raise KeyError("Feature not found")
        if self.features[feature]['type'] == 'string':
            raise TypeError("TypeError: Type must be numeric")
        return sum(self.values_without_nulls(feature))

    def count(self,feature):
        if feature not in self.features.keys():
            raise KeyError("Feature not found")
        return len(self.values_without_nulls(feature))

    def mean(self,feature):
        if feature not in self.features.keys():
            raise KeyError("Feature not found")
        if self.features[feature]['type'] == 'string':
            raise TypeError("TypeError: Type must be numeric")
        return sum(self.values_without_nulls(feature))/len(self.values_without_nulls(feature))

    def min(self,feature):
        if feature not in self.features.keys():
            raise KeyError("Feature not found")
        if self.features[feature]['type'] == 'string':
            raise TypeError("TypeError: Type must be numeric")
        return min(self.values_without_nulls(feature))

    def max(self,feature):
        if feature not in self.features.keys():
            raise KeyError("Feature not found")
        if self.features[feature]['type'] == 'string':
            raise TypeError("TypeError: Type must be numeric")
        return max(self.values_without_nulls(feature))

    def unique(self,feature):
        if feature not in self.features.keys():
            raise KeyError("Feature not found")
        to_return = list(set(self.values_without_nulls(feature)))
        to_return.sort()
        return to_return
    
    # return a list of the values which appear the most in the feature (None values are not counted). HOW?
    def mode(self,feature):
        if feature not in self.features.keys():
            raise KeyError("Feature not found")
        if self.features[feature]['type'] == 'string':
            raise TypeError("TypeError: Type must be numeric")

    # return the number of None values in the feature.
    def empty(self,feature):
        if feature not in self.features.keys():
            raise KeyError("Feature not found")
        return len([x for x in self.features[feature]['__values'] if x is None])



test = DataSummary('happiness.json', 'happiness_meta.csv')

# print(test[-2])
# print(test['Happiness Rank'])
print(test.empty('Country'))

