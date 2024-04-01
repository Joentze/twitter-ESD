# Getting Started with Y.com 👨🏽‍💻

Yapper.com, or Y.com, is a family-friendly microblogging platform like Twitter. Y.com prioritises content safety while allowing you to express yourself. Here's how to get started with Y.com locally.

Place the provided `.env` file in the root directory once the git repository `twitter-esd` is cloned.

Ensure that you have the following installed:

- Docker 🐳

To get started, run the following command:

```bash
docker compose up -d
```

To access the frontend, head to `http://localhost:3000` which is the containerised React App.

To stop all microservices, run the following command:

```bash
docker compose down
```

### Project Limitations:

- As we are utilising [**Hugging Face**](https://discuss.huggingface.co/t/what-is-model-is-currently-loading/13917) Inference API there might be some latency when making API calls at the start. This is because Hugging Face requires some time to load in the pre-trained model into their virtual machines due to limited resources. As a result, Uploading Posts may fail on first try.
- For the uploading of images, images are constrained to a size of approx. 65kb or less. We've observed that Minio fails to load in larger images, this may be a constraint with uploading files with RESTFul requests.
  - A potential solution in future is to use File Transfer Protocol (FTP)

## Directories

```bash
.
├── backend
│   ├── apis
│   │   ├── atomic
│   │   │   ├── asset
│   │   │   ├── comments
│   │   │   ├── content_check
│   │   │   ├── email
│   │   │   ├── follows
│   │   │   ├── likes
│   │   │   ├── posts
│   │   │   └── users
│   │   ├── auth
│   │   ├── complex
│   │   │   ├── read_posts
│   │   │   ├── upload_comment
│   │   │   └── upload_post
│   │   └── kong
│   ├── bucket
│   ├── database
│   └── rabbitmq
└── frontend
    ├── public
    └── src
```
