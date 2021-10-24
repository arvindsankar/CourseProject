# CourseProject

Sentiment Analysis is used to identify the sentiments of the text source. Very commonly, Tweets are used in collecting lots of data for performing sentiment analysis. They can help us understand the opinions and perspectives of various people about a particular topic. The task is to capture the sentiments of the data by developing a ML pipeline and then evaluate the results of the model.

We will use the Twitter Historical Tweet APIs [1] to provide a dataset of tweets on a show like “Squid Game” for a definitive timeline. After collecting a substantial dataset, we will hand label the tweet data and mark it as positive or negative sentiment. We can then do analysis and preprocess the tweets to prepare for a specific model. The model created can be validated and then evaluated with F1 Score (precision and recall).

We will evaluate the data on streaming data via the Twitter Streaming APIs [2]. As tweets for a topic appear in real time, the model will evaluate each tweet as positive or negative. After the tweets stream, we can hand label them and evaluate the accuracy of our model. If we choose to evaluate multiple models, we can measure evaluation speed as another metric.

This task is interesting since it could allow people to measure audience sentiment in real time. If a show is airing, producers of the show can use this tool to understand what the audience thinks of each scene. This would give them a level of insight that would make subsequent episodes more engaging for the audience.

Dataset: We will be using Twitter data for the project
Tools: For streaming, scrapping and stemming Python can be used for data in real time.
Evaluation: We will evaluate using Precision/Recall measures.
