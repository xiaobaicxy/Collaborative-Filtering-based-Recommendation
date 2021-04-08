# coding = utf-8
import random
import math
from operator import itemgetter

from data_processor import DataProcessor

class ItemBasedCF():
    def __init__(self, n, k):
        self.n = n # top n similar movies
        self.k = k # recommend k movies to user
        self.movie_sim_matrix = {} # similar matrix of movies
        
    # calculate similarity of movies
    def calc_movie_sim(self, train_set):
        print("Calculating movie similarity matrix ...")
        for user in train_set.keys():
            movies = train_set[user].keys()
            for m1 in movies:
                for m2 in movies:
                    if m1 == m2:
                        continue
                    self.movie_sim_matrix.setdefault(m1, {})
                    self.movie_sim_matrix[m1].setdefault(m2, 0)
                    r1 = train_set[user][m1]["rating"]
                    r2 = train_set[user][m2]["rating"]
                    self.movie_sim_matrix[m1][m2] += (10 - abs(r1 - r2))
        print('Calculate movie similarity matrix success!')

    # recommend top k movies to user
    def recommend(self, user, train_set):
        K = self.k
        N = self.n
        rank = {}
        watched_movies = train_set[user].keys()

        for movie in watched_movies:
            for related_movie, similarity in sorted(self.movie_sim_matrix[movie].items(), key=itemgetter(1), reverse=True)[:N]:
                if related_movie in watched_movies:
                    continue
                rating = train_set[user][movie]["rating"]
                rank.setdefault(related_movie, 0)
                rank[related_movie] += similarity * float(rating)
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[:K]


    # eval: calculate precision recall
    def evaluate(self, train_set, test_set):
        print('Evaluating start ...')
        K = self.k
        hit = 0 # hit num
        rec_count = 0 # recommend num
        test_count = 0 # test num
        
        for user in train_set.keys():
            test_moives = test_set.get(user, {})
            rec_movies = self.recommend(user, train_set)
            for movie, _ in rec_movies:
                if movie in test_moives:
                    hit += 1
            rec_count += K
            test_count += len(test_moives)

        precision = hit / (1.0 * rec_count)
        recall = hit / (1.0 * test_count)
        print('precisioin=%.4f\trecall=%.4f' % (precision, recall))

if __name__ == '__main__':
    data_processor = DataProcessor()
    filename = "./datasets/ratings.csv"
    train_set, test_set = data_processor.get_dataset(filename)

    item_cf = ItemBasedCF(n=100, k=20)
    item_cf.calc_movie_sim(train_set)
    item_cf.evaluate(train_set, test_set)