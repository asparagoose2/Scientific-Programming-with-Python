from data_summary import DataSummary 

if __name__ == "__main__":
    try:
        DS_err = DataSummary()
    except Exception as err:
        print("Exception: ", err)
    else:
        print("unexpected DataSummary constructor")

    DS = DataSummary(datafile="happiness.json",metafile="happiness_meta.csv")
    print(DS[3])
    print(DS["Country"])

    try:
        DS['GDP']
    except Exception as err:
        print("Exception: ", err)
    else:
        print("unexpected feature GDP")

    try:
        DS['data']
    except Exception as err:
        print("Exception: ", err)
    else:
        print("unexpected feature data")

    print(DS.mean("Happiness Score"))
    print(DS.mode("Class"))
    print(DS.unique("Region"))

    try:
        DS.min("Country")
    except Exception as err:
        print("Exception: ", err)
    else:
        print("unexpected function min for categorical feature")


    DS.to_csv("happiness.csv")

