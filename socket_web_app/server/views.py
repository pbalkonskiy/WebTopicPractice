def index() -> str:
    with open("../templates/index.html") as template:
        return template.read()


def blog() -> str:
    with open("../templates/blog.html") as template:
        return template.read()
