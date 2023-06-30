## 読書ペース管理アプリ
### アプリリンク： <URL https://reading-3qka.onrender.com>
### 開発背景
私は読書が趣味であり,図書館を利用することも多い.  
その際,返却期限までにどれほどのペースで本を読む必要があるか,すぐに分かるアプリが欲しいと考え,製作した.
### 技術選定
#### フロントエンド
- HTML/CSS
	- 取り扱いが容易であるため
- Bootstrap
	- デザインをより洗練されたものにするため
#### バックエンド
- Python
	- 使い慣れているため
- Flask
	- Webアプリケーションの製作に向いているため
- SQL
	- 使い慣れているため
#### その他
- openBD
書誌情報を提供するAPI   
リンク: https://api.openbd.jp
	- ページ数を利用したかったため
## 機能
- 書籍のISBNコードを入力し,openBD内にその書籍が存在する場合,アプリのデータベースに情報を追加する
- 追加される情報はISBNコード,書籍名,著者,ページ数,出版社
- 日付を入力すると,その日に読み終わるために一日に読むべきページ数を表示する
- ページ数を入力すると,毎日そのページだけ読んだ場合,本を読み終わる日付を表示する
- データベースの要素はdeleteボタンをクリックすることで削除できる
### こだわった点
- 要素の削除や,日付・ページ数を変更した時,変更後の値がすぐに代入され,計算が行われるようにした点
