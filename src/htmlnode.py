class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """
        child class should override
        """
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""

        html = ""
        for prop in self.props.items():
            key, attribute = prop
            html += f'{key}="{attribute}"'

        return html

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
