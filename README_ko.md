# HackLine

[Hack](https://github.com/source-foundry/Hack)과 [LINE Seed 폰트](https://seed.line.me/)를 합성한 프로그래밍 폰트, **HackLine**입니다.

[日本語](README.md)

## 특징

- **영문**: Hack 폰트 기반 (프로그래밍용 고정폭 폰트)
  - **전각:반각 = 5:3**: 전각 문자와 반각 문자가 5:3 비율인 wide font입니다. (2:1은 아직 없어요!)
- **일본어 문자**: LINE Seed JP 기반 (히라가나, 가타카나, 한자 약 7,100자)
- **한국어 문자**: 일본어와 한국어를 동시에 다루는 환경을 위해 LINE Seed JP와 KR을 추가한 **HackLine JK**
  - 한글은 일본어 문자와 같은 너비로 조정했습니다.
- **Nerd Font 지원**: 아이콘 폰트 (Devicons, Codicons, FontLogos 등)
- **전각 공백 시각화**: 일본어에서 자주 쓰이는 전각 공백(U+3000)을 시각적으로 식별할 수 있습니다.

| ![Sample](docs/HackLineSample.png) | ![Sample](docs/HackLineSampleClang.png) |
|---|---|


## 다운로드

[**Releases**](https://github.com/nemu626/hackline/releases/latest)에서 최신 버전을 다운로드할 수 있습니다.

### 배포 파일

| 파일명 | 내용 |
|-----------|------|
| `HackLine-vX.X.X.zip` | **기본 버전** (Regular, Bold) |
| `HackLineJK-vX.X.X.zip` | **JK(한글 지원) 버전** (Regular, Bold) |
| `HackLineNF-vX.X.X.zip` | **Nerd Font 버전** (아이콘 포함) |
| `HackLine-All-vX.X.X.zip` | 전체 세트 |

### 폰트 종류

| 폰트명 | 설명 |
|-----------|------|
| **HackLine-Regular/Bold** | 기본 폰트. 라틴 문자 + 일본어 |
| **HackLineNF-Regular/Bold** | Nerd Font 버전. 위 + 아이콘 (Devicons, Codicons, FontLogos, Octicons 등) |

> **💡 Tip**: 터미널이나 에디터에서 아이콘을 표시하려면 **NF 버전**을 사용하세요.

## 빌드 방법

### 필요 사항

- Python 3.x
- fonttools (`pip install fonttools`)
- `zip`, `unzip` 명령어

### 빌드 절차

```bash
# 자동 빌드 (기본 버전만)
./build.sh

# Nerd Font 버전도 포함하여 빌드
./build.sh --nerd
```

### 수동 빌드

```bash
# 소스 폰트 다운로드
curl -L -o Hack-v3.003-ttf.zip https://github.com/source-foundry/Hack/releases/download/v3.003/Hack-v3.003-ttf.zip
unzip Hack-v3.003-ttf.zip -d hack_font

curl -L -o LINE_Seed_JP.zip "https://seed.line.me/src/images/fonts/LINE_Seed_JP.zip"
unzip LINE_Seed_JP.zip -d line_seed_font

# Nerd Font patcher 다운로드 (선택)
curl -L -o FontPatcher.zip https://github.com/ryanoasis/nerd-fonts/releases/download/v3.3.0/FontPatcher.zip
unzip FontPatcher.zip -d font_patcher

# 폰트 생성
python3 merge_fonts.py

# Nerd Font 버전 생성
python3 add_nerd_glyphs.py
```


## 라이선스

- **폰트**: SIL Open Font License 1.1
- **빌드 스크립트**: MIT License

자세한 내용은 [LICENSE](LICENSE) 및 `/LICENSES`를 참조하세요.
참조한 폰트의 라이선스에 대해서는 각 폰트의 리포지토리를 참조하세요.

#### 참조 폰트

- [Hack](https://github.com/source-foundry/Hack) - Source Foundry
- [LINE Seed JP, Line Seed KR](https://seed.line.me/) - LY Corporation
- [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts) - Ryan L McIntyre

## 감사의 말
각 폰트를 배포해 주신 분들께 감사드립니다.
또한 일본어 합성 폰트와 Nerd Font 지원 등에 [yuru7](https://github.com/yuru7)님의 [HackGen](https://github.com/yuru7/HackGen) 작업을 참고했습니다. 감사합니다.
