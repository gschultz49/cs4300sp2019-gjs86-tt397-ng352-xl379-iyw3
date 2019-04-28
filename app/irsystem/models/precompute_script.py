# IR system goes here
import numpy as np
import re, json, os, nltk, csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#from ... import settings
#from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

#ps = PorterStemmer()

path = "../../static/4_15_2019.tsv"
with open(path) as csvfile:
    reader = csv.DictReader(csvfile, dialect='excel-tab')
    sdict = {}
    for row in reader:
        sdict[row['shoeNumber']] = row
        
path1 = "../../static/v2.tsv"
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
    score = analyzer.polarity_scores(text)['neg']
    return score == 0


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


def Precompute(sdict=sdict, rdict = rdict, is_positive = is_positive, tokenize = tokenize, tokenize1=tokenize1, build_inverted_index=build_inverted_index, build_vectorizer=build_vectorizer,
               get_sim=get_sim, top_terms=top_terms, numdisp=18):
    """Precomputes the cosine similarity matrix for all shoes, and outputs the similar dictionary for every shoe """

    
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

    titles = []
    for item in sdict:
        titles.append(sdict[item]['shoeName'])

    #inv_idx = build_inverted_index(sdict)

    dictlist = []
    for i in np.arange(len(sdict)):
        dictlist.append(sdict[str(i)]['usefult'])

    #all_words = list(set(allw))
    n_feats = 4000
    doc_by_vocab = np.empty([len(sdict), n_feats])

    tfidf_vec = build_vectorizer(n_feats, "english")
    doc_by_vocab = tfidf_vec.fit_transform(dictlist).toarray()
    index_to_vocab = {i: v for i, v in enumerate(
        tfidf_vec.get_feature_names())}
    vocab_to_index = {v: i for i, v in index_to_vocab.items()}

    cossim = np.zeros((len(sdict), len(sdict)))
    for i in np.arange(len(sdict)):
        for j in np.arange(i+1, len(sdict)):
            cossim[i, j] = get_sim(i, j, doc_by_vocab)
            cossim[j, i] = cossim[i, j]

    similar = {}
    for i in np.arange(len(sdict)):
        topshoes = np.argsort(-cossim[i])[:numdisp]
        similar[i] = {}
        for j in np.arange(numdisp):
            similar[i][j] = {}
            similar[i][j]['index'] = topshoes[j]
            similar[i][j]['shoeName'] = sdict[str(topshoes[j])]['shoeName']
            similar[i][j]['shoeImage'] = sdict[str(topshoes[j])]['shoe_image']
            similar[i][j]['amazonLink'] = sdict[str(topshoes[j])]['amazonLink']
            similar[i][j]['terrain'] = sdict[str(topshoes[j])]['terrain']
            similar[i][j]['arch_support'] = sdict[str(topshoes[j])]['arch_support']
            similar[i][j]['men_weight'] = sdict[str(topshoes[j])]['men_weight']
            similar[i][j]['women_weight'] = sdict[str(topshoes[j])]['women_weight']
            similar[i][j]['our similarity score'] = round(
                cossim[i][topshoes[j]], 4)
            similar[i][j]['shoes'] = sdict[str(
                i)]['shoeName'], sdict[str(topshoes[j])]['shoeName']
            similar[i][j]['relevant terms'] = top_terms(
                i, topshoes[j], doc_by_vocab, index_to_vocab, top_k=12)[0]
            similar[i][j]['scores'] = top_terms(
                i, topshoes[j], doc_by_vocab, index_to_vocab, top_k=12)[1]
            similar[i][j]['corescore'] = sdict[str(i)]['corescore']
            similar[i][j]['term_and_score'] = top_terms(
                i, topshoes[j], doc_by_vocab, index_to_vocab, top_k=12)[2]

    return similar, shoename_to_index, titles


similar, shoename_to_index, titles = Precompute()

pickle_dictionary =  {"similar" : similar, "shoename_to_index" : shoename_to_index, "titles" : titles}
pickle.dump( pickle_dictionary, open( "big_dictionary.p", "wb" ) )



