# nba-stats-viewer
## 概要
nba-stats-viewerは、NBAのゲームデータ(stats)をシンプルに閲覧できるウェブサイトです。  
https://nba-stats-viewer.site/

PythonとDjangoを用いて開発され、Dockerコンテナ化されています。データ取得は[rapidapi](https://rapidapi.com/api-sports/api/api-nba)を通じて行われ、CI/CDはGithub Actionsを用い、デプロイ先はAWSのECSです。

## 特徴
- NBAのゲームデータを効率的に閲覧可能
- クリーンで使いやすいUI
- Dockerを利用した環境構築
- Github ActionsによるCI/CD
- AWS ECSへの自動デプロイ
