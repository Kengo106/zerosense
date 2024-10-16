# zerosense
## サイト概要

「競馬は興味があるけれど実際にお金をかけたくはない」<br>
そういった人のために、実際のお金を賭けることなく競馬を楽しむことができるアプリです。<br>
このアプリでは、もし本当に馬券を購入していたらどれだけの利益があったのかを計算し、その利益を仲間内で競い合うことができます。<br>
実際にお金はかけないので、競馬の「センス」が「ゼロ」の人でも楽しむことができます。


url:https://develop-matsushima.an.r.appspot.com/

## サイト詳細

<details>
  <summary>ゲーム概要</summary>

会員は「大会」に参加し、ほかの大会参加者と各レースに対する投票を行いスコアを競い合う。

</details>
<details>
  <summary>投票方法</summary>
  
大会参加者は投票対象のレースに対し以下の投票を行う:

- **◎(本命)**: 一番目に上位に入ると予想する馬を選ぶ
- **〇(対抗)**: 二番目に上位に入ると予想する馬を選ぶ
- **▲(大穴)**: 三番目に上位に入ると予想する馬を選ぶ
- **コメント**: レースに関するコメントを書く（スコアには関係なし）

</details>
<details>
  <summary>スコア化のルール</summary>
  
- 大会参加者は投票をもとに以下のルールで馬券を買ったこととし、スコアが計算される。
  
- 馬券はそれぞれ100円として計算され、合計で11枚購入される。

1. **単勝（◎）**：予想された本命馬（◎）が1着になることを予想。
2. **複勝（◎）**：予想された本命馬（◎）が3着以内に入ることを予想。
3. **馬単（◎-⚪︎）**：予想された本命馬（◎）が1着、対抗馬（⚪︎）が2着になる順番を予想。
4. **馬連（◎,⚪）**：予想された本命馬（◎）と対抗馬（⚪︎）がどちらかが1着、もう一方が2着以内に入ることを予想（順番は問わない）。
5. **馬連（◎,▲）**：予想された本命馬（◎）と大穴馬（▲）がどちらかが1着、もう一方が2着以内に入ることを予想（順番は問わない）。
6. **馬連（⚪,▲）**：予想された対抗馬（⚪︎）と大穴馬（▲）がどちらかが1着、もう一方が2着以内に入ることを予想（順番は問わない）。
7. **ワイド（◎,⚪）**：予想された本命馬（◎）と対抗馬（⚪︎）がどちらも3着以内に入ることを予想。
8. **ワイド（◎,▲）**：予想された本命馬（◎）と大穴馬（▲）がどちらも3着以内に入ることを予想。
9. **ワイド（⚪,▲）**：予想された対抗馬（⚪︎）と大穴馬（▲）がどちらも3着以内に入ることを予想。
10. **三連複（◎,⚪,▲）**：予想された本命馬（◎）、対抗馬（⚪︎）、大穴馬（▲）の3頭がどの順番でも良いので3着以内に入ることを予想。
11. **三連単（◎-⚪-▲）**：予想された本命馬（◎）が1着、対抗馬（⚪︎）が2着、大穴馬（▲）が3着になる順番を予想。
- レースの結果が出た後、これらのルールに基づいて購入された場合の利益をスコア化し、他の参加者と競う。

</details>
<details>
  <summary>投票対象のレース</summary>
週末に開催される重賞レース

</details>
<details>
  <summary>締切時間のルール</summary>
レースの発走時間の時間帯（例: 3:40発走なら3時台）の1分前まで。
  
- 例: 3:00～3:59の間に発走するレースの締切は、2:59まで。

</details>

## 使用技術
- python 3.11.1
  - Django 5.2.4
  - Django REST Framework 3.14.0
- TypeScript 5.1.3
  - Angular 16.1.0
- PostgreSQL 14.7
- GCP
  - App Engine
  - Cloud Run
  - Cloud SQL
- Github actions
- docker 
- terraform 1.6.6
- Firebase
- swagger



## インフラ構成図

![インフラ構成図_20240106 drawio](https://github.com/Kengo106/zerosense/assets/131678198/a43d66a5-12ca-409f-a2c7-18d17828b4d8)



<br>※スクレイピングするためのアプリケーションはこちらにあります。https://github.com/Kengo106/zerosense_scraping

## API仕様
<br>
swaggerにて記載
<br>https://kengo106.github.io/zerosense/dist/index.html

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

