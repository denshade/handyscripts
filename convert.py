
import pandas as pd
import sys

if len( sys.argv ) > 1: 
    sourcefile=sys.argv[1]
    alldata = pd.read_csv (sourcefile)
else:
    print('usage: convert.py <sourcefile>')
    print('Converts a csv file of group,date,code tuples into a timeline csv')
    print('Output: group, used dates as columns and code on each row/col combination.')
    sys.exit()

result = pd.DataFrame({'group': []})
dates = alldata.loc[:, 'date'].drop_duplicates(keep='last')
groups = alldata.loc[:, 'group'].drop_duplicates(keep='last')

pd.to_datetime(dates, infer_datetime_format=True)  
dates = dates.sort_values()


for index, value in dates.items():
    result[value] = []

for index, group in groups.items():
    groupDictionary = {}
    groupDictionary["group"] = group
    for index, row in alldata.iterrows():
        if row['group'] == group: 
            if row['date'] in groupDictionary.keys():
                groupDictionary[row['date']] += "," + row['code']
            else:
                groupDictionary[row['date']] = row['code']

    result = pd.concat([result, pd.DataFrame(groupDictionary, index=[0])], ignore_index = True, axis = 0)

print(result.to_csv(index=False))