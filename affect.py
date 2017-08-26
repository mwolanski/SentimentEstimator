# import pickle
# import json
# import sys
import os
from nltk.stem.porter import PorterStemmer
# import valenceArousalCalculator
# import rhymeFinder
import nltk
import string
from nltk.corpus import stopwords
import re

stemmer = PorterStemmer()
negationre = re.compile("not\s*[^\s]*")
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


text = "The wouldn't've, tuple regex_strings. defines a defining list of!! regular or isn't wasn't ever ain't expression  o'clock and strings."


print(createStemmedLyrics(text))
# # string.punctuation
# for key in contractions:
#     if key in text:
#         text = text.replace(key, contractions[key])
# negations = re.findall("not\s*[^\s]*",text)
# for ne in negations:
#     words = ne.split()
#     text = text.replace(ne, 'not'+words[1])
# print(text)
# text = nltk.word_tokenize(text)
# print([word for word in text if word not in stopwords.words('english') and word not in string.punctuation])
# print(text)
# if __name__ == '__main__':
#     sys.stdout = open('tagsFilterOutput.txt','wt')
#     tagsFilter = TagsFilter.TagsFilter()
#     tagsFilter.filterTagsFromAllSongs()

#     print('hello')

#loader = filesLoader.recursive_file_gen('./tagsFiles')
#filterTagsFromOneSong(next(loader))

# print('中文')

# result = pickle.load(open('data.pkl', 'rb'))
# print('hello')

