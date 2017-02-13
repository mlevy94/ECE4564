This is the readme for client.py

to run the program make certain python is installed on the Rpi

run the program using python3 client.py

once run, the program starts a stream that watches the twitter account @4564Team_13

if any tweets are sent to this account with the foramat "@4564Team_13 ##Address:port_"question"" the streamlistener picks up the tweet
and passes it to a wolfram alpha server that looks for answers to the question. if the answer is found the account
tweets a tweet with the format @username "answer"

this program uses the API tweepy to handle the interaction between twitter and the program.
