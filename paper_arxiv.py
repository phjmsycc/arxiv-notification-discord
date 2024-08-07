import os
from discord_webhook import DiscordWebhook
import arxiv
import openai
import random
import time
import yaml
import datetime

def get_summary(result, model):
    system = """与えられた論文の要点を3点のみでまとめ、以下のフォーマットで日本語で出力してください。```
    『タイトルの日本語訳』
    ・要点1
    ・要点2
    ・要点3
    ```
    与える文章にはLaTeXの数式を含みます。
    """

    text = f"title: {result.title}\nbody: {result.summary}"
    response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {'role': 'system', 'content': system},
                    {'role': 'user', 'content': text}
                ],
                temperature=0.25,
            )
    summary = response['choices'][0]['message']['content']
    authors = ', '.join(result.author)
    title_en = result.title
    title, *body = summary.split('\n')
    body = '\n'.join(body)
    date_str = result.published.strftime("%Y-%m-%d %H:%M:%S")
    message = f"発行日: {date_str}\n{result.entry_id}\n{authors}\n{title_en}\n{title}\n{body}\n"
    
    return message

def get_config() -> dict:
    file_abs_path = os.path.abspath(__file__)
    file_dir = os.path.dirname(file_abs_path)
    config_path = f'{file_dir}/./config.yaml'
    with open(config_path, 'r', encoding='utf-8') as yml:
        config = yaml.load(yml, Loader=yaml.Loader)
    return config

def calc_score(abst: str, keywords: dict) -> (float, list):
    sum_score = 0.0
    hit_kwd_list = []

    for word in keywords.keys():
        score = keywords[word]
        if word.lower() in abst.lower():
            sum_score += score
            hit_kwd_list.append(word)
    return sum_score, hit_kwd_list

def search_keyword(
        articles: list, keywords: dict, score_threshold: float
        ) -> list:
    results = []
    key = []
    scores = []

    for article in articles.results():
        abstract = article.summary
        score, hit_keywords = calc_score(abstract, keywords)
        if (score != 0) and (score >= score_threshold):
            results.append(article)
            key.append(hit_keywords)
            scores.append(score)

    return results, key, scores


config = get_config()
api_key = os.getenv('OPENAI_KEY')
model = config['model']
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
subject = config['subject']
keywords = config['keywords']
score_threshold = float(config['score_threshold'])

# OpenAIのapiキー
openai.api_key = api_key
# Discord Webhookを初期化する
webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)

day_before_yesterday = datetime.datetime.today() - datetime.timedelta(days=2)
#     day_before_yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
day_before_yesterday_str = day_before_yesterday.strftime('%Y%m%d')
# datetime format YYYYMMDDHHMMSS
arxiv_query = f'({subject}) AND ' \
                f'submittedDate:' \
                f'[{day_before_yesterday_str}000000 TO {day_before_yesterday_str}235959]'

# arxiv APIで最新の論文情報を取得する
articles = arxiv.Search(
    query=arxiv_query,  # 検索クエリ（
    max_results=1000,  # 取得する論文数
    sort_by=arxiv.SortCriterion.SubmittedDate,  # 論文を投稿された日付でソートする
    sort_order=arxiv.SortOrder.Descending,  # 新しい論文から順に取得する
)

#queryを用意
# query ='ti:%22 Deep Learning %22'

results, words, scores = search_keyword(articles, keywords, score_threshold)

sorted_indices = [i for i, _ in sorted(enumerate(scores), key=lambda x: x[1], reverse = True)]
results = [results[i] for i in sorted_indices]
words = [words[i] for i in sorted_indices]
scores = [scores[i] for i in sorted_indices]


#searchの結果をリストに格納
# result_list = []
# for result in search.results():
#     result_list.append(result)
# #ランダムにnum_papersの数だけ選ぶ
# num_papers = 3
# results = random.sample(result_list, k=num_papers)

# 論文情報をDiscordに投稿する
for i,result in enumerate(results):
    keywords = words[i]
    score = scores[i]
    try:
        # Discordに投稿するメッセージを組み立てる
        message = "今日の論文です！ " + str(i+1) + "本目\n" + "スコア：" + str(score) + " キーワード：" + str(keywords) + "\n" + get_summary(result, model)
        # Discordにメッセージを投稿する
        webhook.content = message
        webhook.execute()
        print(f"Message posted.")
    except Exception as e:
        print(f"Error posting message: {e}")


# print(result_list)
