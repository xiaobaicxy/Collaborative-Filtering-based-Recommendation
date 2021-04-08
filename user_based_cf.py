# coding = utf-8
import random
import math
from operator import itemgetter

from data_processor import DataProcessor

class UserBasedCF():
    def __init__(self, n, k):
        self.n = n # top n similar users
        self.k = k # recommend k movies to user
        self.user_sim_matrix = {} # similar matrix of users

    # calculate similarity of users
    def calc_user_sim(self, train_set):
        print('Creating movie-user dict...')
        movie_user = {}
        for user, movies in train_set.items():
            for movie in movies:
                if movie not in movie_user:
                    movie_user[movie] = set()
                movie_user[movie].add(user)
        print('Create movie-user dict success!')

        print('Calculating user similarity matrix ...')
        for movie, users in movie_user.items():
            for u in users:
                for v in users:
                    if u == v:
                        continue
                    self.user_sim_matrix.setdefault(u, {})
                    self.user_sim_matrix[u].setdefault(v, 0)
                    r1 = train_set[u][movie]["rating"]
                    r2 = train_set[v][movie]["rating"]
                    self.user_sim_matrix[u][v] += (10 - abs(r1 - r2))
        print('Calculate user similarity matrix success!')

    # recommend top k movies to user
    def recommend(self, user, train_set):
        K = self.k
        N = self.n
        rank = {}
        watched_movies = train_set[user].keys()

        for related_user, similarity in sorted(self.user_sim_matrix[user].items(), key=itemgetter(1), reverse=True)[0:N]:
            for movie in train_set[related_user]:
                if movie in watched_movies:
                    continue
                rating = train_set[related_user][movie]["rating"]
                rank.setdefault(movie, 0)
                rank[movie] += similarity * float(rating)
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[0:K]


    # eval: calculate precision recall
    def evaluate(self, train_set, test_set):
        print("Evaluation start ...")
        K = self.k
        hit = 0 # hit num
        rec_count = 0 # recommend num
        test_count = 0 # test num
        
        for i, user, in enumerate(train_set):
            test_movies = test_set.get(user, {})
            rec_movies = self.recommend(user, train_set)
            for movie, _ in rec_movies:
                if movie in test_movies:
                    hit += 1
            rec_count += K
            test_count += len(test_movies)

        precision = hit / (1.0 * rec_count)
        recall = hit / (1.0 * test_count)
        print('precisioin=%.4f\trecall=%.4f' % (precision, recall))

if __name__ == '__main__':
    data_processor = DataProcessor()
    filename = "./datasets/ratings.csv"
    train_set, test_set = data_processor.get_dataset(filename)

    user_cf = UserBasedCF(n=100, k=20)
    user_cf.calc_user_sim(train_set)
    user_cf.evaluate(train_set, test_set)