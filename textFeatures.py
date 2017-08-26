import pronouncing
from difflib import SequenceMatcher
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem.porter import PorterStemmer
import valenceArousalCalculator
import rhymeFinder
import nltk
import string
import re
from nltk.corpus import stopwords

contractions = { 
"can't've": "cannot have",
"couldn't": "could not",
"couldn't've": "could not have",
"mightn't've": "might not have",
"mustn't've": "must not have",
"needn't've": "need not have",
"hadn't've": "had not have",
"oughtn't've": "ought not have",
"shan't've": "shall not have",
"shouldn't've": "should not have",
"wouldn't've": "would not have",
"won't've": "will not have",    
"ain't": "am not",
"aren't": "are not",
"can't": "cannot",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hasn't": "has not",
"haven't": "have not",
"isn't": "is not",
"mayn't": "may not",
"mightn't": "might not",
"mustn't": "must not",
"needn't": "need not",
"oughtn't": "ought not",
"shan't": "shall not",
"sha'n't": "shall not",
"shouldn't": "should not",
"wasn't": "was not",
"weren't": "were not",
"won't": "will not",
"wouldn't": "would not",
}

stemmer = PorterStemmer()
negationre = re.compile("not\s+[^\s]*")

def calculateWordsPerSecond(lyrics, seconds):
    return len([token for token in nltk.word_tokenize(lyrics) if token not in string.punctuation])/seconds

def createStemmedLyrics(lines):
    lyrics = " ".join(lines)
    tokens = [stemmer.stem(token) for token in nltk.word_tokenize(lyrics) if token not in string.punctuation]
    # for key in contractions:
    #     if key in lyrics:
    #         lyrics = lyrics.replace(key, contractions[key])
        
    # negations = re.findall(negationre,lyrics)
    # for ne in negations:
    #     words = ne.split()
    #     lyrics = lyrics.replace(ne, 'not'+words[1])
    # tokens = [stemmer.stem(token) for token in nltk.word_tokenize(lyrics) if token not in stopwords.words('english') and token not in string.punctuation]
    return " ".join(tokens)

def calculateLinesRhyming(lines, window):
    numOfLinesRhyming = len(rhymeFinder.findLinesRhyming(lines, window))
    return numOfLinesRhyming/len(lines)

def hasSimilarLine(line, lines, similarityFactor):
    return len([verse for verse in lines if SequenceMatcher(None, line, verse).ratio() >= similarityFactor]) > 1 #it will find itself 

def findRepeatingLines(lines, similarityFactor):
    linesRepeating = [(line, hasSimilarLine(line, lines, similarityFactor)) for line in lines] 
    return [lineTup[0] for lineTup in linesRepeating if lineTup[1]]

def findSections(lyrics):
    return [text.replace("\n", " ") for text in lyrics.split("\n\n")]

def calculateValenceArousal(lines):
    valAr = valenceArousalCalculator.calculateValenceArousal(lines)
    return valAr

def transformPolarity(score):
    if score > 0.2:
        return 1
    if score < -0.2:
        return -1
    return 0

def calculateSentiment(sections):
    sid = SentimentIntensityAnalyzer()
    polarityScores = [sid.polarity_scores(section)['compound'] for section in sections]
    return transformPolarity(sum(polarityScores)/len(polarityScores))

def calculateSectionValenceArousal(sections):
    valArSections = [calculateValenceArousal([section]) for section in sections] #method needs a list as input
    return (sum([s[0] for s in valArSections])/len(sections), sum([s[1] for s in valArSections])/len(sections))

def calculateSyllabicRegularity(lines):
    syllablesCountArr = [0] * 500
    for line in lines:
        syllablesCountArr[countSyllables(line)] = 1
    return sum(syllablesCountArr)/len(lines)
        
def countSyllables(line):
    tokens = [token.lower() for token in nltk.word_tokenize(line) if token not in string.punctuation]
    phones = [pronouncing.phones_for_word(p) for p in tokens]
    return sum([pronouncing.syllable_count(p[0]) for p in phones if len(p)])

def addTextFeatures(classifiedSong, featuresDict):
    lyrics = classifiedSong["lyrics"]
    lines = [x for x in lyrics.split("\n") if x and x.strip()]
    # text
    featuresDict["words_per_sec"] = calculateWordsPerSecond(lyrics, classifiedSong["song_length"])
    featuresDict["lines"] = len(lines)
    featuresDict["lines_rhyming"] = calculateLinesRhyming(lines, 3)
    repeatingLines = findRepeatingLines(lines, 0.8)
    featuresDict["lines_rep"] = len(repeatingLines)/len(lines)
    featuresDict["syllabic_regularity"] = calculateSyllabicRegularity(lines)
    # emotions
    sections = findSections(lyrics)
    valAr = calculateValenceArousal(lines)
    featuresDict["full_valence"] = valAr[0]
    featuresDict["full_arousal"] = valAr[1]
    secValAr = calculateSectionValenceArousal(sections)
    featuresDict["avg_section_valence"] = secValAr[0]
    featuresDict["avg_section_arousal"] = secValAr[1]
    repValAr = calculateValenceArousal(repeatingLines)
    featuresDict["rep_lines_valence"] = repValAr[0]
    featuresDict["rep_lines_arousal"] = repValAr[1]
    featuresDict["sentiment"] = calculateSentiment(sections)
    featuresDict["lyrics"] = createStemmedLyrics(lines)
    return featuresDict

