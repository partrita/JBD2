# JBD2 - JetBrains Mono Hangul

![GitHub release (latest by date)](https://img.shields.io/github/v/release/partrita/JBD2?style=flat-square)

![](./static/screenshot.png)

이 프로젝트 JBD2는 JetBrains Mono와 D2Coding의 장점을 결합했습니다. JetBrains Mono에 D2Coding의 한글 영역(U+3131-U+318E, U+AC00-U+D7A3)을 덧씌운 뒤 최적의 가독성을 위해 글자 폭을 조정했습니다. 또한 vim을 위한 Nerd Fonts도 포함되어 있습니다.

"JetBrains Mono Hangul"의 원작자인 서장협님은 원래 이름을 "JetBrains D2"로 지으려 했으나, D2Coding의 RFN 라이선스 때문에 "JetBrains Mono Hangul"로 명명했다고 말씀하셨습니다. 하지만 저는 개인적인 편의와 VS Code와 같은 에디터에서의 쉬운 사용을 위해 이 버전을 `JBD2`로 임의로 변경하여 배포합니다.

> 만약 이 이름 변경으로 인해 문제가 발생한다면 추후 수정하도록 하겠습니다.

## 변경 사항

- [x] 'heart' 글리프 매핑을 수정했습니다.

-----

## 폰트 다운로드

![](./static/sample-invert.png)

[release](https://github.com/partrita/JBD2/releases) 페이지에서 `ttf` 파일들을 직접 다운로드할 수 있습니다. 파일명에 포함된 용어에 대한 설명은 아래를 참고하세요.

  * `JBD2-Regular.ttf`: 일반 글꼴입니다. 주로 이 파일을 사용하시면 됩니다.
  * `JBD2-Regular.woff2`: 웹폰트 용도에 적합합니다.
  * `JBD2NF-Regular.ttf`: NF는 Nerd Font의 약자로, 일반 폰트와 다양한 아이콘 글리프를 포함합니다.
  * `JBD2NFM-Regular.ttf`: NFM은 Nerd Font Mono의 약자로, 고정폭 폰트를 의미합니다.
  * `JBD2NFP-Regular.ttf`: NFP는 Nerd Font Proportional의 약자로, 비등폭 글꼴을 의미합니다. 일반적인 텍스트, GUI, 프레젠테이션 등 문자의 폭이 다른 경우에 적합합니다.
  * `JBD2NL-Regular.ttf`: NL은 No Ligatures를 의미합니다. 개발자를 위해 디자인된 JetBrains Mono에서 합자(ligature) 기능이 제거된 버전입니다.


## 직접 빌드하기

Docker를 사용하여 직접 빌드하는 방법은 아래와 같습니다.

1.  먼저 저장소를 복제하고 Docker 이미지를 빌드합니다(이미지 이름을 `JBD2`로 지정):

    ```bash
    gh repo clone partrita/JBD2
    cd JBD2
    docker build -t jbd2 .
    ```

2.  빌드된 Docker 이미지를 인터랙티브 모드로 실행합니다:

    ```bash
    docker run -it -v "$(pwd)":/app jbd2
    ```

3.  Docker 컨테이너 안에서 다음 명령어를 실행할 수 있습니다:

      * `python3 scripts/build.py all`: 자동으로 설정하고 폰트를 빌드합니다.
      * `python3 scripts/build.py setup`: 필요한 폰트 파일을 다운로드하고 압축을 해제합니다.
      * `python3 scripts/build.py build`: 폰트를 병합하고 최종 결과물을 출력합니다.
      * `python3 scripts/build.py clean`: 다운로드된 파일과 출력 파일을 모두 삭제합니다.


## Config 설명

`config.py` 파일에는 폰트 빌드 프로세스를 제어하는 여러 변수가 정의되어 있습니다.


## 감사 인사

코딩하면서 한글 주석이 어색하게 보이는게 항상 불만이었는데, 이 문제를 해결해주신 서장협님(jhyub06@gmail.com)께 진심으로 감사드립니다.

## 라이선스

이 프로젝트는 OFL(Open Font License) 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조해주세요.
