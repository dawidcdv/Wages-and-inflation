import pandas as pd
import re
import matplotlib
import matplotlib.pyplot as plt

def get_data(path, yearsRange):
    df = pd.read_csv(path, sep=";")
    years = []
    values = []

    for col in df.columns:
        res = re.search('(20\d+)',col)

        if res and int(res.group(1)) in yearsRange:
            values.append(pd.to_numeric(df[col].astype("str").values[0].replace(',', '.'), errors='ignore'))
            years.append(pd.to_datetime(0, unit='D', origin=str(res.group(1))))

    return values, years


def get_growth_indexes(data):
    return  [ round( (data[i]/data[i-1]) * 100, 1) for i in range(1,len(data)) ]

def get_real_growth_indexes(nominalGrowthIndexes, inflation):
    if len(nominalGrowthIndexes) != len(inflation):
        raise Exception("Inconsistent data")

    return  [ round( (nominalGrowthIndexes[i]/inflation[i]) * 100, 1) for i in range(0,len(nominalGrowthIndexes)) ]




sallaryData, indexSallary = get_data('wynagrodzenia.csv', range(2003,2020))
inflation, indexInf = get_data('inflacja.csv', range(2004, 2020))

sallaryNominalGrowIndexes = get_growth_indexes(sallaryData)
sallaryRealGrowIndexes = get_real_growth_indexes(sallaryNominalGrowIndexes, inflation)

sallarySeries = pd.Series(index=indexSallary,data=sallaryData)
data = pd.DataFrame(data={"Zarobki Nominalne" : sallaryNominalGrowIndexes, "Dobra konsumpcyjne" : inflation},
                    index=indexInf)




data.plot()
plt.suptitle("Wskaźnik cen dóbr konsumpcyjnych oraz zarobków nominalych")
plt.show()

data['Zarobki realne'] = sallaryRealGrowIndexes


data.plot()
plt.suptitle("Wskaźnik cen dóbr konsumpcyjnych, zarobków nominalych oraz realnych")
plt.show()


sallarySeries.plot()
plt.suptitle("Średnie wynagrodzenie brutto  w zł")
plt.show()

print(data)

print("Srednie")
print(data["Zarobki Nominalne"].mean())
print(data["Dobra konsumpcyjne"].mean())
print(data["Zarobki realne"].mean())

print("Mediany")
print(data["Zarobki Nominalne"].median())
print(data["Dobra konsumpcyjne"].median())
print(data["Zarobki realne"].median())


