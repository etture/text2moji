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
        if not os.path.exists(hex_code):
            os.makedirs(hex_code)

        not_full = True
        while not_full:
            csv_filenames = [f.split('.')[0] for f in os.listdir('data/{}'.format(hex_code)) if f[-4:] == '.csv']
            if len(csv_filenames) > 0:
                cur_date = datetime.strptime(min(csv_filenames), '%Y-%m-%d')
            else:
                cur_date = self.min_date
            exists = True
            while exists:
                if cur_date.strftime('%Y-%m-%d') in csv_filenames:
                    cur_date += timedelta(days=1)
                    if cur_date > self.max_date:
                        return
                else:
                    exists = False

            tweet_criteria = got.manager \
                            .TweetCriteria() \
                            .setQuerySearch(hex_code) \
                            .setSince(cur_date) \
                            .setUntil(cur_date + timedelta(days=1)) \
                            .setMaxTweets(self.Max_Tweet) \
                            .setLang('ko')  

            tweets = got.manager.TweetManager.getTweets(tweet_criteria)
            tweet_list = list()
            for tweet in tweets:
                content = tweet.text
                tweet_list.append([content])
                time.sleep(0.2)
            tweet_df = pd.DataFrame(tweet_list, columns=['text'])
            tweet_df['text_stripped'] = tweet_df['text'].replace(to_replace=r'pic\S+' ,value='',regex=True) \
                                            .replace(to_replace=r'#\S+' ,value='',regex=True) \
                                            .replace(to_replace=r'@\S+' ,value='',regex=True) \
                                            .replace(to_replace = r'([^ 1-9 ㄱ-ㅣ가-힣]+)', value = '', regex = True)
            tweet_df.to_csv("data/{}/{}.csv".format(hex_code, cur_date.strftime('%Y-%m-%d')), index=False, encoding='utf-8')


if __name__ == '__main__':
    fire.Fire(Crawler)