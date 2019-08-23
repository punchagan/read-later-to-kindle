from newspaper import Article
from lxml.html import tostring

ARTICLE_TEMPLATE = """
<article style="page-break-after: always;">
<h1>{description}</h1>
<div class="content">
    {content}
</div>
</article>
"""

DIGEST_TEMPLATE = """
<html>
<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head>
<body>
{digest_content}
</body>
</html>
"""


class DigestFactory:
    def create_digest(self, entries):
        for entry in entries:
            self._fetch_content(entry)
        html = self._get_digest_html(entries)
        with open("/tmp/digest.html", "w") as f:
            f.write(html)

    def _get_digest_html(self, entries):
        digest_content = "\n".join(
            self._format_entry(entry)
            for entry in entries
            if entry.get("content")
        )
        return DIGEST_TEMPLATE.format(digest_content=digest_content)

    def _format_entry(self, entry):
        return ARTICLE_TEMPLATE.format(**entry)

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

    def _clean_content(self, html):
        html = html.replace("\\n", "<br/>")
        return html
