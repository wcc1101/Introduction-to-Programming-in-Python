# input total money
while True:
    try:
        totalMoney = int(input('How much money do you have? '))
        break
    except:
        print('Enter an integer.')

# input records
while True:
    try:
        inputString = input('Add an expense or income record with description and amount:\n')
        records = inputString.split(', ')
        records = [tuple([x.split(' ')[0], int(x.split(' ')[1])]) for x in records]
        break
    except:
        print('Invalid format.')
# print(records)

# output records
print('Here\'s your expense and income records:')
for record in records:
    print(f'{record[0]} {record[1]}')
    # calculate total money
    totalMoney = totalMoney + int(record[1])

# output current money
print(f'Now you have {totalMoney} dollars.')
