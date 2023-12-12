from flask import Flask, url_for, send_from_directory
import markdown
import re
from datetime import datetime
from flask import request



app=Flask(__name__)

@app.route('/')
def home():
    return "Home"+request.remote_addr


@app.route('/blog/<blog_name>')
def blog(blog_name):
    try:
        with open(f'./Blogs/{blog_name}.md') as blog:
            md_content = blog.read()
    except FileNotFoundError:
        return "<title>Error</title>Blog not found. Please check the blog's name."

    # Extract metadata and remove it from markdown content
    metadata, md_content = extract_and_remove_metadata(md_content)

    # Format metadata for HTML
    formatted_metadata = format_metadata(metadata)

    print(formatted_metadata, md_content)

    # Convert Markdown content to HTML
    html_content = markdown.markdown(md_content, extensions=['extra', 'codehilite', 'tables'])

    # Load template and inject metadata and content
    with open(f'./Blogs-template/template.html', 'r', encoding="utf-8") as template:
        html_template = template.read()

    html = html_template.format(title=blog_name, metadata=formatted_metadata, content=html_content)
    return html

def extract_and_remove_metadata(md_content):
    # General regex for key-value pairs
    metadata_regex = r'\[(.*?): (.*?)\]'
    metadata = {}

    # Turn to pairs. e.g. In markdown file: [Date: 12/24/24] [Author: John] => metedata= {"Date": "12/24/24", "Author": "John
    # 
    #  "}
    for match in re.finditer(metadata_regex, md_content):
        key, value = match.groups()
        metadata[key.strip()] = value.strip()
    # Remove metadata from the content
    md_content = re.sub(metadata_regex, '', md_content)
    return metadata, md_content.strip()

def format_metadata(metadata):
    formatted_metadata = ""
    for key, value in metadata.items():
        if key.lower() == 'date':
            try:
                # Convert date to readable format
                date_obj = datetime.strptime(value, '%d/%m/%y')
                value = date_obj.strftime('%b. %d %Y')
            except ValueError:
                value = "Invalid Date"
        # Append formatted metadata to string
        formatted_metadata += f"{key}: {value}<br>"
    return formatted_metadata





@app.route('/blog/images/<imgname>')
def find_image(imgname):
    try:
        return send_from_directory('./Blogs/images', imgname)
    except:
        return "Image error"

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=3000)