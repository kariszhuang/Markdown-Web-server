from flask import Flask, url_for, send_from_directory
import markdown


app=Flask(__name__)

@app.route('/')
def home():
    return "Home"


@app.route('/blog/<blog_name>')
def blog(blog_name):
    try:
        with open(f'./Blogs/{blog_name}.md') as blog:
            md_content=blog.read()
    except:
        return "<title>Error</title>Blog Name Error. Please try to change the blog's name after ~/blog/[name]"

    with open(f'./Blogs-template/template.html','r',encoding="utf-8") as template:
        html_template=template.read()

    html_content=markdown.markdown(md_content,extensions=['extra','codehilite','tables'])

    html=html_template.format(title=blog_name, content=html_content)
    return html

@app.route('/blog/images/<imgname>')
def find_image(imgname):
    return send_from_directory('./Blogs/images', imgname)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=3000)