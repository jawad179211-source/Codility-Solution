from flask import Blueprint, request, jsonify
import json
import os

post_routes = Blueprint('post_routes', __name__)
POST_FILE = "posts.json"

# Helper functions
def read_posts():
    if os.path.exists(POST_FILE):
        with open(POST_FILE, "r") as file:
            return json.load(file)
    return []

def write_posts(posts):
    with open(POST_FILE, "w") as file:
        json.dump(posts, file, indent=4)

# 2.1 Create Post
@post_routes.route('/posts', methods=['POST'])
def create_post():
    posts = read_posts()
    data = request.get_json()
    new_post = {
        "id": len(posts) + 1,
        "user_id": data.get("user_id"),
        "title": data.get("title"),
        "content": data.get("content")
    }
    posts.append(new_post)
    write_posts(posts)
    return jsonify({"message": "Post created", "post": new_post}), 201

# 2.2 Edit Post
@post_routes.route('/posts/<int:post_id>', methods=['PUT'])
def edit_post(post_id):
    posts = read_posts()
    data = request.get_json()
    for post in posts:
        if post["id"] == post_id:
            post["title"] = data.get("title", post["title"])
            post["content"] = data.get("content", post["content"])
            write_posts(posts)
            return jsonify({"message": "Post updated", "post": post})
    return jsonify({"message": "Post not found"}), 404

# 2.3 Delete Post
@post_routes.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    posts = read_posts()
    posts = [post for post in posts if post["id"] != post_id]
    write_posts(posts)
    return jsonify({"message": "Post deleted"}), 200

# 2.4 Get All Posts
@post_routes.route('/posts', methods=['GET'])
def get_all_posts():
    posts = read_posts()
    return jsonify(posts)

# 2.5 Get Post by Id
@post_routes.route('/posts/<int:post_id>', methods=['GET'])
def get_post_by_id(post_id):
    posts = read_posts()
    for post in posts:
        if post["id"] == post_id:
            return jsonify(post)
    return jsonify({"message": "Post not found"}), 404

# 2.6 Get posts by User Id
@post_routes.route('/posts/user/<int:user_id>', methods=['GET'])
def get_posts_by_user(user_id):
    posts = read_posts()
    user_posts = [post for post in posts if post["user_id"] == user_id]
    return jsonify(user_posts)
