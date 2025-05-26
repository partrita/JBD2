# JetBrainsMonoHangul

<div align="center">
    <img src="https://repository-images.githubusercontent.com/500120796/115b6aa3-1fc4-445d-914d-d35184754fa5">
</div>

[JetBrains Mono](https://github.com/JetBrains/JetBrainsMono)에 [D2Coding](https://github.com/naver/d2codingfont)의 한글 영역 (U+3131-U+318E, U+AC00-U+D7A3)을 덧씌운 뒤 폭을 조정한 폰트입니다. [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts)도 릴리즈에 포함되어 있습니다.

> 본래 이름을 JetBrains D2정도로 지으려고 했으나 D2Coding이 RFN 라이선스를 사용하는 바람에 JetBrains Mono Hangul로 이름을 지었습니다.

제가 확인해보았을때는 D2Coding 폰트는 RFN이 아니라 OFL 라이센스였습니다. 또한 폰트 이름이 길면 폰트 설정을 변경할 때 번거로움이 있어 이름을 새로 `JBD2`로 변경하였습니다.

## 다운로드

release 파일에서 `ttf`파일을 다운로드 할 수 있습니다.

## 로컬 환경에서 직접 build

> 로컬 시스템에 설치하는 것은 추천하지 않습니다. 대신 Docker를 사용하세요.

```bash
sudo apt install python3-fontforge
gh repo clone partrita/JetBrainsMonoHangul
cd JetBrainsMonoHangul
python build.py all
```

- `fontforge`는 pip에서 제공하지 않으므로 외부 패키지로 설치해야 합니다.  

## Config 파일 설명

```
download_path: 폰트 빌드에 필요한 파일을 다운로드할 위치. 기본값: 'assets'
out_path: 빌드한 폰드를 내보낼 위치. 기본값: 'out'
jetbrains_mono_version: 사용할 JetBrains Mono 폰트의 버전. 기본값: '2.304'
d2_coding_version: 사용할 D2Coding 폰트의 버전. 기본값: '1.3.2'
d2_coding_date: 사용할 D2Coding 폰트의 릴리즈 날짜. 기본값: '20180524'
jetbrains_mono_url: JetBrains Mono를 다운로드할 URL. 기본값: jetbrains_mono_version에 의해 자동 설정됨.
d2_coding_url: D2Coding을 다운로드할 URL. 기본값: d2_coding_version, d2_coding_date에 의해 자동 설정됨.
jetbrains_mono_name: JetBrains Mono를 다운로드할 때 사용할 이름. 기본값: 'JetBrains_Mono.zip'
d2_coding_name: D2Coding을 다운로드할 때 사용할 이름. 기본값: 'D2_Coding.zip'
d2_coding_width: 사용할 D2Coding의 글자 폭. 기본값: 1000
jetbrains_mono_width: 사용할 JetBrains Mono의 글자 폭. 기본값: 1200
use_system_wget: 외부 wget 사용 여부. 기본값: False
```

## License

OFL하에 배포됩니다. 자세한 것은 LICENSE 파일을 참조해주세요.
