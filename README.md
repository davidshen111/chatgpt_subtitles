# 用OpenAI总结Bilibili字幕
## 简介
这是一个关于OpenAI的练习，通过调用OpenAI API实现对Bilibili视频字幕的总结。

本练习不涉及前端操作获取字幕，而是假设用户已经拿到字幕文件。
有两种方式输入字幕，一种方式是使用Restful消息将含有字幕的文件发送给程序，另一种方式是通过Gradio界面加载本地文件。

为了实现文件分割，采用了递归方法而不是依赖现有的第三方库。

程序提供了三种调用OpenAI API的方法。
在使用UI界面时，用户可以自行选择。
在远程发送消息时，默认的方法是直接调用OpenAI API。
这三种方法分别是：
- 直接调用OpenAI API。
- 使用langchain map-reduce类型的load_summarize_chain方法。
- 使用langchain refine类型的load_summarize_chain方法。

## GUI

![Screenshot 2023-06-10 105254](https://github.com/davidshen111/chatgpt_subtitles/assets/97799018/8b362272-79a3-400d-81da-f1bcf91e17e2)

## 结果对比
需要说明的是结果不仅和采用的方法有关，更重要的是由prompt的好坏来决定。
- OpenAI API
![Screenshot 2023-06-10 105816](https://github.com/davidshen111/chatgpt_subtitles/assets/97799018/95960b85-b1df-40a5-8983-983cb6b8c353)

- Langchain map-reduce
![Screenshot 2023-06-10 110145](https://github.com/davidshen111/chatgpt_subtitles/assets/97799018/a136088c-5c24-479b-a25f-58068e5fdaa8)

- Langchain refine
![Screenshot 2023-06-10 110702](https://github.com/davidshen111/chatgpt_subtitles/assets/97799018/128ded59-448b-4a5a-8409-00140517ae33)


## Docker Operation

- **Build the docker image**
```
docker build -t myapp .
```
下面是dockerfile的部分内容，表明容器启用本地UI。
如果想用远程方式，请注释掉ui.py这行，启用http_server.py这行。
```
#start the gradio ui
CMD ["python", "ui.py"]

#start the http serrver
# CMD ["python", "http_server.py"]
```
- **Start the docker**

For the HTTP Server
```
docker run --name myapp -p 8000:8000 myapp
```
For the Gadio UI
```
docker run --name myapp -p 7860:7860 myapp
```

- **The message example sent by curl command**
```
curl --location 'http://127.0.0.1:8000/summaries/bilibili' \
--header 'Content-Type: application/json' \
--data '@/C:/work/chatgpt_subtitles/test/test1.json'
```

- **Access the GUI**

Open http://127.0.0.1:7860/ in your local browser
