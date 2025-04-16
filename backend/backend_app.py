from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]



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
    for post in POSTS:
        if id ==post['id']:
            return post

@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
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
        return jsonify(new_post)
    return jsonify(POSTS)

@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = find_post_by_id(id)
    if post is None:
        return jsonify({"error": "Post not found"}), 404
    post_index = POSTS.index(post)
    del POSTS[post_index]
    return jsonify(POSTS)


@app.route('/api/posts/<int:id>', methods =['Put'])
def update_post(id):
    post = find_post_by_id(id)
    if post is None:
        return jsonify({"error": "Post not found"}), 404
    new_data = request.get_json()
    post.update(new_data)
    return jsonify(POSTS)

@app.route('/api/posts/search')
def filter_posts():
    title = request.args.get("title")
    if title:
        filtered_posts = [post for post in POSTS if post['title'] == title]
        return jsonify(filtered_posts)

    content = request.args.get("content")
    if content:
        filter_content = [post for post in POSTS if post['content'] == content]
        return jsonify(filter_content)



if __name__ =="__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
