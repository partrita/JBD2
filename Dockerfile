# 베이스 이미지는 Ubuntu 22.04를 사용합니다.
FROM ubuntu:22.04

# 패키지 목록을 업데이트하고 필요한 패키지를 설치합니다.
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        python3-fontforge \
        fontforge \
        sudo wget

# RUN pip install wget

# 작업 디렉토리를 /app으로 설정합니다.
WORKDIR /app

# 컨테이너 실행 시 bash shell로 진입합니다.
CMD ["/bin/bash"]
