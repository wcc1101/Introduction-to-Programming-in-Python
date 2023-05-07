import os
import sys

class Record:
    '''Represent a record.'''
    def __init__(self, category, description, amount):
        '''initialize a record'''
        self._category = category
        self._description = description
        self._amount = int(amount)

    @property
    def category(self):
        '''return category'''
        return self._category
    
    @property
    def description(self):
        '''return description'''
        return self._description
    
    @property
    def amount(self):
        '''return amount'''
        return self._amount
    
class Records:
    '''Maintain a list of all the 'Record's and the initial amount of money.'''
    def __init__(self):
        '''initialize the records and initial money'''
        try:
            with open('records.txt', 'r') as f:
                # read from savedfile
                self._initial_money = int(f.readline())
                self._records = [Record(record.split(' ')[0], record.split(' ')[1], int(record.split(' ')[2])) for record in f.readlines()]
            print('Welcome back!')
        except:
            # initialize records to empty
            self._records = []
            # if invalid format
            if os.path.exists('records.txt'):
                sys.stderr.write('Invalid format in records.txt. Deleting the contents.')
                os.remove('records.txt')
            # input initial money
            try:
                self._initial_money = int(input('How much money do you have? '))
            except:
                sys.stderr.write('Invalid value for money. Set to 0 by default.')
                self._initial_money = 0

    def add(self, input_string, categories):
        '''add a new record into records'''
        try:
            record = Record(*input_string.split(' '))
            # check if category valid
            if categories.is_category_valid(record.category):
                try:
                    # add to records
                    self._records.append(record)
                except:
                    sys.stderr.write('Invalid value for money. Fail to add a record.')
            else:
                sys.stderr.write('The specified category is not in the category list.\nYou can check the category list by command "view categories".\nFail to add a record.')
        except:
            sys.stderr.write('The format of a record should be like this: meal breakfast -50. Fail to add a record.')
    
    def view(self):
        '''show the records'''
        print('Here\'s your expense and income records:')
        print('Category        Description          Amount')
        print('=============== ==================== ======')
        # print records/calculate total money
        totalMoney = self._initial_money
        for record in self._records:
            print(record.category, ' ' * (16 - len(record.category)), record.description, ' ' * (21 - len(record.description)), record.amount, sep='')
            totalMoney = totalMoney + record.amount
        print('===========================================')
        print(f'Now you have {totalMoney} dollars.')
    
    def delete(self, input_string):
        '''delete a record'''
        try:
            record = Record(*input_string.split(' '))
            try:
                # remove from records
                for r in self._records:
                    if (r.category, r.description, r.amount) == (record.category, record.description, record.amount):
                        self._records.remove(r)
                        break
            except:
                sys.stderr.write(f'There\'s no record with {record.category} {record.description} {record.amount}. Fail to delete a record.')
        except:
            sys.stderr.write('Invalid format. Fail to delete a record.')
    
    def find(self, target_categories):
        '''show the records in the subcategories of a category'''
        # find in records
        found_records = list(filter(lambda record : record.category in target_categories, self._records))
        # show found records
        print(f'Here\'s your expense and income records under category "{target_categories[0]}":')
        print('Category        Description          Amount')
        print('=============== ==================== ======')
        total_amount = 0
        for record in found_records:
            print(record.category, ' ' * (16 - len(record.category)), record.description, ' ' * (21 - len(record.description)), record.amount, sep='')
            total_amount += record.amount
        print('===========================================')
        print(f'The total amount above is {total_amount}.')
    
    def save(self):
        '''save the initial money and records'''
        # write to save file
        with open('records.txt', 'w') as f:
            f.write(str(self._initial_money) + '\n')
            f.writelines([str(record.category) + ' ' + str(record.description) + ' ' + str(record.amount) + '\n' for record in self._records])

class Categories:
    '''Maintain the category list and provide some methods.'''
    def __init__(self):
        '''initialize the categories'''
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]
       
    def view(self, categories = [], depth = -1):
        '''show the categories'''
        if depth == -1:
            categories = self._categories
        if type(categories) == str:
            print(f"{'  ' * depth}- {categories}")
        else:
            for c in categories:
                self.view(c, depth + 1)
    
    def is_category_valid(self, category, categories = []):
        '''check if the category in the categories defined'''
        if categories == []:
            categories = self._categories
        if type(categories) == str:
            # base case
            return category == categories
        else:
            # recursive case
            valid = False
            for c in categories:
                valid = valid or self.is_category_valid(category, c)
            return valid
    
    def find_subcategories(self, category):
        '''find the category and return its subcategories'''
        def find_subcategories_gen(category, categories, found = False):
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child, found)
                    if child == category and index + 1 < len(categories) and type(categories[index + 1]) == list:
                        yield from find_subcategories_gen(category, categories[index + 1], True)
            else:
                if categories == category or found:
                    yield categories
            
        return list(find_subcategories_gen(category, self._categories))

if __name__ == '__main__':
    categories = Categories()
    records = Records()
    while True:
        command = input('\nWhat do you want to do (add / view / delete / view categories / find / exit)? ')
        if command == 'add':
            record = input('Add an expense or income record with category, description, and amount (separate by spaces):\n')
            records.add(record, categories)
        elif command == 'view':
            records.view()
        elif command == 'delete':
            delete_record = input("Which record do you want to delete? ")
            records.delete(delete_record)
        elif command == 'view categories':
            categories.view()
        elif command == 'find':
            category = input('Which category do you want to find? ')
            target_categories = categories.find_subcategories(category)
            records.find(target_categories)
        elif command == 'exit':
            records.save()
            break
        else:
            sys.stderr.write('Invalid command. Try again.\n')