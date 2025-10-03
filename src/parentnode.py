from src.htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode requires a tag")

        if self.children is None:
            raise ValueError("ParentChild requires children")

        html_props = self.props_to_html()

        if html_props:
            html = f"<{self.tag} {html_props}>"
        else:
            html = f"<{self.tag}>"

        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"

        return html
