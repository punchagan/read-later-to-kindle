from os.path import abspath, dirname, join
import tempfile

from jinja2 import Environment, FileSystemLoader
from lxml.html import tostring
from newspaper import Article

from send_to_kindle import send_to_kindle


HERE = dirname(abspath(__file__))
DIGEST_NAME = "rl2k-digest.html"
LOG_NAME = "{}.log".format(DIGEST_NAME)


class DigestFactory:
    """Create and send digests."""

    def create_digest(self, entries):
        for entry in entries:
            self._fetch_content(entry)
        html = self._get_digest_html(entries)
        path = join(tempfile.gettempdir(), DIGEST_NAME)
        with open(path, "w") as f:
            f.write(html)
        log_path = self._generate_log(entries)
        print("Digest created at {}".format(path))

        if self.send_email:
            send_to_kindle(path, log_path)
        else:
            print("Not sending email. Logs at {}".format(log_path))

        return path, log_path

    def __init__(self, dry_run):
        self.send_email = not dry_run
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

    def _generate_log(self, entries):
        log_path = join(tempfile.gettempdir(), LOG_NAME)
        with open(log_path, "w") as f:
            print("Generated Digest for the following entries:", file=f)
            for entry in entries:
                line = "{}: {}".format(entry["description"], entry["href"])
                print(line, file=f)
        return log_path

    def _get_digest_html(self, entries):
        template = self.environment.get_template("digest.html")
        return template.render(entries=entries)
