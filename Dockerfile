FROM python:3.12.4-slim-bullseye
ENV GITLAB_TOKEN="dummy"
ENV SLEEP=600
ENV SHEET_ID="dummy"
ENV GOOGLE_SHEET_CREDENTIALS_FILE="gitlab-documentation.json"
ENV SHEET_NAME="Gitlab_Devops_Repositories"
RUN apt update
RUN apt upgrade -y
RUN pip3 install pygsheets datetime requests
RUN mkdir /app
RUN mkdir /app/gitlab
RUN useradd -ms /bin/bash gitlab
RUN chown -R gitlab: /app/gitlab
USER gitlab
WORKDIR /app/gitlab
ADD gitlab.py /app/gitlab
ADD gitlab-documentation.json /app/gitlab
#CMD ["tail","-f","/dev/null"]
CMD ["python3", "gitlab.py"]