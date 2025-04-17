from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


def validate_input(data):
    """Test if title and content are provided"""
    title = data.get("title")
    content = data.get("content")
    if not title:
      return jsonify({"error": "Title is required"}), 400
    if not content:
      return jsonify({"error": "Content is required"}), 400
    return True


def find_post_by_id(id):
    POSTS=load_posts()
    for post in POSTS:
        if id ==post['id']:
            return post


def save_post(POSTS):
    try:
        with open ("posts.json", "w") as p:
          json.dump(POSTS, p, indent = 4)
    except Exception as e:
        print(f"Unexpected error {e}")


def load_posts():
    if not os.path.exists("posts.json"):
        print("posts.json not found. Starting with empty post list.")
        return []
    try:
        with open("posts.json", "r") as p:
            return json.load(p)
    except json.JSONDecodeError:
        print("posts.json is not valid JSON. Starting fresh.")
        return []
    except Exception as e:
        print(f"Unexpected error while loading posts: {e}")
        return []


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    """displays all the posts stored in the Json or adds a post if the POST methode
    is used. Also supporting the sort function and paginated to 10 Posts per page"""
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    start_index = (page - 1) * limit
    end_index = start_index + limit
    POSTS = load_posts()
    paginated_posts = POSTS[start_index : end_index]
    if request.method == 'POST':
        new_post = request.get_json()
        validation_result = validate_input(new_post)
        if validation_result is not True:
            return validation_result
        try:
            new_id = max(post['id'] for post in POSTS) + 1
            new_post['id'] = new_id
        except ValueError:
            new_post['id'] = 1

        POSTS.append(new_post)
        save_post(POSTS)
        return jsonify(new_post)
    sort = request.args.get("sort")
    direction=request.args.get("direction")
    sorted_posts = POSTS
    if sort and direction:
        if direction == "desc":
            reverse=True
        else:
            reverse=False
        try:
            sorted_posts = sorted(POSTS, key = lambda post:post[sort], reverse=reverse)
            return jsonify(sorted_posts)
        except KeyError:
            pass
    return jsonify(paginated_posts)


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    POSTS = load_posts()
    post = find_post_by_id(id)
    if post is None:
        return jsonify({"error": "Post not found"}), 404
    post_index = POSTS.index(post)
    del POSTS[post_index]
    save_post(POSTS)
    return jsonify(POSTS)


@app.route('/api/posts/<int:id>', methods =['Put'])
def update_post(id):
    POSTS = load_posts()
    post = next((post for post in POSTS if post["id"] == id), None)
    if post is None:
        return jsonify({"error": "Post not found"}), 404
    new_data = request.get_json()
    for key in ["title", "content", "author", "date"]:
        if key in new_data:
            post[key] = new_data[key]
    post.update(new_data)
    save_post(POSTS)
    return jsonify(POSTS)


@app.route('/api/posts/search')
def filter_posts():
    title = request.args.get("title")
    POSTS=load_posts()
    if title:
        filtered_posts = [post for post in POSTS if post['title'] == title]
        return jsonify(filtered_posts)

    content = request.args.get("content")
    if content:
        filter_content = [post for post in POSTS if post['content'] == content]
        return jsonify(filter_content)


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error" : "Method not allowed"}), 405


if __name__ =="__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
