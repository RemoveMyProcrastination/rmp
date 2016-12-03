#!/bin/bash

# -- create a user --
curl -v -X POST -H "Content-Type: application/json" localhost:5000/user/ -d '{
    "username": "johndoe",
    "password": "hello world",
    "email": "jdoe@gmail.com"
}'; echo ''


# # -- create an invalid user --
# curl -v -X POST -H "Content-Type: application/json" localhost:5000/user/ -d '{
#     "username": "@!!!#@#",
#     "password": "hello world",
#     "email": "jdoe@gmail.com"
# }'; echo ''


# # -- login a user (get authorization) --
# curl -v -X POST -H "Content-Type: application/json" \
# localhost:5000/user/login/ -d '{
#     "username": "johndoe",
#     "password": "hello world"
# }'; echo ''


# # -- get user --
# curl -v -X GET -H "Content-Type: application/json" \
# -H "Authorization: Basic am9obmRvZTpoZWxsbyB3b3JsZA==" \
# localhost:5000/get/; echo ''


# # -- delete user --
# curl -v -X DELETE -H "Content-Type: application/json" \
# -H "Authorization: Basic am9obmRvZTpoZWxsbyB3b3JsZA==" \
# localhost:5000/user/; echo ''
