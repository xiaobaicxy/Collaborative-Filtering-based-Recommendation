# coding = utf-8
import pandas as pd
import random

class DataProcessor:
    # create train set and test set
    def get_dataset(self, filename, pivot=0.75):
        print("Creating dataset...")
        train_set = {}
        test_set = {}
        train_set_size = 0
        test_set_size = 0
        for (user, movie, rating, timestamp) in self.load_file(filename):
            if(random.random() < pivot):
                train_set.setdefault(user, {})
                train_set[user][movie] = {"rating": rating}
                train_set_size += 1
            else:
                test_set.setdefault(user, {})
                test_set[user][movie] = {"rating": rating}
                test_set_size += 1
        
        print('train set size = %s' % train_set_size)
        print('test set size = %s' % test_set_size)
        print('Create dataset success!')
        return train_set, test_set

    # read csv file
    def load_file(self, filename):
        csvfile = open(filename, encoding='utf-8')
        df = pd.read_csv(csvfile, engine='python', nrows=100000)
        for idx in range(len(df)):
            user = df["userId"][idx]
            movie = df["movieId"][idx]
            rating = df["rating"][idx]
            timestamp = df["timestamp"][idx]
            yield (user, movie, rating, timestamp)

if __name__ == "__main__":
    data_processor = DataProcessor()
    filename = "./datasets/ratings.csv"
    train_set, test_set = data_processor.get_dataset(filename)
    for user in test_set.keys():
        for movie in test_set[user].keys():
            rating = test_set[user][movie]["rating"]
            print(user, movie, rating)
            break
        break
