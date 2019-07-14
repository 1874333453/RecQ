from baseclass.IterativeRecommender import IterativeRecommender
from data.social import SocialDAO
from tool import config
from os.path import abspath


class SocialRecommender(IterativeRecommender):
    """Align users from two data source.

    Remove users who don't appear in user-item interactions from social relations.

    Attributes:
        social: Data access object of social relations.
    """

    def __init__(self, conf, trainingSet, testSet, relation, fold='[1]'):
        super(SocialRecommender, self).__init__(conf, trainingSet, testSet, fold)
        self.social = SocialDAO(self.config, relation)
        # data clean
        cleanList = []
        cleanPair = []
        # remove users that only appear in social network from following view
        for user in self.social.following:
            if not self.data.user.has_key(user):
                cleanList.append(user)
            for u2 in self.social.following[user]:
                if not self.data.user.has_key(u2):
                    cleanPair.append((user, u2))
        for u in cleanList:
            del self.social.following[u]
        for pair in cleanPair:
            if self.social.following.has_key(pair[0]):
                del self.social.following[pair[0]][pair[1]]
        cleanList = []
        cleanPair = []
        # remove users that only appear in social network from followers view
        for user in self.social.followers:
            if not self.data.user.has_key(user):
                cleanList.append(user)
            for u2 in self.social.followers[user]:
                if not self.data.user.has_key(u2):
                    cleanPair.append((user, u2))
        for u in cleanList:
            del self.social.followers[u]
        for pair in cleanPair:
            if self.social.followers.has_key(pair[0]):
                del self.social.followers[pair[0]][pair[1]]

    def readConfiguration(self):
        super(SocialRecommender, self).readConfiguration()
        regular = config.LineConfig(self.config['reg.lambda'])
        self.regS = float(regular['-s'])

    def printAlgorConfig(self):
        super(SocialRecommender, self).printAlgorConfig()
        print 'Social dataset:',abspath(self.config['social'])
        print 'Social size ','(User count:',len(self.social.user),'Trust statement count:'+str(len(self.social.relation))+')'
        print 'Social Regularization parameter: regS %.3f' % (self.regS)
        print '=' * 80
