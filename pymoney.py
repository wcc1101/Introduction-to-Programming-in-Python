import os
import sys

def initialize():
    '''initialize the records and initial money'''
    try:
        with open('records.txt', 'r') as f:
            # read from savedfile
            initial_money = int(f.readline())
            records = [tuple([record.split(' ')[0], record.split(' ')[1], int(record.split(' ')[2])]) for record in f.readlines()]
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
            initial_money = int(input('How much money do you have? '))
        except:
            sys.stderr.write('Invalid value for money. Set to 0 by default.')
            initial_money = 0

    return initial_money, records

def initialize_categories():
    '''initialize the categories'''
    # return categories
    return ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]

def is_category_valid(category, categories):
    '''check if the category in the categories defined'''
    if type(categories) == str:
        # base case
        return category == categories
    else:
        # recursive case
        valid = False
        for c in categories:
            valid = valid or is_category_valid(category, c)
        return valid

def add(records, categories):
    '''add a new record into records'''
    try:
        # input record
        cate, dscp, amnt = input('Add an expense or income record with category, description, and amount (separate by spaces):\n').split(' ')
        # check if category valid
        if not is_category_valid(cate, categories):
            sys.stderr.write('Invalid category. Fail to add a record.')
            return records
        try:
            # add to records
            records.append(tuple([cate, dscp, int(amnt)]))
        except:
            sys.stderr.write('Invalid value for money. Fail to add a record.')
    except:
        sys.stderr.write('The format of a record should be like this: meal breakfast -50. Fail to add a record.')

    return records

def view(initial_money, records):
    '''show the records'''
    print('Here\'s your expense and income records:')
    print('Category        Description          Amount')
    print('=============== ==================== ======')
    # print records/calculate total money
    totalMoney = initial_money
    for record in records:
        print(record[0], ' ' * (16 - len(record[0])), record[1], ' ' * (21 - len(record[1])), record[2], sep='')
        totalMoney = totalMoney + record[2]
    print('===========================================')
    print(f'Now you have {totalMoney} dollars.')

def delete(records):
    '''delete a record'''
    try:
        # input record to be deleted
        cate, dscp, amnt = input('Which record do you want to delete?\n').split(' ')
        try:
            # remove from records
            records.remove(tuple([cate, dscp, int(amnt)]))
        except:
            sys.stderr.write(f'There\'s no record with {cate} {dscp} {amnt}. Fail to delete a record.')
    except:
        sys.stderr.write('Invalid format. Fail to delete a record.')

    return records

def view_categories(categories, depth = -1):
    '''show the categories'''
    if type(categories) == str:
        print(f"{'  ' * depth}- {categories}")
    else:
        for c in categories:
            view_categories(c, depth + 1)

def flatten(L):
    '''flatten the list L'''
    if type(L) == list:
        # recursive case
        result = []
        for child in L:
            result.extend(flatten(child))
        return result
    else:
        # base case
        return [L]
    
def find_subcategories(category, categories):
    '''find the category and return its subcategories'''
    if category == categories:
        # base case
        return True
    elif type(categories) == list:
        # recursive case
        for i, c in enumerate(categories):
            found = find_subcategories(category, c)
            if found == True:
                if i + 1 < len(categories) and type(categories[i + 1]) == list:
                    return flatten(categories[i:i + 2])
                else:
                    return [c]
            if found != []:
                return found
    # base case
    return []

def find(records, categories):
    '''show the records in the subcategories of a category'''
    # input category
    category = input('Which category do you want to find? ')
    # find subcategories
    subcategories = find_subcategories(category, categories)
    # find in records
    found_records = list(filter(lambda record : record[0] in subcategories, records))
    # show found records
    print(f'Here\'s your expense and income records under category "{category}":')
    print('Category        Description          Amount')
    print('=============== ==================== ======')
    total_amount = 0
    for record in found_records:
        print(record[0], ' ' * (16 - len(record[0])), record[1], ' ' * (21 - len(record[1])), record[2], sep='')
        total_amount += record[2]
    print('===========================================')
    print(f'The total amount above is {total_amount}.')

def save(initial_money, records):
    '''save the initial money and records'''
    # write to save file
    with open('records.txt', 'w') as f:
        f.write(str(initial_money) + '\n')
        f.writelines([str(record[0]) + ' ' + str(record[1]) + ' ' + str(record[2]) + '\n' for record in records])

if __name__ == '__main__':
    initial_money, records = initialize()
    categories = initialize_categories()
    while True:
        # input command
        command = input('\nWhat do you want to do (add / view / delete / view categories / find / exit)? ')
        # handle different commands
        if command == 'add':
            records = add(records, categories)
        elif command == 'view':
            view(initial_money, records)
        elif command == 'delete':
            records = delete(records)
        elif command == 'view categories':
            view_categories(categories)
        elif command == 'find':
            find(records, categories)
        elif command == 'exit':
            save(initial_money, records)
            break
        else:
            sys.stderr.write('Invalid command. Try again.\n')
