
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
    {'Folk': 435, 'Rock': 2935, 'Punk': 479, 'Electronica': 188, 'Metal': 917, 'Blues': 145, 'Pop': 407, 'Rap': 1257}

    
label:
    
    original label : train_val/original_label.csv
    finial label : train_val/label.csv

performance:

    bi-lstm 0.6840 (5 epoch)
    double bi-lstm 0.6740  (4 epoch)
    bi-lstm-deep conv 0.6740 (5 epoch)
    lstm 0.6720 (5 epoch)
    
    number behind # is the result, the effect is bi-lstm > lstm > double bi-lstm > bi-lstm-deep conv
    Resean is the effect of overfitting is quite significant on this dataset. 
    The finial number of the data is not enough to surpport the mission here.

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
    
