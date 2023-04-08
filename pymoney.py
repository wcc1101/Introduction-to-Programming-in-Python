# input total money
totalMoney = int(input('How much money do you have? '))

# input record
inputString = input('Add an expense or income record with description and amount:\n')
record = inputString.split(' ')
totalMoney = totalMoney + int(record[1])

# output current money
print(f'Now you have {totalMoney} dollars.')