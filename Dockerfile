# 베이스 이미지는 Ubuntu 22.04를 사용합니다.
FROM ubuntu:22.04

# 패키지 목록을 업데이트하고 필요한 패키지를 설치합니다.
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        python3-fontforge \
        fontforge \
        sudo

# 작업 디렉토리를 /app으로 설정합니다.
WORKDIR /app

# 현재 프로젝트 내 script 폴더의 모든 내용을 컨테이너의 /app에 복사합니다.
COPY script/ .

# 컨테이너 실행 시 bash shell로 진입합니다.
CMD ["/bin/bash"]
