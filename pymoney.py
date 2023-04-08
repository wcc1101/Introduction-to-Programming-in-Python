import os

try:
    with open('records.txt', 'r') as f:
        # read from savedfile
        initialMoney = int(f.readline())
        records = [tuple([record.split(' ')[0], int(record.split(' ')[1][:-1])]) for record in f.readlines()]
    print('Welcome back!')
    # calculate total money
    totalMoney = initialMoney
    for record in records:
        totalMoney = totalMoney + record[1]
except:
    # initialize records to empty
    records = []
    # if invalid format
    if os.path.exists('records.txt'):
        print('Invalid format in records.txt. Deleting the contents.')
    # input initial money
    try:
        initialMoney = int(input('How much money do you have? '))
    except:
        print('Invalid value for money. Set to 0 by default.')
        initialMoney = 0
    # initialize total money
    totalMoney = initialMoney

while True:
    # input command
    command = input('\nWhat do you want to do (add / view / delete / exit)? ')
    # handle different commands
    if command == 'add':
        try:
            # input record
            dscn, amnt = input('Add an expense or income record with description and amount:\n').split(' ')
            try:
                # add to records
                records.append(tuple([dscn, int(amnt)]))
                # update total money
                totalMoney = totalMoney + int(amnt)
            except:
                print('Invalid value for money. Fail to add a record.')
        except:
            print('The format of a record should be like this: breakfast -50. Fail to add a record.')
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
        try:
            # input record to be deleted
            dscn, amnt = input('Which record do you want to delete?\n').split(' ')
            try:
                # remove from records
                records.remove(tuple([dscn, int(amnt)]))
                totalMoney = totalMoney - int(amnt)
            except:
                print(f'There\'s no record with {dscn} {amnt}. Fail to delete a record.')
        except:
            print('Invalid format. Fail to delete a record.')
    elif command == 'exit':
        # write to save file
        with open('records.txt', 'w') as f:
            f.write(str(initialMoney) + '\n')
            f.writelines([str(record[0]) + ' ' + str(record[1]) + '\n' for record in records])
        break
    else:
        print('Invalid command. Try again.')