testBytes = b'\xd0\x91\xd0\xb0\xd0\xb9\xd1\x82\xd1\x8b'
testIndexes = [0, 1, 2, 3, 4, 5]
testValues = [2, 0, 2, 5, 4, 3, 0, 2, 5, 4, 3]
testMax = 5
testMin = 0
testMaxIndex = 3
testMinIndex = 1


class Calculations:
    def __init__(self, *args, **kwargs):
        print('Calc')

    def findMax(self, data, param):
        newMax = 0
        maxIndexes = []
        for i in range(0, len(data)):
            if data[i] > newMax:
                newMax = data[i]
        for i in range(0, len(data)):
            if data[i] == newMax:
                maxIndexes.append(i)
        if param == 'number':
            return newMax
        elif param == 'index':
            return maxIndexes[0]
        elif param == 'all_indexes':
            return maxIndexes
        else:
            return newMax, maxIndexes



calc = Calculations()

print(calc.findMax(testValues, 'number'))
print(calc.findMax(testValues, 'index'))
print(calc.findMax(testValues, 'all_indexes'))

