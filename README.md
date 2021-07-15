# eSamudaay_task
Simple task on APIs

Hi Devs,

The Docker image size is 947MB

## The Steps to follow in order to Build and Start the Docker Container

# To install docker-compose

1. Run this command to download the current stable release of Docker Compose:
    ```
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    ```
2. Apply executable permissions to the binary:
    ```
    sudo chmod +x /usr/local/bin/docker-compose
    ```

# To build the container

```
docker-compose build
```

# To run the container

```
docker-compose up
```

## API endpoints present

    ```
    http://127.0.0.1:8000/calculate_order_value  # task api
    ```
### The Postman API collection is the docs folder.
Instead of providing screedshots, i have provided the api collection.

## Reason for using Bisect
    ```
    Bisect is used here to search the range index where the distance is going to be. It is used instead of if/else statements as bisect uses binary search which is faster
    than conditional statements.
    ```