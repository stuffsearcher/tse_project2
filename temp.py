import pandas

f = pandas.read_csv('cwd\data2.csv')

y = pandas.cut(f['Speed'],[0,2,4,6,8,10,12,14])
 
f['bins'] = y

f = f.set_index('Time') #f.set_index('Time', inplace=True)