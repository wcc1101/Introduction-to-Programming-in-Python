# input total money
while True:
    try:
        totalMoney = int(input('How much money do you have? '))
        break
    except:
        print('Enter an integer.')

records = []

while True:
    # input command
    command = input('\nWhat do you want to do (add / view / delete / exit)? ')
    # handle different commands
    if command == 'add':
        while True:
            try:
                # input record
                record = input('Add an expense or income record with description and amount:\n').split(' ')
                # add to records
                records.append(tuple([record[0], int(record[1])]))
                # update total money
                totalMoney = totalMoney + int(record[1])
                break
            except:
                print('Invalid format.')
    elif command == 'view':
        print('Here\'s your expense and income records:')
        print('Description              Amount')
        print('======================== ======')
        # print records
        for record in records:
            print(record[0], ' ' * (25 - len(record[0])), record[1], sep='')
        print('======================== ======')
        print(f'Now you have {totalMoney} dollars.')
    elif command == 'delete':
        # input record to be deleted
        record = input('Which record do you want to delete?\n').split(' ')
        record = tuple([record[0], int(record[1])])
        try:
            # remove from records
            records.remove(record)
            totalMoney = totalMoney - int(record[1])
        except:
            print('This record doesn\'t exist.')
    elif command == 'exit':
        break
    else:
        print('Invalid command.')