docker build -t myapp .
# For http server
docker run --name myapp -p 8000:8000 myapp

# For Gadio UI
docker run --name myapp -p 7860:7860 myapp
http://127.0.0.1:7860/
curl --location 'http://127.0.0.1:8000/summaries/bilibili' \
--header 'Content-Type: application/json' \
--data '@/C:/work/chatgpt_subtitles/test/test1.json'