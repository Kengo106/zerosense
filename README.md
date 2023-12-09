# zerosense
## サイト概要

「競馬は興味があるけれど実際にお金をかけたくはない」<br>
そういった人のために、実際のお金を賭けることなく競馬を楽しむことができるアプリです。<br>
このアプリでは、もし本当に馬券を購入していたらどれだけの利益があったのかを計算し、その利益を仲間内で競い合うことができます。<br>
実際にお金はかけないので、競馬の「センス」が「ゼロ」の人でも楽しむことができます。


url:https://develop-matsushima.an.r.appspot.com/

## 使用技術
- python 3.11.1
  - Django 5.2.4
  - Django REST Framework 3.14.0
- TypeScript 5.1.3
  - Angular 16.1.0
- PostgraSQL 14.7
- GCP
  - AppEngine
  - Cloud SQL
- Github actions
- Firebase

## 画面構成
<img width="400" alt="ログイン" src="https://github.com/Kengo106/zerosense/assets/131678198/1e25d9e9-7a36-4887-b6f8-348f166a627a">
<br>
<img width="400" alt="新規登録" src="https://github.com/Kengo106/zerosense/assets/131678198/0a2b733f-ee92-4dca-b7bf-4d612bb767ef">
<br>
<img width="400" alt="大会選択画面" src="https://github.com/Kengo106/zerosense/assets/131678198/34741867-6681-44ed-a902-4c7bc7204e5c">
<br>
<img width="400" alt="大会メイン画面" src="https://github.com/Kengo106/zerosense/assets/131678198/190123f7-f5d6-41d4-9ed4-4b7165600c75">
<br>
<img width="400" alt="投票" src="https://github.com/Kengo106/zerosense/assets/131678198/9a60db5f-ffd6-4646-84e6-002e5b856e6a">

## インフラ構成図

![インフラ構成図_20231209 drawio](https://github.com/Kengo106/zerosense/assets/131678198/da78d697-a11a-475e-86a7-b5dcaf93c1d0)


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


