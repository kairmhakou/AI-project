import csv


reservationList=[]
zonesList=[]
with open('toy1.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file , delimiter=";")
    line_count=0
    for row in csv_reader:
        if row[0][0]=="r":
            if line_count== 0 :
                print(f'{", ".join(row)}')
                line_count += 1
            else:
                autos= row[5].split(',')
                print(f'{row[0]} ,{row[1]} , {row[2]}, {row[3]}, {row[4]}, {autos}, {row[6]}, {row[7]}')
                reservationList.append(row)
                line_count += 1
        elif row[0][0] == "z":
            zones= row[1].split(',')
            print(f'{row[0]},{zones}')
        else:
            print(f'{row}')
            
print(reservationList[0][5])
auto_list=reservationList[0][5].split(',')
print(auto_list)
