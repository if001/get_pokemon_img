#crawler_img

[ポケモンだいすきクラブ](https://www.pokemon.jp/)のポケモン図鑑から画像を取ってきます。

## usage

```
python3 crawler_img.py start_id end_id
```

ポケモンのIDの区間を指定するとその間のポケモンの画像を取ってきます。

引数を与えなければ、ID001からID807(現在のポケモン数の最大値)を取ってきます。
画像はimg/に保存されます。

保存された画像のファイル名は、もともとのURLにある画像のファイル名で保存されます。

ポケモンの名前から画像を取得できるように、以下のようなフォーマットのoutput.cvsも同時に出力されます。

```
id, ポケモンの名前, 画像ファイル名
1, フシギダネ, 6274c667f64f562162580bbacbae8c5d.png
.
.
```

startとendの大小の比較などはおこなってないのでおかしな値を入れるとしにます。
