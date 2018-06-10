from .factories import PageFactory


def test_page():
    page = PageFactory.build(content="# Header")
    assert (
        page.content_as_html == '<h1 id="header">Header</h1>'
    ), "Expected content to be convertable to html"
