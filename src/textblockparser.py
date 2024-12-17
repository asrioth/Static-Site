class TextBlockParser():

    def markdown_to_blocks(markdown):
        lines = markdown.split('\n')
        blocks = []
        block = ""
        for line in lines:
            if line == "" and block == "":
                continue
            elif line == "" and block != "":
                blocks.append(block)
                block = ""
            elif block != "":
                block += "\n" + line
            else:
                block = line
        if block != "":
            blocks.append(block)
        return blocks
            