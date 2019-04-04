import glob
import json
import pandas as pd
import os
import random
import pprint
class_dict = {
    'rock':'Rock',
    'grunge':'Rock',
    'hip' :'HipHop',
    'hop' : 'HipHop',
    'crunk' : 'HipHop',
    'metal': 'Metal',
    'deathcore': 'Metal',
    'industrial': 'Metal',
    'pop' : 'Pop',
    'punk' : 'Punk',
    'emo' : 'Punk',
    'post-hardcore' : 'Punk',
    'wave' : 'Punk',
    'age' : 'Punk',
    'rap' : 'Rap',
    'soul' : 'Blues',
    'blues' : 'Blues',
    'r&b' : 'Blues',
    'folk' :'Folk',
    'country' : 'Folk',
    'electronic' : 'Electronica' ,
    'house' : 'Electronica' ,
    'electronica' : 'Electronica' ,
    'trance' : 'Electronica' ,
    'ebm' : 'Electronica' ,
    'horrorcore' : 'Rap',
              }
if __name__=='__main__':
    output = os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)),
            'train_val'
        )
    if not os.path.exists(output):
        os.mkdir(output)
    data_list = glob.glob(
        os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)),
            'processed_data',
            '*.json'
        ))
    datas = []
    for x in data_list:
        try:
            datas .append(json.load(open(x)))
        except:
            continue

    datas = [x for y in datas for x in y]
    tmp = []
    genres= []
    print(len(datas))
    for d in datas:
        genre = d['album']['genre']
        if not genre:
            continue
        a = 0
        for word in class_dict.keys():
            if word in genre.lower():
                genres.append(class_dict[word])
                d['album']['genre'] = class_dict[word]
                a =1
                break
        if not a :
            genres.append(genre)
        tmp.append([d['lyrics'],d['album']['genre']])
    genres = tuple(set(genres))
    pd.DataFrame(genres,index=list(range(len(genres))),columns=['class']).to_csv(os.path.join(output,'original_label.csv'))

    datas = [[x[0],genres.index(x[1])] for x in tmp]
    a = [0] * len(genres)
    for d in datas:
        a[d[1]] +=1
    genres = dict(zip(genres,a))
    pprint.pprint( genres)
    print(sum(a))

    genres = dict(filter(lambda x : x[1] > 20 , genres.items()))
    genres = tuple(genres.keys())
    datas = [[x[0],genres.index(x[1])] for x in tmp if x[1] in genres]
    a = [0] * len(genres)
    for d in datas:
        a[d[1]] +=1
    print(dict(zip(genres,a)))
    print(sum(a))
    random.shuffle(datas)
    genres = pd.DataFrame(genres,index=list(range(len(genres))),columns=['class'])
    genres.to_csv(os.path.join(output,'label.csv'))
    split = 500
    pd.DataFrame(datas[:split],index=list(range(len(datas[:split]))),columns=['lyrics','class']).to_csv(os.path.join(output,'test.csv'))
    pd.DataFrame(datas[split:],index=list(range(len(datas[split:]))),columns=['lyrics','class']).to_csv(os.path.join(output,'train.csv'))

    pass