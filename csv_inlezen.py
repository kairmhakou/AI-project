import csv


reservation_list=[]
with open('toy1.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file , delimiter=";")
    line_count=0
    for row in csv_reader:
        if line_count== 0 :
            print(f'{", ".join(row)}')
            line_count += 1
        else:
            auto= row[5].split(',')
            print(f'{row[0]} ,{row[1]} , {row[2]}, {row[3]}, {row[4]}, {auto}, {row[6]}, {row[7]}')
            reservation_list.append(row)
            line_count += 1
    print(f'Processed {line_count} lines.')

print(reservation_list[0][5])
auto_list=reservation_list[0][5].split(',')
print(auto_list)


