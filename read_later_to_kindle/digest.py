from os.path import abspath, dirname, join

from jinja2 import Environment, FileSystemLoader
from lxml.html import tostring
from newspaper import Article


HERE = dirname(abspath(__file__))


class DigestFactory:
    def create_digest(self, entries):
        for entry in entries:
            self._fetch_content(entry)
        html = self._get_digest_html(entries)
        path = "/tmp/digest.html"
        with open(path, "w") as f:
            f.write(html)
        return path

    def __init__(self):
        self.template_dir = join(HERE, "templates")
        self.template_loader = FileSystemLoader(self.template_dir)
        self.environment = Environment(loader=self.template_loader)

    def _clean_content(self, html):
        html = html.replace("\\n", "<br/>")
        return html

    def _fetch_content(self, entry):
        url = entry["href"]
        article = Article(url)

        try:
            article.download()
            article.parse()
        except Exception:
            content = ""
        else:
            if article.top_node is not None:
                content = tostring(article.top_node).decode()
            else:
                content = article.text
        finally:
            entry["content"] = self._clean_content(content)

    def _get_digest_html(self, entries):
        template = self.environment.get_template("digest.html")
        return template.render(entries=entries)
