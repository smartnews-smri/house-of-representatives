# 国会議案データベース：衆議院
- 衆議院の公式ウェブサイトから国会に提出された議案をデータベース化しました。
- 商用・非商用を問わず、自由にデータのダウンロードや検索が可能です。

## 背景

- 衆議院のウェブサイト「議案情報」では国会に提出された議案を確認できますが、検索や集計を行うには各ページに分かれたデータを整理する必要があります。
- そこでスマートニュース メディア研究所では、議案のデータを衆議院ウェブサイトから取得し、CSVやJSONなど機械判読可能なデータで公開するとともに、[閲覧用のページ](https://smartnews-smri.github.io/house-of-representatives/)を作成して自由に検索・集計できるようにしました。

![image_1280_640](https://user-images.githubusercontent.com/12462251/176733194-e9155042-2d85-48be-81b5-ebd8e113c050.png)

## 公開データの見方

- [/data](https://github.com/smartnews-smri/house-of-representatives/tree/main/data)にデータファイルを公開しています。原則としてCSVとJSONの両方で公開します。
  - [gian.csv](https://github.com/smartnews-smri/house-of-representatives/blob/main/data/gian.csv) / [gian.json](https://github.com/smartnews-smri/house-of-representatives/blob/main/data/gian.json)：すべての議案データを掲載したファイルです。途中経過も含むため、議案そのものの数よりも大きくなります。たとえば第150回国会に提出され、第151回で成立した議案は掲載回次「150」および「151」のデータが2行発生します。
    - 掲載回次：議案が掲載された国会の回次。
    - キャプション：議案情報ページのテーブルに付されたキャプション。
    - 種類〜審議状況：それぞれ議案情報ページにあるテーブルの同名列。
    - 経過情報 / 経過情報URL：議案情報ページにあるテーブル「経過情報」列のテキストとリンクURL。
    - 本文情報 / 本文情報URL：議案情報ページにあるテーブル「本文情報」列のテキストとリンクURL。
    - 議案種類〜議案提出の賛成者：それぞれ議案経過情報ページにあるテーブルの同名列。
    - なお「議案提出回次」「議案番号」「議案件名」は、それぞれ「提出回次」「番号」「議案件名」と重複するため掲載していない。
  - [gian_summary.json](https://github.com/smartnews-smri/house-of-representatives/blob/main/data/gian_summary.json)：gianから掲載回次の重複を排除したもの。
    - 提出回次、種類、番号、議案件名が同じものを同じ議案と判断しています。
    - データ構造の関係からJSON形式だけで公開しています。
  - [gian_status.csv](https://github.com/smartnews-smri/house-of-representatives/blob/main/data/gian_status.csv) / [gian_status.json](https://github.com/smartnews-smri/house-of-representatives/blob/main/data/gian_status.json)：gianから「審議状況」のデータを集計したもの。
  - [gian_type.csv](https://github.com/smartnews-smri/house-of-representatives/blob/main/data/gian_type.csv) / [gian_type.json](https://github.com/smartnews-smri/house-of-representatives/blob/main/data/gian_type.json)：gianから「種類」のデータを集計したもの。


## 閲覧用ページについて

- 本プロジェクトのデータを閲覧・検索できるページを公開しています。
- URL： https://smartnews-smri.github.io/house-of-representatives/
- 「集計情報」では成立した/撤回された議案の数、議案を提出した国会議員、政党別の議案への賛否などの集計を見ることができます。
- また「議案検索」では議案の件名や提出者、賛成・反対した政党名などから議案を検索できます。検索結果だけを選んでダウンロードすることも可能です。



## 二次利用とライセンスについて

- すべてのデータとソースコードは自由に閲覧・ダウンロードが可能です。
- GitHubプロジェクトのライセンスはMITライセンスとしており、商用・非商用を問わずご自由にお使いいただけます。
- ソースコード等を引用する際の著作権表記は「スマートニュース メディア研究所」または「SmartNews Media Research Institute」としてください。
- なお、本プロジェクトの利用によって生じたいかなる損害についても、開発者およびスマートニュース株式会社は一切責任を負いません。
