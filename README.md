
# CourseProject

## Abstract

Sentiment Analysis is used to identify the sentiments of the text source. Tweets can be a very informative data source to collect data on a variety of opinion holders to sentiment analysis. They can help us understand the opinions and perspectives of various people on virtually any topic. There are over **200 million** twitter users with tweets we can mine in real time to get a real time view of how a sample of the population feels about a certain topic.  Holistically, our task was to build an ML pipeline and sentiment analysis model that can be trained on tweets, and to build a system that can use the model to predict the sentiment of tweets as they appear in real time.

## Pointers for Grader
Project Report - TODO
Video - https://www.youtube.com/watch?v=q64aoTrx_Zg

To install this on your system, please use conda. After cloning and entering the CourseProject directory follow these steps.

```console
conda create --name demo python=3.8
conda activate demo
pip install -r requirements.txt
```

After requirements have been installed, you should be able to run through the notebook and run the system. Unless you have Twitter API keys, you should only look at the "evaluate" and "simulate" commands of the tool listed below. If you do have twitter API keys, feel free to run any of the commands documented below.

## Usage

We have written a wrapper around our system for the grader to use to run the code to collect tweets, evaluate the model, stream tweets, and simulate evaluating in real time.

There are four modes to use our tool:

```console
foo@bar % python tool.py --help

usage: tool.py [-h] {download,evaluate,stream,simulate} ...

positional arguments:

{download,evaluate,stream,simulate}

optional arguments:

-h, --help  show this help message and exit
```

### Download Mode (Requires Twitter API keys)

```console
usage: tool.py download [-h] --topic TOPIC --start_time START_TIME --end_time END_TIME [--output OUTPUT]

-h, --help  show this help message and exit
--topic TOPIC Topic for tweets to download.
--start_time START_TIME Start time to download tweets in ISO format.
--end_time END_TIME End time to download tweets in ISO format.
--output OUTPUT File path to store downloaded tweets.
```

As the names and arguments suggest, we can use this mode to download tweets from a given topic in the time range (START_TIME, END_TIME). This is implemented with the Twitter Search API. **NOTE: the Twitter Developer API keys only allow us to retrieve data from up to 7 days ago. If you need data from even earlier, you will need to use an Academic Researcher API account**.

Remember to pass the start time and end time in ISO format! Here is an example command you may use (adjust the date so you are retrieving data from within the last 7 days).

```console
python tool.py download --topic="Jeopardy" --start_time=2021-12-06T03:00:00 --end_time=2021-12-06T03:30:00 --output demo_tweets
```

### Evaluate Mode 

```console
usage: tool.py evaluate [-h] --model MODEL --vectorizer VECTORIZER --input INPUT --output OUTPUT

-h, --help  show this help message and exit
--model MODEL File path to Sklearn model in .joblib format.
--vectorizer VECTORIZER File path to Sklearn vectorizer in .joblib format.
--input INPUT File path to tweets to evaluate against in format.
--output OUTPUT File path to post tweet_id and sentiment detected.
```

We can use this mode to evaluate pre-trained models on an input file of tweets and produce and output file that contains the output of the model. Note we use a the joblib sklearn package to serialize and deserialize our models. Documentation on this package can be found here: https://joblib.readthedocs.io/en/latest/

The Vectorizer provided is used to transform a string of text into something more similar to bag of words model. (Our example one uses TF-IDF weighting that we learned in the Text Retrieval section of our class!) Here are some example commands you can try to use our models to evaluate some tweets.

The models we will used are stored here:
```console
(base) foo@bar % ls models
LogisticR_model.joblib  Naive_Bayes.joblib  vectorizer.joblib
```

Here's what the input data looks like:

```
(base) foo@bar CourseProject % head examples/input_data.csv
Mayim Bialik is back #Jeopardy! https://t.co/Vz5FhkUBYG
@ReallyAmerican1 Garland is building a case. \nwe don't want to go in all HalfAss. \nDouble Jeopardy applies  \neven in this case
RT @OccupyDemocrats: BREAKING: Amy Schneider becomes the first openly trans person in history to make it into Jeopardy's "Tournament of Cha\u2026
RT @Ian_R_Williams: @dispositive? I know him! Beloved Law School Professor Making Jeopardy Debut Tonight https://t.co/XXGQTs3n5x
The latest My Playful News! https://t.co/OMPtg2O2n3 Thanks to @GF_Films @CallMeCarsonYT @_thejeopardyfan #jeopardy #funko
Ok  have seen both hosts now Ken  and Mayim Bialik.\n\nPrefer Mayim \n\n#Jeopardy
@2ndHandBookery Multiple people said Clue and it makes me so happy. That\u2019s on my list  also Death Becomes Her  The Big Lebowski  Goodfellas and Double Jeopardy. So many more but I\u2019ll stick with those \U0001f602
Another article. https://t.co/kfTaCSLmFb
@Bree_AndersenXO @FeelFreeToPanic He's just toying with  them now  He really thinks he won with CPS.He is putting that baby in jeopardy of being taken away and he doesn't care
@bklvr70 @ryanlcooper I'm of this opinion. I can understand  though  that drs and hospitals are reluctant to put themselves in legal jeopardy by refusing  esp. with the red legislatures eager to lynch medicos for Fox points.
```

Use this command to run our model and vectorizer on this input and store the output to a file called 'output_tweets'.

```console
python tool.py evaluate --model models/Naive_Bayes.joblib --input examples/input_data.csv --output output_tweets --vectorizer models/vectorizer.joblib
```

Here’s what the output data looks like:

```console
(base) foo@bar CourseProject % head output_tweets

0,Mayim Bialik is back #Jeopardy! https://t.co/Vz5FhkUBYG
0,@ReallyAmerican1 Garland is building a case. \nwe don't want to go in all HalfAss. \nDouble Jeopardy applies  \neven in this case
1,RT @OccupyDemocrats: BREAKING: Amy Schneider becomes the first openly trans person in history to make it into Jeopardy's "Tournament of Cha\u2026
0,RT @Ian_R_Williams: @dispositive? I know him! Beloved Law School Professor Making Jeopardy Debut Tonight https://t.co/XXGQTs3n5x
0,The latest My Playful News! https://t.co/OMPtg2O2n3 Thanks to @GF_Films @CallMeCarsonYT @_thejeopardyfan #jeopardy #funko
1,Ok  have seen both hosts now Ken  and Mayim Bialik.\n\nPrefer Mayim \n\n#Jeopardy
1,@2ndHandBookery Multiple people said Clue and it makes me so happy. That\u2019s on my list  also Death Becomes Her  The Big Lebowski  Goodfellas and Double Jeopardy. So many more but I\u2019ll stick with those \U0001f602
0,Another article. https://t.co/kfTaCSLmFb
1,@Bree_AndersenXO @FeelFreeToPanic He's just toying with  them now  He really thinks he won with CPS.He is putting that baby in jeopardy of being taken away and he doesn't care
1,@bklvr70 @ryanlcooper I'm of this opinion. I can understand  though  that drs and hospitals are reluctant to put themselves in legal jeopardy by refusing  esp. with the red legislatures eager to lynch medicos for Fox points.
```

The integer 0 or 1 before the tweet on each line denotes the sentiment the model gives. In our case, the 0 denotes a negative sentiment and 1 denotes a positive one.

### Stream Mode (Requires Twitter API keys)

```console
usage: tool.py stream [-h] --topic TOPIC --model MODEL --vectorizer VECTORIZER --output OUTPUT [--duration DURATION]

  -h, --help            show this help message and exit
  --topic TOPIC         Topic for tweets to stream.
  --model MODEL         File path to Sklearn model in .joblib format.
  --vectorizer VECTORIZER
                        File path to Sklearn vectorizer in .joblib format.
  --output OUTPUT       File path to post tweet_id and sentiment detected.
  --duration DURATION   How long to stream tweets for (in seconds).
```

We can use this mode to evaluate pre-trained models on a stream of incoming tweets and produce and output file that contains the output of the model. Note we use a the joblib sklearn package to serialize and deserialize our models. Documentation on this package can be found here: https://joblib.readthedocs.io/en/latest/

The Vectorizer provided is used to transform a string of text into something more similar to bag of words model. (Our example one uses TF-IDF weighting that we learned in the Text Retrieval section of our class!) Here are some example commands you can try to use our models to run models on a stream of tweets.

```console
python tool.py stream --topic="cats" --model models/Naive_Bayes.joblib --output output_tweets  --vectorizer models/vectorizer.joblib --duration 30
```

This command will download a stream of *real-time* tweets for 30 seconds on the topic "cats". This means any tweet with the word "cat" will get parsed, evaluated and the result will be stored in the output_tweets file.

The integer 0 or 1 before the tweet on each line of the output_tweet file denotes the sentiment the model gives. In our case, the 0 denotes a negative sentiment and 1 denotes a positive one.

### Simulate Mode

```
usage: tool.py simulate [-h] --model MODEL --vectorizer VECTORIZER --input INPUT --output OUTPUT [--duration DURATION]

-h, --help  show this help message and exit
--model MODEL File path to Sklearn model in .joblib format.
--vectorizer VECTORIZER File path to Sklearn vectorizer in .joblib format.
--input INPUT File path where tweets are read from.
--output OUTPUT File path to post tweet_id and sentiment detected.
--duration DURATION How long to stream tweets for (in seconds).
```

Since the stream mode requires the user to have Twitter API keys, we have created another mode for the reader to try our system that does not require them. This mode is just like the Stream Mode but it uses a stream simulator to read tweets from a file and send the tweets to our model process over some duration in a random way. For details on how this is implemented, please read the project documentation.

```console
python tool.py simulate --model models/Naive_Bayes.joblib --output output_tweets --input examples/input_data.csv --vectorizer models/vectorizer.joblib --duration 30
```

This command will send the tweets in the example directory to the model process and records the results to the output_tweets file with the sentiment recorded.

Here is an example with the sentiment:

```console
(base) foo@bar CourseProject % head output_tweets

0,@JeopardyGuesser @missmayim #blindguess #Jeopardy going with Dadaism\t\t\t\t\t\t\t\t\n
1,RT @HowardU: Tune in TOMORROW\tDec. 7th! HU\\u2019s very own Dr. John Harkless\tassociate professor\tDepartment of Chemistry\twill appear as a co\\u2026\t\t\t\t\n
0,@bklvr70 @ryanlcooper I'm of this opinion. I can understand\tthough\tthat drs and hospitals are reluctant to put themselves in legal jeopardy by refusing\tesp. with the red legislatures eager to lynch medicos for Fox points.\t\t\t\t\t\n
1,RT @QuakeMedia: "Jeopardy!" contestant Amy Schneider (@jeopardyamy) making history as the first trans-woman to qualify for the #TournamentO\\u2026\t\t\t\t\t\t\t\t\n
1,RT @madimoukas: Coming out of tweeting retirement for @KenJennings. For the love of god please make this man the host and stop toying with\\u2026\t\t\t\t\t\t\t\t\n
0,@richjhewitt #Jeopardy https://t.co/NyI7bwtTKR\t\t\t\t\t\t\t\t\n
1,Watching the news is depressing. I never thought in my lifetime that we could lose our democracy in the United States! Yes\tthe USA is in jeopardy of a take over of our government and the Republican party and a hugh portion of Americans seem to be okay with it. Wake up!\t\t\t\t\t\t\t\n
1,@Jeopardy @missmayim. It is a common error\tbut Farsi is neither the official language of Persia nor the same as Persian.  Persian is Persian and Farsi is Farsi.  Today\\u2019s game perpetuates the misunderstanding that Farsi is a common name for Persian. They are not interchangeable.\t\t\t\t\t\t\t\n
1,Girl Groups is a category on Jeopardy right now and all I wanted was for The Runaways to be an answer\tit was the $2000 clue and NO ONE GOT IT.\t\t\t\t\t\t\t\n
0,@Jeopardy Yes\tit was great!\t\t\t\t\t\t\t\n
```

### Creation of Models

Creation of pre-trained models is found in the notebook/ directory. This includes preprocessing, training and testing of the models.

The prefetched dataset consisting of around 2000 tweets is used. The various columns in dataset are
·   	tweetId: unique Id of tweet
·   	date: tweet date
·   	polarity: sentiment of tweet. Either 1 or 0
·   	fulltweet: the text of the tweet
For creating the models suggest running the notebook provided under the notebook folder. We need python version 3.6 and miniconda,  a free minimal installer for conda which can be downloaded from here- https://docs.conda.io/en/latest/miniconda.html.
Create a new conda environment and install jupyter notebook and other dependencies. Start Jupyter notebook.
```console
conda create -n my-conda-env                 # creates new virtual env
conda activate my-conda-env                   # activate environment in terminal
conda install jupyter                         # install jupyter + notebook

conda install numpy
conda install pandas
conda install nltk
​​conda install -c conda-forge matplotlib
conda install -c conda-forge wordcloud
conda install seaborn
conda install scikit-learn

jupyter notebook                  # start server + kernel inside my-conda-env
```
Importing dependencies for creating models-
```console
import csv
import re
import html
import nltk
from csv import writer
from ast import literal_eval
import numpy as np
import pandas as pd
import pylab as pl
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud, STOPWORDS
%matplotlib inline
%config InlineBackend.figure_format = 'retina'
#Machine learning
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
```

Once the dependencies are imported we can read and load the labelled dataset provided under folder ‘notebook’ (week1_labelled_tweets2.csv and week2_labelled_tweets2.csv). Loading the dataset the notebook (K_load_preprocess_training.ipynb) can be run in a step wise manner as directed here - https://github.com/arvindsankar/CourseProject/tree/main/notebook

The data is analyzed and cleaned. Cleaning is done by removing urls, html codes, hashtags, mentions, stopwords. Stemming and Lemmatization is then applied on data. 

After cleaning, the data is split into training and testing subsets. The Vectorizer provided is used to transform a string of text into something more similar to a bag of words model. (Our example one uses TF-IDF weighting that we learned in the Text Retrieval section of our class!). 
```console
X=df.fulltweet
y=df.polarity
X_training, X_testing, y_training, y_testing = split_into_training(X,y)

vectorize_train_test = TfidfVectorizer(ngram_range=(1,2), max_features=1000)
vectorize_train_test.fit(X_training)
X_training = vectorize_train_test.transform(X_training)
X_testing  = vectorize_train_test.transform(X_testing)
```
Once the models are trained they are used to evaluate test data. 
Training Naive Bayes model
```console
# Training Naive Bayes model
NB_model = MultinomialNB()
NB_model.fit(X_training, y_training)
evaluate_model_values(NB_model)
y_predict1 = NB_model.predict(X_testing)
print('Accuracy Score of Naive Bayes:',accuracy_score(y_testing, y_predict1))
```
Training Logistic Regression model
```console
# Training Logistic Regression model
LogisticR_model = LogisticRegression(solver='lbfgs')
LogisticR_model.fit(X_training, y_training)
evaluate_model_values(LogisticR_model)
y_predict2 = LogisticR_model.predict(X_testing)
print('Accuracy Score of LogisticRegression:',accuracy_score(y_testing, y_predict2))
```
The following are the precision, recall and F1 scores generated by Naïve Bayes and LogisticRegression models we created-
```console
              precision    recall  f1-score   support

         0.0       0.84      0.82      0.83       130
         1.0       0.76      0.78      0.77        93

    accuracy                           0.81       223
   macro avg       0.80      0.80      0.80       223
weighted avg       0.81      0.81      0.81       223

Accuracy Score of Naive Bayes: 0.8071748878923767
```
```console
      precision    recall  f1-score   support

         0.0       0.93      0.81      0.86       130
         1.0       0.77      0.91      0.84        93

    accuracy                           0.85       223
   macro avg       0.85      0.86      0.85       223
weighted avg       0.86      0.85      0.85       223

Accuracy Score of LogisticRegression: 0.852017937219731
```

Once the models are trained and tested they are serialized using skc package to evaluate data. Note we use the joblib sklearn package to serialize and deserialize our models. Documentation on this package can be found here: https://joblib.readthedocs.io/en/latest/
```console
from joblib import dump, load
dump(NB_model, 'NB_model.joblib') 
dump(LogisticR_model, 'LogisticR_model.joblib')
dump(vectorize_data_file, 'vectorizer.joblib')
```
