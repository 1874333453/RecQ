from random import random
from tool.file import FileIO


class DataSplit(object):

    def __init__(self):
        pass

    @staticmethod
    def dataSplit(data, test_ratio = 0.3, output=False, path='./', order=1, binarized = False):
        if test_ratio >= 1 or test_ratio <= 0:
            test_ratio = 0.3
        testSet = []
        trainingSet = []
        for entry in data:
            if random() < test_ratio:
                testSet.append(entry)
            else:
                trainingSet.append(entry)
        if output:
            FileIO.writeFile(path,'testSet['+str(order)+']', testSet)
            FileIO.writeFile(path, 'trainingSet[' + str(order) + ']', trainingSet)
        return trainingSet, testSet

    @staticmethod
    def crossValidation(data, k):
        for i in range(k):
            trainingSet = []
            testSet = []
            for index, line in enumerate(data):
                if index % k == i:
                    testSet.append(line[:])
                else:
                    trainingSet.append(line[:])
            yield trainingSet, testSet
