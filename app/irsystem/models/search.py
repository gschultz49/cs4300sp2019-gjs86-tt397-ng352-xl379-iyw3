# IR system goes here
import numpy as np
import re, json, os, nltk, csv
import pickle
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from ... import settings
#from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

#ps = PorterStemmer()

path = os.path.join(settings.APP_STATIC, "v1.tsv")
# path = "../../static/v1.tsv"
with open(path) as csvfile:
    reader = csv.DictReader(csvfile, dialect='excel-tab')
    sdict = {}
    for row in reader:
        sdict[row['shoeNumber']] = row
        
path1 = os.path.join(settings.APP_STATIC, "v2.tsv")
# path1 = "../../static/v2.tsv"
with open(path1) as tsvfile2:
    reader = csv.DictReader(tsvfile2, dialect='excel-tab')
    rdict = {}
    for row in reader:
        rdict[row['shoeName']] = row
        
# Build analyzer
analyzer = SentimentIntensityAnalyzer()

def is_positive(text):
    """
    Typical threshold values (used in the literature cited on this page) are:
    positive sentiment: compound score >= 0.05
    neutral sentiment: (compound score > -0.05) and (compound score < 0.05)
    negative sentiment: compound score <= -0.05
    """    
    # sample output {'compound': -0.1458, 'pos': 0.267, 'neg': 0.315, 'neu': 0.418}
    score = analyzer.polarity_scores(text)['compound']
    return score >= 0.05


def tokenize(text):
    """Returns a list of words that make up the text. Words are stemmed.
    
    Params: {text: String}
    Returns: List
    """
    text = text.lower()

    reg = '[a-z]+'
    list = re.findall(reg, text)
    list1 = []
    #for item in list:
    #    list1.append(ps.stem(item))
    return list


def tokenize1(text):
    """Returns a list of words that make up the text. Words are unstemmed.
    
    Params: {text: String}
    Returns: List
    """
    text = text.lower()

    reg = '[a-z0-9]+'
    list = re.findall(reg, text)
    return list

def tokenize2(text):
    """Returns a list of words that make up the text. Words are unstemmed.
    
    Params: {text: String}
    Returns: List
    """
    text = text.lower()

    reg = '[a-z]+'
    list = re.findall(reg, text)
    return list


def build_inverted_index(shoedict):
    newdict = {}
    for shoe in shoedict:
        for t in set(shoedict[shoe]['tokens']):
            if t not in newdict:
                newdict[t] = []
                newdict[t].append((shoe, shoedict[shoe]['tokens'].count(t)))
            else:
                newdict[t].append((shoe, shoedict[shoe]['tokens'].count(t)))
    return newdict


def build_vectorizer(max_features, stop_words, tokenizer=tokenize2, max_df=0.8, min_df=1, norm='l2'):
    """Returns a TfidfVectorizer object with the above preprocessing properties.
    
    Params: {max_features: Integer,
             max_df: Float,
             min_df: Float,
             norm: String,
             stop_words: String}
    Returns: TfidfVectorizer
    """
    return TfidfVectorizer(stop_words=stop_words, tokenizer=tokenizer, max_df=max_df, min_df=min_df,
                           max_features=max_features, norm=norm)


def build_vectorizer_unstemmed(max_features, stop_words, max_df=0.8, min_df=1, norm='l2'):
    """Returns a TfidfVectorizer object with the above preprocessing properties.
    
    Params: {max_features: Integer,
             max_df: Float,
             min_df: Float,
             norm: String,
             stop_words: String}
    Returns: TfidfVectorizer
    """
    return TfidfVectorizer(stop_words=stop_words, max_df=max_df, min_df=min_df,
                           max_features=max_features, norm=norm)


tfidf_vec1 = build_vectorizer_unstemmed(5000, "english")


def get_sim(shoe1, shoe2, input_doc_mat):
    """Returns a float giving the cosine similarity
    
    Params: {shoe1: Int,
             shoe2: Int,
             input_doc_mat: Numpy Array,
    Returns: Float (Cosine similarity of the two shoes.)
    """
    norm1 = np.linalg.norm(input_doc_mat[shoe1])
    norm2 = np.linalg.norm(input_doc_mat[shoe2])
    return np.dot(input_doc_mat[shoe1], input_doc_mat[shoe2])/(norm1*norm2)


def top_terms(shoe1, shoe2, input_doc_mat, index_to_vocab, top_k=10):
    """Returns a list of the top k similar terms (in order) 
    
    Params: {shoe1: Int,
             shoe2: Int,
             input_doc_mat: Numpy Array,
             index_to_vocab: Dict,
             top_k:Int}
    Returns: List 
    """
    shoe1idf = input_doc_mat[shoe1]
    shoe2idf = input_doc_mat[shoe2]
    prod = np.multiply(shoe1idf, shoe2idf)
    new = np.flip(np.argsort(prod)[-top_k:], axis=0)
    final = []
    score = []
    concat = []
    for i in new:
        if (prod[i] > 0):
            final.append(index_to_vocab[i])
            score.append(prod[i])
            concat.append((index_to_vocab[i], prod[i]))
    return final, score, concat


splitter = re.compile(r"""
    (?<![A-Z])  # LOOKBEHIND last character cannot be uppercase
    [.!?]       # match punctuation
    \s+
    (?=[A-Z])   # LOOKAHEAD next character must be followed by at least one whitespace and an uppercase      
    """, re.VERBOSE)

shoename_to_index = {}
index_to_shoename = {}
#allw = []

for item in sdict:
    name = sdict[item]['shoeName']
    list1 = sdict[item]['good_buy_bullets'].split('</s>')
    sdict[item]['good'] = []
    sdict[item]['tokens'] = []
    sdict[item]['usefult'] = ""
    sdict[item]['useful'] = ""
    sdict[item]['lowername'] = name.lower()
    sdict[item]['name'] = tokenize1(name)
    shoename_to_index[name.lower()] = int(sdict[item]['shoeNumber'])
    index_to_shoename[sdict[item]['shoeNumber']] = name.lower()
    
    reviews = ""
    features = []
    if name in rdict:   
        sdict[item]['amazonLink'] = rdict[name]['link']
        reviews = rdict[name]['amazonReviews']
    
    blist = []
    for s in splitter.split(sdict[item]['bottom_line']):
        if is_positive(s):
            blist.append(s)

    unwantedlist = [' consumers ', ' purchasers ', ' said ', ' user ', ' consumer ', ' purchaser ', ' buyers ',
                    ' buyer ', ' his ', ' was ', ' review ', ' comment ', ' reviews ',
                    ' reviewers ', ' reviewer ', ' wearer ', ' wearers ', ' commented ',
                    ' thought ', ' mentioned ', ' felt ', ' this ', ' users ', ' has ', ' feel ', ' admired ',
                    ' testers ', ' tester ', ' comments ', 's', "good", 'pair', 'definitely','t','like','very','ha','just',
                   'stated', 'shoes', 'pair', 'shoe', 'pairs', 'model', 'saucony','previous','pros','cons','ye','didn','wasn','ve','t','k',
                   'feels','consider','considers','mistake','earlier','installment','old','d','don','compared','compare','went','e','gt','v',
                   'version','asics','clifton','buy','bought','d','a','b','c','f','g','h','i','j','l','m','n','o','p','q','r','u','w','x','y',
                   'z','read','gets','maybe','really','amazon','footwear','product','em','purchase','used','purchased', 'great']

    for sent in list1:
        if len(sent) > 0:
            sdict[item]['good'].append(sent[3:])
    for sent in blist:
        if len(sent) > 0:
            sent = sent + "."
            sdict[item]['good'].append(sent)
    
    t = tokenize1(reviews)
    for token in t:
        sdict[item]['tokens'].append(token)
    
    for sent in sdict[item]['good']:
        t = tokenize1(sent)
        for token in t:
            sdict[item]['tokens'].append(token)
           # allw.append(token)
            

    newunwant = [term.strip() for term in unwantedlist]

    for t in sdict[item]['tokens']:
        sdict[item]['useful'] = sdict[item]['useful'] + ' ' + t
        if t not in newunwant:
            if t not in tokenize1(name):
                sdict[item]['usefult'] = sdict[item]['usefult'] + ' ' + t

#NOT CALLING precompute() now, loading and unpickling instead
#similar, shoename_to_index, titles = Precompute()

big_dict_path = os.path.join(settings.APP_MODELS, "big_dictionary.p")
print (big_dict_path)
with open(big_dict_path, "rb") as pickle_file:
    unpickled_dictionary = pickle.load(pickle_file)
# unpickled_dictionary = pickle.load( open( "big_dictionary.p", "rb" ) )
similar = unpickled_dictionary['similar']
shoename_to_index = unpickled_dictionary['shoename_to_index']
titles = unpickled_dictionary['titles']


def FindSimilarShoes(shoename, information_dict=similar, shoename_to_index=shoename_to_index):
    """ given a valid shoe name, outputs a list of 6 similar shoes"""
    shoename = shoename.lower()
    if shoename not in shoename_to_index:
        return []
    
    index = shoename_to_index[shoename]
    datadict = information_dict[index]
    newdict = {}
    for i in datadict:
        newdict[i] = {}
        newdict[i]['shoeName'] = datadict[i]['shoeName']
        newind = shoename_to_index[datadict[i]['shoeName'].lower()]
        newdict[i]['shoeImage'] = datadict[i]['shoeImage']
        newdict[i]['amazonLink'] = datadict[i]['amazonLink']
        newdict[i]['similarity'] = datadict[i]['our similarity score']
        newdict[i]['relevantTerms'] = datadict[i]['relevant terms']
        newdict[i]['term_and_score'] = datadict[i]['term_and_score']
        newdict[i]['corescore'] = datadict[i]['corescore']
        newdict[i]['terrain'] = datadict[i]['terrain']
        newdict[i]['arch_support'] = datadict[i]['arch_support']
        newdict[i]['men_weight'] = datadict[i]['men_weight']
        newdict[i]['women_weight'] = datadict[i]['women_weight']
        sim_shoes = []
        numbers = 0
        for j in information_dict[newind]:
            if numbers < 5:
                sim_shoes.append(information_dict[newind][j]['shoeName'])
            numbers += 1
        newdict[i]['similarShoes'] = sim_shoes
    array = []
    for item in newdict:
        array.append(newdict[item])
    return array


def CompleteName(q, titles=titles):
    """  given a query that is meant to be a shoe name, give the top 15 suggested valid shoe names   """

    q = q.lower()
    possible = []
    for t in titles:
        if q in t.lower():
            possible.append(t)
    return possible[:15]


    u_input = {}
    u_input['arch_support'] = "N/A"
    u_input['terrain'] = "N/A"
    
def FindQuery(q, u_input, sdict=sdict, numtop=18, get_sim=get_sim, information_dict=similar, shoename_to_index=shoename_to_index, tfidf_vec1=tfidf_vec1, top_terms=top_terms):
    """ Given a query, outputs the top 6 related shoes    """

    user_dict = u_input
    
    newdictlist = []
    for i in np.arange(len(sdict)):
        newdictlist.append(sdict[str(i)]['useful'])
    newdictlist.append(q)

    doc_by_vocab1 = tfidf_vec1.fit_transform(newdictlist).toarray()
    index_to_vocab1 = {i: v for i, v in enumerate(
        tfidf_vec1.get_feature_names())}
    vocab_to_index1 = {v: i for i, v in index_to_vocab1.items()}

    cossim1 = np.zeros(len(sdict))
    for i in np.arange(len(sdict)):
            cossim1[i] = get_sim(i, len(sdict), doc_by_vocab1)
    
    if np.argmax(cossim1) == 0:
        return []
    
    topresult = np.flip(np.argsort(cossim1))
    
    #topresults = topresult[:numtop]
    
    
    topresults = []
    
    i = 0
    while len(topresults) < numtop and i < 100:
        if len(user_dict["arch_support"]) != 3 and user_dict["arch_support"] != "N/A" and user_dict['arch_support'] != sdict[str(topresult[i])]['arch_support']:
            if len(user_dict["arch_support"]) != 2:
                i += 1
                continue
            if (len(user_dict["arch_support"]) == 2 and user_dict["arch_support"][0] != sdict[str(topresult[i])]['arch_support'] 
            and user_dict["arch_support"][1] != sdict[str(topresult[i])]['arch_support']):
                i += 1
                continue
        if len(user_dict["terrain"]) != 2 and user_dict["terrain"] != "N/A" and user_dict["terrain"] != sdict[str(topresult[i])]['terrain']:
            i += 1
            continue
        topresults.append(topresult[i])
        i +=1
      
    
    sentdict = {}
    for i in topresults:
        sentdict[i] = {}
        num = 0
        for sent in sdict[str(i)]['good']:
            sentdict[i][num] = sent
            num += 1
        sentdict[i][num] = q

        doc_by_vocab_sent = tfidf_vec1.fit_transform(
            [sentdict[i][d] for d in sentdict[i]]).toarray()
        index_to_vocab_sent = {i: v for i, v in enumerate(
            tfidf_vec1.get_feature_names())}
        vocab_to_index_sent = {v: i for i, v in index_to_vocab_sent.items()}
        cossim_sent = np.zeros(len(sdict[str(i)]['good']))
        for j in np.arange(len(sdict[str(i)]['good'])):
            cossim_sent[j] = get_sim(j, len(sentdict[i])-1, doc_by_vocab_sent)
        index = np.argsort(-cossim_sent)[:2]
        sentdict[i]['sent'] = []
        for ind in index:
            if (cossim_sent[ind] > 0):
                sentdict[i]['sent'].append(sdict[str(i)]['good'][ind])

    tops = {}
    for i in np.arange(len(topresults)):
        tops[i] = {}
        tops[i]['shoeName'] = sdict[str(topresults[i])]['shoeName']
        tops[i]['shoeImage'] = sdict[str(topresults[i])]['shoe_image']
        tops[i]['amazonLink'] = sdict[str(topresults[i])]['amazonLink']
        tops[i]['similarity'] = round(cossim1[topresults[i]], 4)
        tops[i]['corescore'] = sdict[str(topresults[i])]['corescore']
        tops[i]['relevantTerms'] = top_terms(len(
            sdict), topresults[i], doc_by_vocab1, index_to_vocab1, top_k=len(tokenize1(q)))[0]
        tops[i]['scores'] = top_terms(len(
            sdict), topresults[i], doc_by_vocab1, index_to_vocab1, top_k=len(tokenize1(q)))[1]
        tops[i]['termsAndScores'] = top_terms(len(
            sdict), topresults[i], doc_by_vocab1, index_to_vocab1, top_k=len(tokenize1(q)))[2]
        tops[i]['relevantSentence'] = sentdict[topresults[i]]['sent']
        tops[i]['terrain'] = sdict[str(topresults[i])]['terrain']
        tops[i]['men_weight'] = sdict[str(topresults[i])]['men_weight']
        tops[i]['women_weight'] = sdict[str(topresults[i])]['women_weight']
        tops[i]['arch_support'] = sdict[str(topresults[i])]['arch_support']

    for item in tops:
        sim_shoes = []
        newindex = shoename_to_index[tops[item]['shoeName'].lower()]
        numbers = 0
        for j in information_dict[newindex]:
            if numbers < 5:
                sim_shoes.append(information_dict[newindex][j]['shoeName'])
            numbers += 1
        tops[item]['similarShoes'] = sim_shoes

    array = []
    
    maxnum = len(tokenize1(q))
    
    for num in np.flip(np.arange(maxnum)+1):
        for item in tops:
            if len(tops[item]['relevantTerms'])==num:
                array.append(tops[item])
    return array


def CompleteQuery(query, tokenize=tokenize1):
    """ given an incomplete query, outputs the next word suggestion    """

    #look only at the last word, given that the word is not a stop word
    index = len(tokenize(query))-1
    q = tokenize(query)[index]
    while q in stopwords.words('english') and index > 0:
        index -= 1
        q = tokenize(query)[index]

    tokens = {}

    #use results from top 100 hits
    sim = FindQuery(q, numtop=100)

    for dictionary in sim:
        if q in dictionary['relevantTerms']:
            for sent in dictionary['relevantSentence']:
                sentence = tokenize1(sent)
                if q in sentence:
                    index = sentence.index(q)
                    if index + 1 < len(sentence):
                        newtoken = sentence[index + 1]
                        if newtoken not in stopwords.words('english'):
                            if newtoken not in tokens:
                                tokens[newtoken] = 1
                            else:
                                tokens[newtoken] += 1
    words = sorted(tokens.items(), key=lambda x: x[1], reverse=True)

    topwords = []
    for item in words[:12]:
        topwords.append(item[0])

    return topwords
