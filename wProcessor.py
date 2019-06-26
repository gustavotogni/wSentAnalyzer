import nltk
from nltk.text import Text
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 
from nltk.util import ngrams
import re
import string
from string import punctuation 
import pandas as pd
from wPlotter import wPlotter

class wProcessor:

    def __init__(self, outputPath):
        self._stopwords = set(stopwords.words('english') + list(punctuation) + ['AT_USER','URL','...','quot'])
        self._classifier = None
        self._outputPath = outputPath
        self._plotter = wPlotter(outputPath)
        
    def prepMsgList(self, message):

        try:
            processedContents = message.lower() # convert text to lower-case
            processedContents = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', processedContents) # remove URLs
            processedContents = re.sub('@[^\s]+', 'AT_USER', processedContents) # remove usernames
            processedContents = re.sub(r'#([^\s]+)', r'\1', processedContents) # remove the # in #hashtag]
            processedContents = re.sub("'","", processedContents) # remove ' which breaks the tokenization
            processedContents = word_tokenize(processedContents) # remove repeated characters (helloooooooo into hello)            
            processedContents = [word for word in processedContents if word not in self._stopwords]

            return processedContents

        except:
            print("Unexpected error parsing the following record from the training file:")
            print(message)
            return ""
        
    def getMsgFeatures(self, msgTokens):

        gText = Text(msgTokens)
        msgContent = ' '.join(msgTokens)
        
        features = {}
        features['length'] = len(msgContent)
        features['lexdiv'] = self.getLexicalDiversity(gText)
        features['longestword'] = self.getLongestWord(msgContent)

        for token in msgTokens:
            wordCount = msgContent.lower().count(token)
            if (wordCount > 1):
                features["repeats({})".format(token)] = wordCount

        for unigram in msgTokens:
                features["unigram({})".format(unigram)] = True

        for bigram in self.getBigrams(msgTokens):
            features["bigram({})".format(bigram)] = True

        for trigram in self.getTrigrams(msgTokens):
            features["trigram({})".format(trigram)] = True

        return features

    # Unique words / total words ratio
    def getLexicalDiversity(self, text):

        textLength = len(text)
        if (textLength > 0):
            return len(set(text)) / len(text)
        else:
            return 0    

    def getBigrams(self, tokens):
        return list(ngrams(tokens, 2))

    def getTrigrams(self, tokens):
        return list(ngrams(tokens, 3))

    def getLongestWord(self, sen):

        for char in string.punctuation:
            sen = sen.replace(char, ' ')
        
        text = sen.split()
        text.sort(key = lambda x: len(x))

        try:
            return text[-1]
        except:
            return ""

    def classifyMsgList(self, msgList):

        if (self._classifier is None):
            self.trainNewClassifier()

        msgList['features'] = msgList['tokens'].apply(self.getMsgFeatures)
        msgList['sentiment'] = msgList['features'].apply(self._classifier.classify)

        self._plotter.mpsTreeMap(msgList, '# of msg. per Sentiment', 'ClassifiedDs')
        self._plotter.fdistCumulative(msgList, "Word Freq. Distribution", 'ClassifiedDs')
        self._plotter.fdistByGroup(msgList.groupby('sentiment')[['tokens']].sum(), "Word Freq. Distribution", "ClassifiedDs")
        
        return msgList

    def trainNewClassifier(self):

        trainingMsgDf = pd.read_csv(
            'training.csv',
            sep = ',',
            names = [
                'tweet_id',
                'sentiment',
                'author',
                'content'
            ],
            usecols = [
                'content',
                'sentiment'
            ],
            skiprows = 1
        )

        trainingMsgDf['length'] = trainingMsgDf['content'].apply(len)
        trainingMsgDf['tokens'] = trainingMsgDf['content'].apply(self.prepMsgList)

        self._plotter.mpsTreeMap(trainingMsgDf, '# of msg. per Sentiment', 'TrainingDs')                
        self._plotter.fdistCumulative(trainingMsgDf, "Word Freq. Distribution", 'TrainingDs')       
        self._plotter.fdistByGroup(trainingMsgDf.groupby('sentiment')[['tokens']].sum(), "Word Freq. Distribution", "TrainingDs")        
        
        trainingDsMsgFeatures = [(self.getMsgFeatures(tokens), sentiment) for (sentiment, content, length, tokens) in trainingMsgDf.values]    
        
        trainingDsTrainSet = trainingDsMsgFeatures[0:39000]
        trainingDsTestSet = trainingDsMsgFeatures[39000:40000]

        nbClassifier = nltk.NaiveBayesClassifier.train(trainingDsTrainSet)

        print("NaiveBayesClassifier trained.")
        print("Full feature set example:")
        print(trainingDsTrainSet[0])
        print("Accuracy:")
        print(nltk.classify.accuracy(nbClassifier, trainingDsTestSet))
        print("Labels:")
        print(nbClassifier.labels())
        nbClassifier.show_most_informative_features(25)
        
        errors = []
        for (msg, tag) in trainingDsTestSet:       
            guess = nbClassifier.classify(msg)
            if guess != tag:
                errors.append((tag, guess, msg))

        self._classifier = nbClassifier