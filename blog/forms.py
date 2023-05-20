from django import forms  # Djangoフレームワークからformsモジュールをインポート
from .models import Comment  # カレントディレクトリの作成したmodels.py からCommentクラスをインポート

class CommentForm(forms.ModelForm):
    class Meta:  # コメントフォームと関連づけるクラスやフィールドを指定する
        model = Comment  # インポートしたCommentクラス
        fields = ["name", "email", "body"]  # Commentクラスで定義したものから選択

# forms.pyは入力フォームを定義するもの
