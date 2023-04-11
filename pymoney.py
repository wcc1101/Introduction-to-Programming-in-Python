import os
import sys

def initialize():
    try:
        with open('records.txt', 'r') as f:
            # read from savedfile
            initialMoney = int(f.readline())
            records = [tuple([record.split(' ')[0], int(record.split(' ')[1][:-1])]) for record in f.readlines()]
        print('Welcome back!')
    except:
        # initialize records to empty
        records = []
        # if invalid format
        if os.path.exists('records.txt'):
            sys.stderr.write('Invalid format in records.txt. Deleting the contents.')
            os.remove('records.txt')
        # input initial money
        try:
            initialMoney = int(input('How much money do you have? '))
        except:
            sys.stderr.write('Invalid value for money. Set to 0 by default.')
            initialMoney = 0

    return initialMoney, records

def add(records):
    try:
        # input record
        dscp, amnt = input('Add an expense or income record with description and amount:\n').split(' ')
        try:
            # add to records
            records.append(tuple([dscp, int(amnt)]))
        except:
            sys.stderr.write('Invalid value for money. Fail to add a record.')
    except:
        sys.stderr.write('The format of a record should be like this: breakfast -50. Fail to add a record.')

    return records

def view(initialMoney, records):
    print('Here\'s your expense and income records:')
    print('Description              Amount')
    print('======================== ======')
    # print records/calculate total money
    totalMoney = initialMoney
    for record in records:
        print(record[0], ' ' * (25 - len(record[0])), record[1], sep='')
        totalMoney = totalMoney + record[1]
    print('======================== ======')
    print(f'Now you have {totalMoney} dollars.')

def delete(records):
    try:
        # input record to be deleted
        dscp, amnt = input('Which record do you want to delete?\n').split(' ')
        try:
            # remove from records
            records.remove(tuple([dscp, int(amnt)]))
        except:
            sys.stderr.write(f'There\'s no record with {dscp} {amnt}. Fail to delete a record.')
    except:
        sys.stderr.write('Invalid format. Fail to delete a record.')

    return records

def save(initialMoney, records):
    # write to save file
    with open('records.txt', 'w') as f:
        f.write(str(initialMoney) + '\n')
        f.writelines([str(record[0]) + ' ' + str(record[1]) + '\n' for record in records])

if __name__ == '__main__':
    initialMoney, records = initialize()
    while True:
        # input command
        command = input('\nWhat do you want to do (add / view / delete / exit)? ')
        # handle different commands
        if command == 'add':
            records = add(records)
        elif command == 'view':
            view(initialMoney, records)
        elif command == 'delete':
            records = delete(records)
        elif command == 'exit':
            save(initialMoney, records)
            break
        else:
            sys.stderr.write('Invalid command. Try again.\n')
