# HateBook REST API
A simple REST API made in Python in Flask. The only resources are User and his Posts and it's CRUD operations are limited by authentication implemented using JWT.
## Installation
```
cd hatebook-api
./run.sh
```
## Routes
* /users
* /users/{user_name}
* /users/{user_name}/posts
* /users/{user_name}/posts/{post_id}
* /login
## Resources
* User
  * name: string
  * password: string
  * posts: Post[]
* Post
  * id: number
  * author: User
  * text: string