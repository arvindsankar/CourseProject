import argparse
import datetime

from commands.download import Download
from commands.evaluate import Evaluate
from commands.stream import Stream, StreamSimulator

parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(dest='subcommand')
subparsers.required = True  # required since 3.7


"""
Commands:
      download - Download tweets for a certain topic in a certain time frame
      evaluate - Evaluate sklearn model on labelled dataset
      stream   - Stream Tweets and run model against the incoming tweets
"""

# python tool.py download --topic="Jeopardy" --start_time=2021-12-06T03:00:00 --end_time=2021-12-06T03:30:00 --output demo_tweets
parser_download = subparsers.add_parser('download')
parser_download.add_argument('--topic', required=True,
							  help='Topic for tweets to download.')
parser_download.add_argument('--start_time', required=True,
							  help='Start time to download tweets in ISO format.',
							  type=datetime.datetime.fromisoformat)
parser_download.add_argument('--end_time', required=True,
							  help='End time to download tweets in ISO format.',
							  type=datetime.datetime.fromisoformat)
parser_download.add_argument('--output',
							  help='File path to store downloaded tweets.')

# python tool.py evaluate --model models/Naive_Bayes.joblib --input input_tweets --output output_tweets
parser_evaluate = subparsers.add_parser('evaluate')
parser_evaluate.add_argument('--model', required=True,
							  help='File path to Sklearn model in .joblib format.')
parser_evaluate.add_argument('--input', required=True,
							  help='File path to tweets to evaluate against in format.')
parser_evaluate.add_argument('--output', required=True,
							  help='File path to post tweet_id and sentiment detected.')

# python tool.py stream --topic="Jeopardy" --model models/Naive_Bayes.joblib --output output_tweets
parser_stream = subparsers.add_parser('stream')
parser_stream.add_argument('--topic', required=True,
							help='Topic for tweets to stream.')
parser_stream.add_argument('--model', required=True,
							help='File path to Sklearn model in .joblib format.')
parser_stream.add_argument('--output', required=True,
							help='File path to post tweet_id and sentiment detected.')
parser_stream.add_argument('--duration', default=30,
							help='How long to stream tweets for (in seconds).',
							type=int)

# python tool.py simulate --topic="Jeopardy" --model models/Naive_Bayes.joblib --output output_tweets
parser_simulate = subparsers.add_parser('simulate')
parser_simulate.add_argument('--model', required=True,
							help='File path to Sklearn model in .joblib format.')
parser_simulate.add_argument('--input', required=True,
							help='File path where tweets are read from.')
parser_simulate.add_argument('--output', required=True,
							help='File path to post tweet_id and sentiment detected.')
parser_simulate.add_argument('--duration', default=30,
							help='How long to stream tweets for (in seconds).',
							type=int)

args = parser.parse_args()


if __name__ == '__main__':
	if args.subcommand == 'download':
	    downloader = Download(args.topic, args.start_time, args.end_time, args.output)
	    downloader.execute()
	elif args.subcommand == 'evaluate':
		evaluator = Evaluate(args.model, args.input, args.output)
		evaluator.execute()
	elif args.subcommand == 'stream':
		streamer = Stream(args.topic, args.model, args.output, datetime.timedelta(seconds=args.duration))
		streamer.execute()
	elif args.subcommand == 'simulate':
		simulator = StreamSimulator(args.model, args.input, args.output, datetime.timedelta(seconds=args.duration))
		simulator.execute()
	else:
		raise "Subcommand not found!"
