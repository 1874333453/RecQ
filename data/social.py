from structure import new_sparseMatrix


class SocialDAO(object):
    def __init__(self, conf, relation=list()):
        self.conf = conf
        self.user = {} # used to store the order of users in social network
        self.relation = relation # [(head user, tail user, weight)]
        self.following = {} # users that current user are following
        self.followers = {} # users that follow current user
        self.trustMatrix = self.__generate()

    def __generate(self):
        triple = []
        for line in self.relation:
            userId1, userId2, weight = line
            # add relations to dict
            if not self.following.has_key(userId1):
                self.following[userId1] = {}
            self.following[userId1][userId2] = weight
            if not self.followers.has_key(userId2):
                self.followers[userId2] = {}
            self.followers[userId2][userId1] = weight
            # order the user
            if not self.user.has_key(userId1):
                self.user[userId1] = len(self.user)
            if not self.user.has_key(userId2):
                self.user[userId2] = len(self.user)
            triple.append([self.user[userId1], self.user[userId2], weight])
        return new_sparseMatrix.SparseMatrix(triple)

    def row(self, user):
        # return users that current user are following from the trust matrix
        return self.trustMatrix.row(self.user[user])

    def col(self, user):
        # return current user's followers
        return self.trustMatrix.col(self.user[user])

    def elem(self,u1,u2):
        return self.trustMatrix.elem(u1,u2)

    def weight(self,u1,u2):
        if self.following.has_key(u1) and self.following[u1].has_key(u2):
            return self.following[u1][u2]
        else:
            return 0

    def trustSize(self):
        return self.trustMatrix.size

    def getFollowers(self,u):
        if self.followers.has_key(u):
            return self.followers[u]
        else:
            return {}

    def getFollowees(self,u):
        if self.following.has_key(u):
            return self.following[u]
        else:
            return {}

    def hasFollowee(self,u1,u2):
        if self.following.has_key(u1):
            if self.following[u1].has_key(u2):
                return True
            else:
                return False
        return False

    def hasFollower(self,u1,u2):
        if self.followers.has_key(u1):
            if self.followers[u1].has_key(u2):
                return True
            else:
                return False
        return False
