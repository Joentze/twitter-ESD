FROM golang:latest 

WORKDIR /app

COPY go.mod go.sum main.go .

RUN go build -o bin .

ENTRYPOINT ["/app/bin"]


