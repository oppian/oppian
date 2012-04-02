import markdown
import re
from pygments import highlight
from markdown.preprocessors import  Preprocessor
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

class CodeBlockPreprocessor(Preprocessor):
    def run (self, lines):
        new_lines = []
        seen_start = False
        lang = None
        block = []
        for line in lines:
            if line.startswith("@@") is True and seen_start is False:
                lang = line.strip("@@ ")
                seen_start = True
            elif line.startswith("@@") is True and seen_start is True:
                lexer = get_lexer_by_name(lang)
                content = "\n".join(block)
                highlighted = highlight(content, lexer, HtmlFormatter(linenos='table', cssclass="sourcecode", lineseparator="<br>"))
                new_lines.append("\n%s\n" % (highlighted))
                lang = None
                block = []
                seen_start = False
            elif seen_start is True:
                block.append(line)
            else:
                new_lines.append(line)
        return new_lines

class CodeExtension(markdown.Extension):
    """ Add source code hilighting to markdown codeblocks. """

    def __init__(self, configs):
        # define default configs
        self.config = {
            'force_linenos' : [False, "Force line numbers - Default: False"],
            'css_class' : ["codehilite", "Set class name for wrapper <div> - Default: codehilite"],
            }
        
        # Override defaults with user settings
        for key, value in configs:
            self.setConfig(key, value) 

    def extendMarkdown(self, md, md_globals):
        """ Add  to Markdown instance. """
        pyg = CodeBlockPreprocessor(md)
        pyg.config = self.config
        md.preprocessors.insert(0, "pygments", pyg) 

def makeExtension(configs={}):
    return CodeExtension(configs=configs)
