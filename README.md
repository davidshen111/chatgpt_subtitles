docker build -t myapp .
docker run --name myapp -p 8000:8000 myapp

curl --location 'http://127.0.0.1:8000/summaries/bilibili' \
--header 'Content-Type: application/json' \
--data '@/C:/work/chatgpt_subtitles/test/test1.json'