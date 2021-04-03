# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 23:03:35 2021

@author: Hugo Xue
"""


'''评论情感分析'''
from analysis_corpus import AnalysisCorpus
from ifidf import TFIDF
from extract_sentences import ExtractThemeSentences
from calc_sentiment import ClacSentiment
import pandas as pd
import openpyxl

products = pd.read_excel("products.xlsx")
df_prod = products.dropna(how="any")   

def gen_themeset(tfidf_dict, title_list):
    #获取完整主题集
    if not tfidf_dict:
        return {}
    theme_set = {}
    theme_set.update(tfidf_dict)
    tfidf_list= theme_set.values()
    max_tfidf = max(tfidf_list)
    min_tfidf = min(tfidf_list)
    #title的权重较高，做特殊处理
    max_threshold = min_tfidf + 0.85 * (max_tfidf - min_tfidf)
    min_threshold = min_tfidf + 0.55 * (max_tfidf - min_tfidf)
    for title_word in title_list:
        if theme_set.has_key(title_word) and theme_set[title_word] < max_threshold:
            theme_set[title_word] = max_threshold
        elif not theme_set.has_key(title_word):
            theme_set[title_word] = min_threshold
    return theme_set

def gen_sen_tfidf(theme_set, sentence_words_list):
    sen_tfidf_list = []
    for sentence_list in sentence_words_list:
        sen_tfidf_list.append([theme_set[word] for word in sentence_list])
    return sen_tfidf_list

def sen_title_count(title_list, sentence_words_list):
    sen_title_list = []
    for sentence_list in sentence_words_list:
        word_count = 0
        for word in title_list:
            word_count += list(sentence_list).count(word)
        sen_title_list.append(word_count)
    return sen_title_list

def vector_proc(theme_set, sentence_words_list):
    words_list = theme_set.keys()
    theme_list = [theme_set[word] for word in words_list]
    sen_list = []
    for sentence_list in sentence_words_list:
        temp_list = []
        for word in words_list:
            count = sentence_list.count(word)
            simi = theme_set.get(word, 0)
            temp_list.append(1.00 * count * simi)
        sen_list.append(temp_list)
    return theme_list, sen_list

def get_sentiment(sen_score_list, sentiment_list):
    sort_score_list = sorted(sen_score_list, reverse=True)

    if len(sen_score_list) in range(3,11):
        length = 3
    elif len(sen_score_list) > 10:
        length = int(30 * len(sen_score_list) / 100)
    else:
        length = len(sen_score_list)
    
    theme_score_list = sort_score_list[:length+1]
    sentiment = 0.00
    for sen_score in theme_score_list:
        sen_index = sen_score_list.index(sen_score)
        value = sentiment_list[sen_index]
        sentiment += value
    return sentiment / len(theme_score_list)

def clac_sentiment(title, content):
    ac = AnalysisCorpus()
    # 获取产品名称的分词列表。
    title_list = ac.cut_sentence(title)
    # 获取评论内容的分句列表。
    content_list = ac.cut_content(content)
    if len(content_list) == 0:
        return 0
    # 获取评论内容的分词列表。格式：[[],[],[],]
    sentence_words_list, seg_list, tags_list = ac.cut_content_sentence(content_list)

    # 获取句法依存提取
    depend_list = ac.get_depend(seg_list, tags_list)

    tfidf_obj = TFIDF()
    tfidf_dict = tfidf_obj.get_tfidf(sentence_words_list)

    # 获取完整主题集
    theme_set = gen_themeset(tfidf_dict, title_list)
    theme_list, sen_list = vector_proc(theme_set, sentence_words_list)
    sen_tfidf_list = gen_sen_tfidf(theme_set, sentence_words_list)
    sen_title_list = sen_title_count(title_list, sentence_words_list)
    # 提取主题句
    them_obj = ExtractThemeSentences()
    sen_score_list = them_obj.get_score(theme_list, sen_list, sen_tfidf_list, sen_title_list)

    score_cut_list = []
    for i in range(len(sen_score_list)):
        score_cut_list.append([sen_score_list[i], "|".join(sentence_words_list[i])])

    if len(sen_score_list) == 0:
        return 0
    cs = ClacSentiment()
    sentiment_list, words = cs.get_sen(depend_list)
    sentiment = get_sentiment(sen_score_list, sentiment_list)
    return sentiment, words

def senti_main():
    sentiment_score = []
    for j in range(len(df_prod)):
        name = df_prod.iloc[j,0]
        pro_comments = df_prod.iloc[j,10]
        add_comments = df_prod.iloc[j,11]
        mid_comments = df_prod.iloc[j,12]
        con_comments = df_prod.iloc[j,13]
        all_comments = name+pro_comments+add_comments+mid_comments+con_comments
        print("No.{} products analysis processing.".format(j))
    
        sentiment, words = clac_sentiment(name, all_comments)
        sent_matrix = [sentiment, "|".join(words)]
        sentiment_score.append(sent_matrix)
        print(sent_matrix)
    
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = 'sentiment_scores' 
    sheet['A1'] = 'sentiment'
    sheet['B1'] = 'words'
    
    for sent_score in sentiment_score:
        sheet.append(sent_score)
        
    filename = 'jd_sentiment_scores.xlsx'
    wb.save(filename)
    
    return sentiment_score

if __name__ == "__main__":
    senti_scores = senti_main()