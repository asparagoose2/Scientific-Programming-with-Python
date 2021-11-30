import csv
import os
import json


class DataSummary:

    def __init__(self, datafile, metafile):
        self.data = []
        if not os.path.isfile(datafile) or not os.path.isfile(metafile):
            raise Exception('ValueError: File not found')

        with open(metafile, 'r') as f:
            self.features = dict(next(csv.DictReader(f)))
            # print(self.features)
           
        with open(datafile, 'r') as f:
            rawdata = json.load(f)
            for record in rawdata["data"]:
                newrecord = dict()
                for feature in self.features.keys():
                    if feature not in record.keys():
                        newrecord[feature] = None
                    else:
                        newrecord[feature] = record[feature]
                self.data.append(newrecord)


test = DataSummary('happiness.json', 'happiness_meta.csv')
print("Hello World")


        