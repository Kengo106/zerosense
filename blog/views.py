from http.client import HTTPResponse
from django.shortcuts import render, redirect  # renderはhtmlなどの情報をもとに描画データを作成する

from .forms import CommentForm
from .models import Post

def frontpage(request):  # urls.pyから呼ばれる
    posts = Post.objects.all()  # models.pyのPostの要素を取得
    return render(request, "blog/frontpage.html", {"posts":posts})  # クライアントからのリクエスト、htmlファイル、上で指定したpostsの要素をhtmlに結び付けて返す

def post_detail(request, slug):  # slugにはurls.pyの<slug:slug>で指定されたものが入る
    post = Post.objects.get(slug=slug)  # Postの中のslugが<slug:slug>で指定されたものを取得する
    
    if request.method == "POST":  # 送信ボタンを押してきた場合はPOSTなので以下の処理を始める
        form = CommentForm(request.POST)  # request.POST には、forms.pyで定義したname、email、body というキーがあり、それぞれにユーザーが入力した値が格納されている。
        print("Redirecting to post_detail")
        if form.is_valid():  # バリデーションルールがTrueであれば
            comment = form.save(commit=False)  # commentに対しform = CommentForm(request.POST)で定義した入力フォームからの入力を一時的に保存
            comment.post = post  # post(投稿)と結び付ける
            comment.save()  # .save()はデータベースに保存するメソッド
            print("Redirecting to post_detail")
            return redirect("post_detail", slug=post.slug)
        

    else:  
        form =CommentForm()

    return render(request, "blog/post_detail.html", {"post":post, "form":form})
    
    
    



