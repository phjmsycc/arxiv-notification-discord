# Description
https://zenn.dev/ozushi/articles/ebe3f47bf50a86 とCarrier-Owl (https://github.com/fkubota/Carrier-Owl) を参考に、毎日Dicordに新着arXivを通知するBotを作りました。

## 特徴 
- 複数のキーワードに興味の度合いを設定
- 論文のキーワードヒット数とキーワードの優先度がしきい値以上である論文を厳選
- タイトルの和訳・アブストの3行要約(日本語)を提供

# How to use
* pythonをインストール
* zipを解凍し適当なディレクトリに置く
* OpenAIのAPIキーとDiscordのwebhook URLを取得し、config.yamlに記載。
* 先程のディレクトリで
```bash
pip install -r requirements.txt
```

を実行
* config.yamlのキーワードを設定
* 以下を実行
```bash
python paper_arxiv.py
```

これでDiscordに通知されます。
毎日通知させるにはもう少し作業が必要(PCにpythonスクリプトを定期実行させる設定or何かしらのクラウドサービスが必要)です。