from surprise import Reader, Dataset 
import pandas as pd
import surprise
#from surprise.model_selection import cross_validate, train_test_split
from collections import defaultdict
import numpy as np


# NOTES:
    # Add all new users to the filelocation. 
    # Then instantiate this class or run processData function 
    # then use get_top_n() to get the predictions 
class PrimaryAlgorithm:
    uid = None 
    data = None
    filelocation = 'data/ratings.csv'

    def __init__(self):
        df = self.processData()

    def getDataHelper(self): # HELPER FUNCTION 
        try:
            df = pd.read_csv(self.filelocation)
            if np.in1d(np.array(['userId','imdbId','rating']), df.columns).all():
                df = df[['userId','imdbId','rating']]
        except FileNotFoundError as e:
            print("Prim Algorithm - File Not Found - do not return a widget with user based recommendations.")
        except Exception as e:
            print(type(e).__name__, e.args)
            df = pd.DataFrame()
        return df 

    def processData(self):
        df = self.getDataHelper()
        reader = Reader(rating_scale=(0.5,5.0)) # used to parse file containing ratings - REQUIRED 
        data = Dataset.load_from_df(df[['userId','imdbId','rating']],reader).build_full_trainset()
        self.data = data
        #return self.data
    
    def getPredictionsHelper(self,data): # instance of algo 
        algo = surprise.SVD()
        algo.fit(data)
        return algo

    def get_top_n(self, uid, n=10):
        #uid = int(uid)
        df = self.getDataHelper()
        self.processData()
        algo = self.getPredictionsHelper(self.data)

        # get unique movies 
        unique_movies = df['imdbId'].unique() # np 
        user = df.loc[df['userId']==uid, ['imdbId']]
        unique_movies_filtered = np.setdiff1d(unique_movies,user)
        predictions = {}
        # dict of movie_id : prediction 
        for movie_id in unique_movies_filtered:
            predictions[movie_id] =  algo.predict(uid=uid,iid=movie_id).est

        # sort by values high to low 
        top_n = sorted(predictions.items(),key=lambda x: x[1], reverse=True)
        
        return([movie_id for (movie_id, _) in top_n[:n]])

    def test(self):
        #prim = PrimaryAlgorithm()
        df = self.processData()
        top_n = self.get_top_n(114709, 10)
        print(self.get_top_n(114709,10))
#END CLASS 

'''
def getImdbId(mid):
    mid = int(mid)
    df = pd.read_csv('data/links.csv')
    assert 'movieId' in df.columns and 'imdbId' in df.columns
    ind = df[df['movieId']==mid].index.values
    return df.loc[ind,'imdbId'].values[0]

#print(str(getImdbId('1')))
'''

#PrimaryAlgorithm().test()