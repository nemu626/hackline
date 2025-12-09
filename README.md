# HackLine

Hack と LINE Seed JP を合成したプログラミングフォント。

## 特徴

- **ラテン文字**: Hack フォント由来（プログラミング向け等幅フォント）
- **日本語文字**: LINE Seed JP 由来（ひらがな、カタカナ、漢字 約7,100文字）

## ダウンロード

`build/` ディレクトリから以下のフォントをダウンロードできます：

- `HackLine-Regular.ttf`
- `HackLine-Bold.ttf`

## ビルド方法

### 必要なもの

- Python 3.x
- fonttools (`pip install fonttools`)

### ビルド手順

```bash
# ソースフォントをダウンロード
curl -L -o Hack-v3.003-ttf.zip https://github.com/source-foundry/Hack/releases/download/v3.003/Hack-v3.003-ttf.zip
unzip Hack-v3.003-ttf.zip -d hack_font

curl -L -o LINE_Seed_JP.zip "https://seed.line.me/src/images/fonts/LINE_Seed_JP.zip"
unzip LINE_Seed_JP.zip -d line_seed_font

# フォントを生成
python3 merge_fonts.py
```

## ライセンス

- **フォント**: SIL Open Font License 1.1
- **ビルドスクリプト**: MIT License

詳細は [LICENSE](LICENSE) を参照してください。

## クレジット

- [Hack](https://github.com/source-foundry/Hack) - Source Foundry
- [LINE Seed JP](https://seed.line.me/) - LY Corporation
