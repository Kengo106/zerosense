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
- docker 
- terraform 1.6.6
- Firebase



## インフラ構成図

![インフラ構成図_20231211](https://github.com/Kengo106/zerosense/assets/131678198/f77f8e51-0b55-428b-8610-4b55632611c9)


<br>※スクレイビングするためのアプリケーションはこちらにあります。https://github.com/Kengo106/zerosense_scraping/blob/main/README.md
## ER図

![20231206_ER図](https://github.com/Kengo106/zerosense/assets/131678198/29443331-19ca-4f19-a4ac-b33c991bcdb7)
## 画面遷移図

![画面遷移図_20231213](https://github.com/Kengo106/zerosense/assets/131678198/400e1c29-f733-4b14-abb0-274c5eaff2b6)


## 画面一覧
| 画面名   |説明| 画面 |
| --- | ----------- | ------- |
| アカウント登録  | ユーザー登録をする |   <img width="400" alt="新規登録" src="https://github.com/Kengo106/zerosense/assets/131678198/0a2b733f-ee92-4dca-b7bf-4d612bb767ef">   |
| ログイン   |ログインをする | <img width="400" alt="ログイン" src="https://github.com/Kengo106/zerosense/assets/131678198/1e25d9e9-7a36-4887-b6f8-348f166a627a">    |
| 大会選択   |参加中の大会(投票結果による利益を競い合うグループ)一覧を作成する | <img width="400" alt="大会選択画面" src="https://github.com/Kengo106/zerosense/assets/131678198/59cd010b-a43c-4510-a99d-126de858c55c">   |
| 大会メイン   | 各ユーザーの成績情報の確認、今週の帳票対象のレースを確認する。点数計算にはJRA日本中央競馬協会のホームページをスクレイピングし、レース結果を取得した結果をもとに計算しています。| <img width="400" alt="大会メイン画面" src="https://github.com/Kengo106/zerosense/assets/131678198/190123f7-f5d6-41d4-9ed4-4b7165600c75">   |
| 投票   | レースに対し投票を行う| <img width="400" alt="投票" src="https://github.com/Kengo106/zerosense/assets/131678198/9a60db5f-ffd6-4646-84e6-002e5b856e6a">   |
| レース結果選択   | 過去のレース一覧を確認する|<img width="400" alt="レース結果選択画面" src="https://github.com/Kengo106/zerosense/assets/131678198/90d6420f-d97f-48c5-8c64-932145653443">|
| レース結果確認   | 選択されたレースの結果を確認する|<img width="400" alt="過去レースの結果" src="https://github.com/Kengo106/zerosense/assets/131678198/0e973217-d758-465e-aad2-3720ca087fa4">|
| 大会作成   |新しい大会を作成する |   <img width="400" alt="大会作成" src="https://github.com/Kengo106/zerosense/assets/131678198/4a155d88-159e-47e7-9ad5-5cbee130c9b9">|
| 大会検索   |大会コードから大会を探し、参加する |  <img width="400" alt="大会検索" src="https://github.com/Kengo106/zerosense/assets/131678198/24a20e3b-11dc-4849-8be7-fcc68b5f22a6">  |
| アカウント情報  | アカウント情報を表示する | <img width="400" alt="ユーザー情報" src="https://github.com/Kengo106/zerosense/assets/131678198/64e9aa96-9006-4d9f-be4a-92e96aac7168">|
| アカウント削除  | アカウントを削除する | <img width="400" alt="アカウント削除" src="https://github.com/Kengo106/zerosense/assets/131678198/5a547046-1aca-4941-b7fb-0ece63eb7c1e">|

