# Description

https://zenn.dev/ozushi/articles/ebe3f47bf50a86 と Carrier-Owl (https://github.com/fkubota/Carrier-Owl) を参考に、毎日 Dicord に新着 arXiv を通知する Bot を作りました。

## 特徴

- 複数のキーワードに興味の度合いを設定
- 論文のキーワードヒット数とキーワードの優先度がしきい値以上である論文を厳選
- タイトルの和訳・アブストの 3 行要約(日本語)を提供

# How to use

- リポジトリをForkする。
- OpenAI の API キーと Discord の webhook URL を取得し、secrets に登録。

![alt text](data/images/image-2.png)

![alt text](data/images/image-1.png)

![alt text](data/images/image.png)


- 適宜 config.yaml のキーワードを設定


これで Discord に通知されます。
