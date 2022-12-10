# Name

交代勤務引継ぎアプリ

このアプリケーションは交代勤務の方の引継ぎ業務の効率化と検索を容易にすることを目的としたアプリケーションです

# Description
このアプリケーションは、交代勤務の方の引継ぎ業務をSNS風に行うことで以下のメリットを得ることができます

### 画像の添付による具体性

トラブルなど発生した場合にその状態を画像に残すことで

口頭のみの引き継ぎに比べて、次の勤務者が状況を把握しやすくなります


### 返信機能による現在の状況の把握

トラブル発生の引継ぎを投稿することで、自分を含む勤務者全員がその投稿に返信を行うことができます

またトラブル解決のために行ったことを記載して返信することで

そのトラブルがどのような方法で解決されたかという記録を残すことができます


### タグ付けによる検索性の効率化

トラブルなどの引継ぎに対し、このアプリは様々なタグをつけることができます

これによって、後に同じようなトラブルが発生した時に

タグから検索することでトラブル解決のヒントを得ることができます


# Demo
##### 引継ぎ

![demo](https://raw.github.com/wiki/fjmtyy/koutai_kinmu_hikitsugi/img/引継ぎ.gif)

##### タグ検索

![demo](https://raw.github.com/wiki/fjmtyy/koutai_kinmu_hikitsugi/img/タグ検索.gif)

##### 返信

![demo](https://raw.github.com/wiki/fjmtyy/koutai_kinmu_hikitsugi/img/返信機能.gif)

# Requirement

```bash
cd handover_app
pip install -r requirements.txt
```

# .env file
.envはhandover_appディレクトリ直下に配置してください


```
SECRET_KEY=django's secret key
DEBUG=False for local, Ture for production
ALLOWED_HOSTS=127.0.0.1 for local, domain name for production
DATABASE_URL= Please provide the URL of the DB in each environment
AWS_STORAGE_BUCKET_NAME=NULL locally, AWS bucket name in production
AWS_INPUT_BUCKET_NAME=NULL locally, AWS bucket name in production
```

# start
requirementsをインストールして

.envを設定後に以下のbash
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
runserver後に以下のURLにアクセス

http://127.0.0.1:8000/login/

先ほどのcreatesuperuserにて作成したユーザーでログインできます


### 詳細設定
http://127.0.0.1:8000/admin/

上記にアクセスしてcreatesuperuserにて作成したユーザーでログインすると管理画面にて必要事項が設定できます


#### タグ
引継ぎ項目のタグの「追加」を押すとタグの作成ができます

タグを作成することで引継ぎを行うことができます


#### ユーザー作成
アカウント項目のユーザーの「追加」を押すとユーザー作成ができます

また、詳細設定として「ユーザー」を押して、IDを押すと詳細な情報が設定できます

ここでは名前とアバターを設定することで、引継ぎにその情報を付加することができます

また権限では「ユーザー」の権限を付与することで引継ぎの投稿や検索機能と返信機能を使用することができます


#### guest
上記のユーザー作成でusernameをguestで登録することで

password認証なしでゲストログインができます

ただし権限は「有効」のみを付与して下さい


# Note
このアプリケーションはDjangoを使用しています
versionは3.2.11です

Pythonは3.8.5にて動作確認をしています

DBはmariaDB 10.5にて動作確認をしています


# Author

藤本優也

zvgz_0t0p@gmail.com

# License
詳細はLICENSEをご覧ください

