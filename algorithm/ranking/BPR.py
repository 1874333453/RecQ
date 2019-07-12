# coding:utf8
from baseclass.IterativeRecommender import IterativeRecommender
from random import choice
from tool.qmath import sigmoid
from math import log
from collections import defaultdict


class BPR(IterativeRecommender):
    """2009-BPR-UAI
    BPR：Bayesian Personalized Ranking from Implicit Feedback
    Steffen Rendle,Christoph Freudenthaler,Zeno Gantner and Lars Schmidt-Thieme
    """

    def __init__(self, conf, trainingSet=None, testSet=None, fold='[1]'):
        super(BPR, self).__init__(conf,trainingSet,testSet,fold)

    # def readConfiguration(self):
    #     super(BPR, self).readConfiguration()

    def initModel(self):
        super(BPR, self).initModel()

    def buildModel(self):
        print 'Preparing item sets...'
        self.PositiveSet = defaultdict(dict)
        #self.NegativeSet = defaultdict(list)

        for user in self.data.user:
            for item in self.data.trainSet_u[user]:
                if self.data.trainSet_u[user][item] >= 1:
                    self.PositiveSet[user][item] = 1
                # else:
                #     self.NegativeSet[user].append(item)
        print 'training...'
        iteration = 0
        itemList = self.data.item.keys()
        while iteration < self.maxIter:
            self.loss = 0
            for user in self.PositiveSet:
                # draw u
                u = self.data.user[user]
                for item in self.PositiveSet[user]:
                    # draw i
                    i = self.data.item[item]
                    # draw j
                    item_j = choice(itemList)
                    while self.PositiveSet[user].has_key(item_j):
                        item_j = choice(itemList)
                    j = self.data.item[item_j]
                    # 利用draw的三元组(u,i,j)来优化模型参数
                    self.optimization(u, i, j)
            # 正则化项损失
            self.loss += self.regU * (self.P * self.P).sum() + self.regI * (self.Q * self.Q).sum()
            iteration += 1
            if self.isConverged(iteration):
                break

    # 模型参数优化核心部分
    def optimization(self, u, i, j):
        s = sigmoid(self.P[u].dot(self.Q[i]) - self.P[u].dot(self.Q[j]))
        # update latent features of user u
        self.P[u] += self.lRate * ( (1 - s) * (self.Q[i] - self.Q[j]) - self.regU * self.P[u] )
        # update latent features of item i
        self.Q[i] += self.lRate * ( (1 - s) * self.P[u] - self.regI * self.Q[i] )
        # update latent features of item j
        self.Q[j] -= self.lRate * ( (1 - s) * self.P[u] - self.regI * self.Q[j] )
        # 论文中的优化目标是最大后验概率，添加一个负号就可以转化成我们熟悉的损失函数，所以这里的损失为-log
        self.loss += -log(s)

    def predict(self, user, item):
        if self.data.containsUser(user) and self.data.containsItem(item):
            u = self.data.getUserId(user)
            i = self.data.getItemId(item)
            predictRating = sigmoid(self.Q[i].dot(self.P[u]))
            return predictRating
        else:
            return sigmoid(self.data.globalMean)

    def predictForRanking(self, user):
        'invoked to rank all the items for the user'
        if self.data.containsUser(user):
            u = self.data.getUserId(user)
            return self.Q.dot(self.P[u])
        else:
            return [self.data.globalMean] * self.num_items
