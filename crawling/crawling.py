import os
import time
from datetime import datetime, timedelta

import fire
import pandas as pd
import GetOldTweets3 as got
from emoji_data import EmojiSequence


class Crawler:
    def __init__(self):
        self.Max_Tweet = 300
        self.min_date = datetime.strptime('2017-01-01', '%Y-%m-%d')
        self.max_date = datetime.strptime('2019-12-01', '%Y-%m-%d')

    def run(self, hex_code):
        # Driver code
        not_full = True
        while not_full:
            csv_filenames = [f.split('.')[0] for f in os.listdir('Data/{}'.format(hex_code)) if f[-4:] == '.csv']
            if len(csv_filenames) > 0:
                cur_date = datetime.strptime(min(csv_filenames), '%Y-%m-%d')
            else:
                cur_date = self.min_date
            exists = True
            while exists:
                if cur_date.strftime('%Y-%m-%d') in csv_filenames:
                    cur_date += timedelta(days=1)
                    if cur_date > self.max_date:
                        not_full = False
                        return
                else:
                    exists = False

            print("=== Date: {} -- Collecting {} tweets in Korean ===".format(cur_date.strftime('%Y-%m-%d'), self.Max_Tweet), flush=True)

            start_time = time.time()
            query_emoji = EmojiSequence.from_hex(str(hex_code)).string
            tweet_criteria = got.manager \
                            .TweetCriteria() \
                            .setQuerySearch(query_emoji) \
                            .setSince(cur_date.strftime('%Y-%m-%d')) \
                            .setUntil((cur_date + timedelta(days=1)).strftime('%Y-%m-%d')) \
                            .setMaxTweets(self.Max_Tweet) \
                            .setLang('ko')  

            tweets = got.manager.TweetManager.getTweets(tweet_criteria)
            tweet_list = [[t.text] for t in tweets]

            print("Time taken to collect tweets: {0:0.2f} minutes".format((time.time() - start_time)/60), flush=True)

            tweet_df = pd.DataFrame(tweet_list, columns=['text'])
            tweet_df['text_stripped'] = tweet_df['text'].replace(to_replace=r'pic\S+' ,value='',regex=True) \
                                            .replace(to_replace=r'#\S+' ,value='',regex=True) \
                                            .replace(to_replace=r'@\S+' ,value='',regex=True) \
                                            .replace(to_replace = r'([^ 1-9 ㄱ-ㅣ가-힣]+)', value = '', regex = True)
            tweet_df.to_csv("Data/{}/{}.csv".format(hex_code, cur_date.strftime('%Y-%m-%d')), index=False, encoding='utf-8')

            print("Tweets successfully saved for date {}!".format(cur_date.strftime('%Y-%m-%d')), flush=True)


if __name__ == '__main__':
    fire.Fire(Crawler)