# IR system goes here
import numpy as np
import re, json, os, nltk, csv
# from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

# nltk.download('stopwords')
ps = PorterStemmer()

# APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
# APP_STATIC = os.path.join(APP_ROOT, 'static')


# FIGURE OUT HOW TO GET THIS TO USE THE REAL APPLICATION ROOT
# with ("4_10_2019.tsv") as csvfile:

with open("/Users/gschultz49/Desktop/CS4300/CS4300_Flask_template/app/4_10_2019.tsv") as csvfile:
    reader = csv.DictReader(csvfile, dialect='excel-tab')
    sdict = {}
    for row in reader:
        sdict[row['shoeNumber']] = row
        

def tokenize(text):
    """Returns a list of words that make up the text. Words are stemmed.
    
    Params: {text: String}
    Returns: List
    """
    text = text.lower()

    reg = '[a-z]+'
    list = re.findall(reg,text)
    list1 = []
    for item in list:
        list1.append(ps.stem(item))
    return list1

def tokenize1(text):
    """Returns a list of words that make up the text. Words are unstemmed.
    
    Params: {text: String}
    Returns: List
    """
    text = text.lower()

    reg = '[a-z0-9]+'
    list = re.findall(reg,text)
    return list

def build_inverted_index(shoedict):
    newdict = {}
    for shoe in shoedict:
        for t in set(shoedict[shoe]['tokens']):
            if t not in newdict:
                newdict[t] = []
                newdict[t].append((shoe,shoedict[shoe]['tokens'].count(t)))
            else:
                newdict[t].append((shoe,shoedict[shoe]['tokens'].count(t)))
    return newdict

def build_vectorizer(max_features, stop_words, tokenizer = tokenize, max_df=0.8, min_df=1, norm='l2'):
    """Returns a TfidfVectorizer object with the above preprocessing properties.
    
    Params: {max_features: Integer,
             max_df: Float,
             min_df: Float,
             norm: String,
             stop_words: String}
    Returns: TfidfVectorizer
    """
    return TfidfVectorizer(stop_words = stop_words, tokenizer = tokenize, max_df = max_df, min_df = min_df, 
                           max_features = max_features, norm=norm)


def build_vectorizer_unstemmed(max_features, stop_words, tokenizer = tokenize, max_df=0.8, min_df=1, norm='l2'):
    """Returns a TfidfVectorizer object with the above preprocessing properties.
    
    Params: {max_features: Integer,
             max_df: Float,
             min_df: Float,
             norm: String,
             stop_words: String}
    Returns: TfidfVectorizer
    """
    return TfidfVectorizer(stop_words = stop_words, max_df = max_df, min_df = min_df, 
                           max_features = max_features, norm=norm)
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
    return np.dot(input_doc_mat[shoe1],input_doc_mat[shoe2])/(norm1*norm2)


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
    prod = np.multiply(shoe1idf,shoe2idf)
    new = np.flip(np.argsort(prod)[-top_k:],axis = 0)
    final = []
    score = []
    concat = []
    for i in new:
        if (prod[i] > 0):
            final.append(index_to_vocab[i])
            score.append(prod[i])
            concat.append((index_to_vocab[i],prod[i]))
    return final,score,concat

def Precompute(sdict = sdict, tokenize = tokenize, build_inverted_index = build_inverted_index, build_vectorizer = build_vectorizer,
              get_sim = get_sim, top_terms = top_terms, numdisp = 6):

    """Precomputes the cosine similarity matrix for all shoes, and outputs the similar dictionary for every shoe """
    
    shoename_to_index = {}
    index_to_shoename = {}
    allw = []
    for item in sdict:
        name = sdict[item]['shoeName']
        list1 = sdict[item]['good_buy_bullets'].split('</s>')
        blist = sdict[item]['bottom_line'].split('.')
        sdict[item]['good']=[]
        sdict[item]['tokens'] = []
        sdict[item]['usefult'] = ""
        sdict[item]['useful'] = ""
        sdict[item]['lowername'] = name.lower()
        sdict[item]['name'] =tokenize1(name)
        shoename_to_index[name.lower()] = int(sdict[item]['shoeNumber'])
        index_to_shoename[sdict[item]['shoeNumber']] = name.lower()


        unwantedlist = [' consumers ',' purchasers ',' said ',' user ',' consumer ',' purchaser ',' buyers ',
                        ' buyer ',' his ',' was ',' review ',' comment ',' reviews ', 
                        ' reviewers ', ' reviewer ', ' wearer ', ' wearers ', ' commented ',
                       ' thought ', ' mentioned ', ' felt ', ' this ' , ' users ', ' has ', ' feel ', ' admired ',
                       ' testers ', ' tester ', ' comments ','s']

        for sent in list1:
            if len(sent) > 0:
                sdict[item]['good'].append(sent[3:])
        for sent in blist:
            if len(sent) > 0:
                sent = sent + "."
                sdict[item]['good'].append(sent)

        for sent in sdict[item]['good']:
            t = tokenize1(sent)
            for token in t:
                sdict[item]['tokens'].append(token)
                allw.append(token)

        newunwant = [term.strip() for term in unwantedlist]

        for t in sdict[item]['tokens']:
            sdict[item]['useful'] = sdict[item]['useful'] + ' ' + t
            if t not in newunwant:
                if t not in tokenize1(name): 
                    sdict[item]['usefult'] = sdict[item]['usefult'] + ' ' + t
                    
    titles = []
    for item in sdict:
        titles.append(sdict[item]['shoeName'])      
        
    inv_idx = build_inverted_index(sdict)
        
    all_words = list(set(allw))
    n_feats = len(all_words)
    doc_by_vocab = np.empty([len(sdict), n_feats])
        
    tfidf_vec = build_vectorizer(n_feats, "english")
    doc_by_vocab = tfidf_vec.fit_transform([sdict[d]['usefult'] for d in sdict]).toarray()
    index_to_vocab = {i:v for i, v in enumerate(tfidf_vec.get_feature_names())}
    vocab_to_index = {v:i for i, v in index_to_vocab.items()}

    cossim = np.zeros((len(sdict),len(sdict)))
    for i in np.arange(len(sdict)):
        for j in np.arange(i+1,len(sdict)):
            cossim[i,j] = get_sim(i,j,doc_by_vocab)
            cossim[j,i] = cossim[i,j]

    similar = {}
    for i in np.arange(len(sdict)):
        topshoes = np.argsort(-cossim[i])[:numdisp]
        similar[i]= {}
        for j in np.arange(numdisp):
            similar[i][j]= {}
            similar[i][j]['index'] = topshoes[j]
            similar[i][j]['shoeName']=sdict[str(topshoes[j])]['shoeName']
            similar[i][j]['shoeImage']=sdict[str(topshoes[j])]['shoe_image']
            similar[i][j]['amazonLink']=sdict[str(topshoes[j])]['amazonLink']

            similar[i][j]['our similarity score'] = round(cossim[i][topshoes[j]],4)
            similar[i][j]['shoes'] = sdict[str(i)]['shoeName'],sdict[str(topshoes[j])]['shoeName']
            similar[i][j]['relevant terms'] = top_terms(i, topshoes[j], doc_by_vocab, index_to_vocab, top_k=12)[0]
            similar[i][j]['scores'] = top_terms(i, topshoes[j], doc_by_vocab, index_to_vocab, top_k=12)[1]
            similar[i][j]['corescore'] = sdict[str(i)]['corescore']
            similar[i][j]['term and score'] = top_terms(i, topshoes[j], doc_by_vocab, index_to_vocab, top_k=12)[2]
            
    return similar, shoename_to_index, titles

similar, shoename_to_index, titles = Precompute()

def FindSimilarShoes(shoename,information_dict = similar,shoename_to_index =shoename_to_index):
    
    """ given a valid shoe name, outputs a list of 6 similar shoes"""
    shoename = shoename.lower()
    index = shoename_to_index[shoename]
    datadict = information_dict[index]
    newdict= {}
    for i in datadict:
        newdict[i] = {}
        newdict[i]['shoeName'] = datadict[i]['shoeName']
        newind = shoename_to_index[datadict[i]['shoeName'].lower()]
        newdict[i]['shoeImage'] = datadict[i]['shoeImage']
        newdict[i]['amazonLink'] = datadict[i]['amazonLink']
        newdict[i]['similarity'] = datadict[i]['our similarity score']
        newdict[i]['relevantTerms'] = datadict[i]['relevant terms']
        newdict[i]['corescore'] = datadict[i]['corescore'] 
        sim_shoes = []
        for j in information_dict[newind]:
            sim_shoes.append(information_dict[newind][j]['shoeName'])
        newdict[i]['similarShoes'] = sim_shoes 
    array = []
    for item in newdict:
        array.append(newdict[item])
    return array

def CompleteName(q,titles = titles):
    
    """  given a query that is meant to be a shoe name, give the top 15 suggested valid shoe names   """
    
    q = q.lower()
    possible = []
    for t in titles:
        if q in t.lower():
            possible.append(t)
    return possible[:15]


def FindQuery(q,sdict = sdict, numtop = 6, information_dict = similar,shoename_to_index = shoename_to_index,tfidf_vec1 = tfidf_vec1):
    
    """ Given a query, outputs the top 6 related shoes    """ 

    qdict = sdict.copy()
    qdict['q'] = {}
    qdict['q']['useful'] = q

    doc_by_vocab1 = tfidf_vec1.fit_transform([qdict[d]['useful'] for d in qdict]).toarray()
    index_to_vocab1 = {i:v for i, v in enumerate(tfidf_vec1.get_feature_names())}
    vocab_to_index1 = {v:i for i, v in index_to_vocab1.items()}

    cossim1 = np.zeros(len(sdict))
    for i in np.arange(len(sdict)):
            cossim1[i] = get_sim(i,len(sdict),doc_by_vocab1)
    topresults = np.flip(np.argsort(cossim1))[:numtop]
    
    sentdict = {}
    for i in topresults:
        sentdict[i]= {}
        num = 0
        for sent in sdict[str(i)]['good']:
            sentdict[i][num] = sent
            num += 1
        sentdict[i][num] = q
        doc_by_vocab_sent = tfidf_vec1.fit_transform([sentdict[i][d] for d in sentdict[i]]).toarray()
        index_to_vocab_sent = {i:v for i, v in enumerate(tfidf_vec1.get_feature_names())}
        vocab_to_index_sent = {v:i for i, v in index_to_vocab_sent.items()}
        cossim_sent = np.zeros(len(sdict[str(i)]['good']))
        for j in np.arange(len(sdict[str(i)]['good'])):
            cossim_sent[j]=get_sim(j,len(sentdict[i])-1,doc_by_vocab_sent)
        index = np.argsort(-cossim_sent)[:2]
        sentdict[i]['sent'] = []
        for ind in index:
            if (cossim_sent[ind] > 0):
                sentdict[i]['sent'].append(sdict[str(i)]['good'][ind])
    
    tops = {}
    for i in np.arange(len(topresults)):
        tops[i]= {}
        tops[i]['shoeName'] = sdict[str(topresults[i])]['shoeName']
        tops[i]['shoeImage'] = sdict[str(topresults[i])]['shoe_image']
        tops[i]['amazonLink'] = sdict[str(topresults[i])]['amazonLink']
        tops[i]['similarity'] = round(cossim1[topresults[i]],4)
        tops[i]['corescore'] = sdict[str(topresults[i])]['corescore']
        tops[i]['relevantTerms'] = top_terms(len(sdict),topresults[i], doc_by_vocab1, index_to_vocab1, top_k=len(tokenize1(q)))[0]
        tops[i]['scores'] = top_terms(len(sdict),topresults[i], doc_by_vocab1, index_to_vocab1, top_k=len(tokenize1(q)))[1]
        tops[i]['termsAndScores'] = top_terms(len(sdict),topresults[i], doc_by_vocab1, index_to_vocab1, top_k=len(tokenize1(q)))[2]
        tops[i]['relevantSentence']=sentdict[topresults[i]]['sent']
    
    for item in tops:
        sim_shoes = []
        newindex = shoename_to_index[tops[item]['shoeName'].lower()]
        for j in information_dict[newindex]:
            sim_shoes.append(information_dict[newindex][j]['shoeName'])
        tops[item]['similarShoes'] = sim_shoes 
        
    array = []
    for item in tops:
        array.append(tops[item])
    return array

def CompleteQuery(query,tokenize = tokenize1):
    
    """ given an incomplete query, outputs the next word suggestion    """ 

    #look only at the last word, given that the word is not a stop word
    index = len(tokenize(query))-1
    q = tokenize(query)[index]
    while q in stopwords.words('english') and index > 0:
        index -= 1
        q = tokenize(query)[index]
    
    tokens = {}
    
    #use results from top 200 hits
    sim = FindQuery(q, numtop = 200)
    
    for dictionary in sim:
        if q in dictionary['relevant terms']:
            for sent in dictionary['relevant sentence']:
                sentence = tokenize1(sent)
                index = sentence.index(q)
                if index + 1 < len(sentence):
                    newtoken  = sentence[index + 1]
                    if newtoken not in stopwords.words('english'):
                        if newtoken not in tokens:
                            tokens[newtoken] = 1
                        else:
                            tokens[newtoken] += 1
    words = sorted(tokens.items(), key=lambda x: x[1], reverse = True)
    
    topwords = []
    for item in words[:12]:
        topwords.append(item[0])
        
    return topwords
