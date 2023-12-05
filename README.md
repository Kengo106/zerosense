# zerosense
## サイト概要

競馬は興味があるけれど実際にお金をかけるのはちょっと、、、<br>
そういった人のために、実際のお金を賭けることなく競馬を楽しむことができるアプリです。<br>
このアプリでは、もし本当に馬券を購入していたらどれだけの利益があったのかを計算し、その利益を仲間内で競い合うことができます。

url:https://develop-matsushima.an.r.appspot.com/

## 使用技術
- python 3.1.1
  - Django 5.2.4
  - Django REST Framework 3.14.0
- TypeScript 5.1.3
  - Angular 16.1.0
- PostgraSQL 14.7
- GCP
  - AppEngine
  - Cloud SQL
- FireBase
## インフラ構成図

![インフラ構成図_20231206 drawio (2)](https://github.com/Kengo106/zerosense/assets/131678198/db4b9c75-0c80-497c-b950-b480db143046)



## ER図

![20231206_ER図](https://github.com/Kengo106/zerosense/assets/131678198/29443331-19ca-4f19-a4ac-b33c991bcdb7)

## 機能一覧
| 機能   |     説明      | 画面 |
| --- | ----------- | ------- |
| ユーザー登録機能   | ユーザー登録をする |       |
| ログイン機能    |ログインをする |     |
| ログアウト機能   | ログアウトをする |     |
| 大会一覧機能   |参加中の大会(投票結果による利益を競い合うグループ)一覧を作成する |    |
| 大会作成機能   |新しい大会を作成する |    |
| 大会検索機能   |大会コードから大会を探し、参加する |    |
| 大会情報表示機能   | 各ユーザーの成績情報の表示、今週の帳票対象のレースを表示する|    |
| 投票機能   | レースに対し投票を行う|    |
| レース結果表示機能   | 過去のレース結果を表示する||
| スクレイピング機能   | JRA日本中央競馬協会のホームページからレース結果を取得する|---|


