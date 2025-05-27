# JetBrainsMonoHangul

![](./static/sample-invert.png)

[JetBrains Mono](https://github.com/JetBrains/JetBrainsMono)에 [D2Coding](https://github.com/naver/d2codingfont)의 한글 영역 (U+3131-U+318E, U+AC00-U+D7A3)을 덧씌운 뒤 폭을 조정한 폰트입니다. [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts)도 릴리즈에 포함되어 있습니다.

> 본래 이름을 JetBrains D2정도로 지으려고 했으나 D2Coding이 RFN 라이선스를 사용하는 바람에 JetBrains Mono Hangul로 이름을 지었습니다.

제가 확인해보았을때는 D2Coding 폰트는 RFN이 아니라 OFL 라이센스였습니다. 또한 폰트 이름이 길면 폰트 설정을 변경할 때 번거로움이 있어 이름을 새로 `JBD2`로 변경하였습니다.

## 다운로드

release 파일에서 `ttf`파일을 다운로드 할 수 있습니다. 파일명에 대한 설명은 아래를 참고하세요.

- `JBD2-Regular.ttf` : 일반 글꼴
- `JBD2-Regular.woff2` : 웹폰트용 글꼴
- `JBD2NF-Regular.ttf` : NF는 Nerd Font의 약자로, 일반 폰트와 icon 폰트를 의미.
- `JBD2NFM-Regular.ttf` : NFM은 Nerd Font Mono의 약자로, 고정폭 폰트를 의미.
- `JBD2NFP-Regular.ttf` :NFP는 Nerd Font Propo의 약자로, Proportional Font(비등폭 글꼴)을 의미합니다. 이는 일반적인 문장이나 GUI, 발표 자료 등과 같이 글자의 폭이 다른 경우에 적합합니다.
- `JBD2NL-Regular.ttf`: NL은 JetBrains에서 개발자를 위해 만든 서체인 JetBrains Mono에서 이음자(ligature) 기능을 제거한 버전입니다.

## 로컬 환경에서 직접 빌드하기

Docker를 사용하세요.

1. Repo 복사: 

```bash
gh repo clone partrita/JBD2
cd JBD2
``` 

2. Docker 이미지 빌드 (이미지 이름을 JBD2로 지정):

```bash
docker build -t JBD2 .
```

3. 빌드한 이미지를 bash로 실행 (인터랙티브 모드): 

```bash
docker run -it -v "$(pwd)":/app JBD2
```

4. 실행된 Docker 이미지 안에서 명령어를 실행합니다.

- `python build.py all`: 자동으로 setup 및 폰트 빌드
- `python build.py setup`: 폰트 파일 다운로드 및 압축 해제
- `python build.py build`: 폰트 병합 및 출력
- `python build.py clean`: 다운로드 및 출력 파일 삭제

## Config 파일 설명

아래는 config.py에 정의된 각 변수의 의미와 역할을 설명한 내용입니다.

### D2Coding Font Configuration

- **D2_CODING_VERSION**
  사용할 D2Coding 폰트의 버전입니다.
  예시: `'1.3.2'`

- **D2_CODING_DATE**
  사용할 D2Coding 폰트의 릴리즈 날짜입니다.
  예시: `'20180524'`

- **D2_CODING_URL**
  D2Coding 폰트 zip 파일을 다운로드할 URL입니다.
  `D2_CODING_VERSION`과 `D2_CODING_DATE` 값에 따라 자동으로 생성됩니다.

- **D2_CODING_ZIP_NAME**
  D2Coding 폰트 zip 파일을 다운로드할 때 사용할 파일명입니다.
  예시: `'D2_Coding.zip'`

- **D2_CODING_WIDTH**
  사용할 D2Coding 폰트의 글자 폭(advance width) 값입니다.
  예시: `1000`


### JetBrains Mono Font Configuration

- **JETBRAINS_MONO_VERSION**
  사용할 JetBrains Mono 폰트의 버전입니다.
  예시: `'2.304'`

- **JETBRAINS_MONO_URL**
  JetBrains Mono 폰트 zip 파일을 다운로드할 URL입니다.
  `JETBRAINS_MONO_VERSION` 값에 따라 자동으로 생성됩니다.

- **JETBRAINS_MONO_ZIP_NAME**
  JetBrains Mono 폰트 zip 파일을 다운로드할 때 사용할 파일명입니다.
  예시: `'JetBrains_Mono.zip'`

- **JETBRAINS_MONO_WIDTH**
  사용할 JetBrains Mono 폰트의 글자 폭(advance width) 값입니다.
  예시: `1200`


### Build & Path Configuration

- **DOWNLOAD_PATH**
  폰트 빌드에 필요한 파일(예: zip 파일, 임시 폴더 등)을 저장할 기본 경로입니다.
  예시: `'assets'`

- **BUILT_FONTS_PATH**
  빌드가 완료된 폰트 파일(TTF, WOFF2 등)을 저장할 경로입니다.
  예시: `'built_fonts'`

- **BUILT_FONT_FILENAME_BASE**
  빌드된 폰트 파일의 기본 이름(접두사)입니다.
  예시: `'JBD2'`

- **USE_SYSTEM_WGET**
  외부 시스템의 wget 명령어를 사용할지 여부를 지정합니다.
  예시: `False` (내장 Python 모듈 사용)


### 기타 경로 변수

- **DOWNLOAD_JETBRAINS_TTF_PATH**
  JetBrains Mono zip 파일을 풀었을 때, TTF 파일들이 위치하는 경로입니다.
  예시: `'assets/fonts/ttf'`

- **SOURCE_D2_CODING_FONT_PATH**
  D2Coding 폰트의 TTF 파일이 위치하는 경로입니다.
  예시: `'assets/D2Coding/D2Coding-Ver1.3.2-20180524.ttf'`

## License

OFL하에 배포됩니다. 자세한 것은 LICENSE 파일을 참조해주세요.
