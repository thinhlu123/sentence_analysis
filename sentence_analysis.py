import spacy
from spacy.matcher import Matcher
import ast
import re
from predict import get_prediction

import pathlib
path = pathlib.Path(__file__).parent.absolute()
class separateEntity:
    def __init__(self):
        self.sp = spacy.load('en_core_web_sm')

        self.matcher = Matcher(self.sp.vocab)
        
        fW = open(str(path) + "/rule-what.txt", "r")
        for lineW in fW:
            pattern = ast.literal_eval(lineW)
            self.matcher.add('WHAT_QUESTION', None, pattern)
        fH = open(str(path) + "/rule-how.txt", "r")
        for line in fH:
            pattern = ast.literal_eval(line)
            self.matcher.add('HOW_QUESTION', None, pattern)

    def getObject(self, doc):
        sen = self.sp(doc)
        objectSen = []
        nou = sen.noun_chunks
        pronoun = ["i","she","he","them","they","it","its","mine"]
        for n in nou:
            if any(n.text.lower() in s for s in pronoun):continue
            if n.text.lower() != "photoshop" or n.text.lower() != "ps":
                objectSen.append(n.text)
        # for word in self.sen:
        #     if word.pos_ == "NOUN" or (word.pos_ == "PROPN" and word.text.lower() != "photoshop" and "." not in word.text): 
        #         objectSen.append(word.text)
        return objectSen
    def getAction(self, doc):
        sen = self.sp(doc)
        actionSen = []
        for word in sen:
            if word.pos_ == "VERB": 
                actionSen.append(word.text)
        return actionSen
    def getTitle(self, doc):
        sen = self.sp(doc)
        title = ""
        for word in sen:
            if word.pos_ == "NOUN" or (word.pos_ == "PROPN" and word.text.lower() != "photoshop") or word.pos_ == "VERB" or word.pos_ == "ADJ" or word.pos_ == "PART": 
                title += word.text+"_"
        return title[:-1]

    def checkWHQuestion(self, doc):
        # dataResp = get_prediction(doc)
        # scoreArr = []
        # for data in dataResp.payload:
        #     score = data.classification.score
        #     if score > 0.54:
        #         scoreArr.append(score)
        # if len(scoreArr) > 0:
        #     maxScore = max(scoreArr)
        #     for data in dataResp.payload:
        #         score = data.classification.score
        #         if score == maxScore:
        #             return data.display_name

        sen = self.sp(doc)
        
        if len(sen) <= 0 : return "NONE" 
        
        #Xét riêng cho what vì khi rule chỉ có 1 chữ độ chính xác rất thấp
        #Nếu câu chỉ có 1 chữ
        if len(sen) == 1:
            whatRule = ["NOUN", "PROPN"]
            if sen[0].pos_ in whatRule: return "WHAT_QUESTION"
            return "NONE"
        #Nếu câu chỉ có 2 chữ
        if len(sen) == 2: 
            whatRule = [["PROPN","PROPN"],["NOUN", "NOUN"],["PROPN","NOUN"]]
            wordPosArr = []
            for word in sen:
                wordPosArr.append(word.pos_)
            
            if wordPosArr in whatRule: return "WHAT_QUESTION"
            return "NONE"
        
        matches = self.matcher(sen)

        for match_id, start, end in matches:
            span = sen[start:end]
            if len(span.text) > 0:
                return self.sp.vocab.strings[match_id]
        
        return "NONE"


if __name__ == '__main__':
    sentance = "Colour shift This is the settings that I use"
    # sentance = 'Ayuda! El blanco sale amarillo en'
    # seperate = separateEntity(sentance)
    # objectSen = seperate.getObject()
    # print(objectSen)
    # actionSen = seperate.getAction()
    # print(actionSen)
    # # title = seperate.getTitle()
    # # print(title)
    # tag = seperate.getTag()
    # print(tag)
    # pos = seperate.getPos()
    # print(pos)
    # print(seperate.checkWHQuestion())


#     #print(f'{word.text:{12}} {word.pos_:{10}} {word.tag_:{8}} {spacy.explain(word.tag_)}')
