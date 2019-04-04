
lyric classification
=====

data source : lyrics  wiki (sitemap)

data :
    
    final data file : 
        train_val/train.csv  6244
        train_val/test.csv 500
    TOTAL crawler : 67934
    vald data: 6923
    data has category : 6744
    {'Electronica': 188, 'Metal': 917, 'Folk': 435, 'Punk': 479, 'Pop': 407, 'HipHop': 1166, 'Ska': 32, 'Blues': 94, 'Rap': 91, 'Rock': 2935}


    
label:
    
    original label : train_val/original_label.csv
    finial label : train_val/label.csv

performance,train time iteration 319142:

    bi-lstm 0.6600
    double bi-lstm 0.648  (overfitting)
    bi-lstm-deep conv 0.6640000004768372 
    lstm 0.6560000004768372

report:
    
    crawler :       scrapy (python package)
    evaluation:     9 class, (train_val/label.csv)
    dataset:        dir data/train.csv, data/test.csv
    technology:     deep learning
                    CNN http://cs231n.github.io/convolutional-networks/
                    lstm:   http://colah.github.io/posts/2015-08-Understanding-LSTMs/,
                            自己写的，扔了就跑 ： https://zhuanlan.zhihu.com/p/35756075
                    bi-lstm: 
                    word embedding: https://towardsdatascience.com/introduction-to-word-embedding-and-word2vec-652d0c2060fa
                    GloVe: embedding/glove.pdf
                    keras: https://keras.io/zh/preprocessing/text/
    network:        tokenize -> word embedding -> (bi-lstm or lstm) -> CNN (3*3) (or deeper, see lstm_keras.py) -> pooling -> dense net -> 6 binary sigmoid for classify

usage :
    
    lyric_sitemap_crawler/spiders/sitemapcrawl.py
    lyric_sitemap_crawler/lyrics_songs_extract.py
    nlp_mining/json2csv.py
    lstm_keras.py
    
