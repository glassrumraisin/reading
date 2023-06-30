## 読書ペース管理アプリ
### 動画リンク:  <URL https://youtu.be/tk4jnjZaoV8>
### アプリリンク： <URL https://reading-3qka.onrender.com>
### 技術選定
#### フロントエンド
- HTML/CSS
- Bootstrap
#### バックエンド
- Python
- Flask
- SQL
#### その他
- openBD
書誌情報を提供するAPI  
ページ数を利用できるため採用  
Link: https://api.openbd.jp
## 機能
- 書籍のISBNコードを入力し,openBD内にその書籍が存在する場合,アプリのデータベースに情報を追加する
- 追加される情報はISBNコード,書籍名,著者,ページ数,出版社
- 日付を入力すると,その日に読み終わるために一日に読むべきページ数を表示する
- ページ数を入力すると,毎日そのページだけ読んだ場合,本を読み終わる日付を表示する
- データベースの要素はdeleteボタンをクリックすることで削除できる
