from django.db import models  # django.dbモジュールからmodelsをインポート

class Post(models.Model):  # 投稿のフィールドをデータベースに作成
    title =models.CharField(max_length=255)  # タイトルのフィールドを作成。以下同様
    slug = models.SlugField()
    intro = models.TextField()
    body = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):  # 投稿されたものにコメントをつけるフィールドを作成
    post = models.ForeignKey(  # postフィールドは外部キーを指定するものPostを外部キーとしてrelated_namedで指定しているcommentsはPostからアクセスする場合Post.commentsのように
        Post, related_name="comments", on_delete=models.CASCADE)  # Postに関連するComentsにアクセスできるon_delete=models.CASCADEのようにカスケードで指定できる

    name = models.CharField(max_length=255)
    email = models.EmailField()  

    body = models.TextField()
    posted_date = models.DateField()
    

