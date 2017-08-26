import langid

def classifySongToLang(song):
    langString = song['lyrics']
    lang = langid.classify(langString,)[0]
    return lang

def isEnglish(song):
    return classifySongToLang(song) == 'en'