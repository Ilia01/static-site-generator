def extract_title(markdown):
    for line in markdown.split("\n"):
        if "#" in line and line.count("#") == 1:
            return line.strip("#" " ")
        else:
            raise Exception("There's no header in markdown", markdown)
