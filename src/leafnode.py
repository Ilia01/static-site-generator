from src.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode requires a value")

        if self.tag is None:
            return self.value

        html_props = self.props_to_html()

        if html_props:
            return f"<{self.tag} {html_props}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
