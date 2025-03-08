import csv
ffile=open("z.csv",'w')
output=csv.writer(ffile,delimiter=';',lineterminator='\n')
fields =['Location','Day', 'Forecast_Date', 'Run', 'Forecast_Hr', '850_mb','Tmax','Tmin']
output.writerow(fields) # Write headers
print(output)
