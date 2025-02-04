'''
Time Decay Model
If Selected;
p = (1-α)p + α
If not selected:
p = (1-α)p
Where p is the selection probablity, α is the degree of weight decrease.
'''

import news_classes
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient

NUM_OF_CLASSES = 17
INITIAL_P = 1.0 / NUM_OF_CLASSES
ALPHA = 0.1

SLEEP_TIME_IN_SECONDS = 1

LOG_CLICK_TASK_QUEUE_URL = 'amqps://ejghaimx:q87sIhf2vRU55dEUNgMYFy7cXlmDYFE1@snake.rmq2.cloudamqp.com/ejghaimx'
LOG_CLICK_TASK_QUEUE_NAME = "log-click-task-queue"

PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"
NEWS_TABLE_NAME = "news"

click_queue_client = CloudAMQPClient(LOG_CLICK_TASK_QUEUE_URL, LOG_CLICK_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        return 
    if ('userId' not in msg
        or 'newsId' not in msg
        or 'timestamp' not in msg):
        return
    
    userId = msg['userId']
    newsId = msg['newsId']

    db = mongodb_client.get_db()
    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId': userId})

    if model is None:
        print('Creating preference model for new user: {}'.format(userId))
        new_model = {'userId': userId}
        preference = {}
        for i in news_classes.classes:
            preference[i] = float(INITIAL_P)
        new_model['preference'] = preference
        model = new_model

    print("Updating preference model for user {}".format(userId))
    # Update preference model using time decay model
    news = db[NEWS_TABLE_NAME].find_one({'digest': newsId})
    if (news is None
        or 'class' not in news
        or news['class'] not in news_classes.classes):
        print(news is None)
        print('class' not in news)
        print(news['class'] not in news_classes.classes)
        print("Skipping processing...")
        return

    click_class = news['class']

    old_p = model['preference'][click_class]
    model['preference'][click_class] = float((1 - ALPHA) * old_p + ALPHA)

    for i, prob in model['preference'].items():
        if not i == click_class:
            model['preference'][i] = float(
                (1 - ALPHA) * model['preference'][i])
    
    db[PREFERENCE_MODEL_TABLE_NAME].replace_one({'userId': userId}, model, upsert=True)


def run():
    while True:
        if click_queue_client is not None:
            msg = click_queue_client.getMessage()
            if msg is not None:
                try:
                    handle_message(msg)
                except Exception as e:
                    print(e)
                    pass
            click_queue_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == "__main__":
    run()