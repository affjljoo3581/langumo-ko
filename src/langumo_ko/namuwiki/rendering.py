import re


class Renderer:
    def __init__(self, *rules: str):
        self.patterns = [re.compile(rule, re.IGNORECASE | re.MULTILINE)
                         for rule in rules]

    def replacement(self, match: re.Match) -> str:
        raise NotImplementedError()

    def render(self, source: str) -> str:
        for pattern in self.patterns:
            source = pattern.sub(self.replacement, source)
        return source


class InlineRenderer(Renderer):
    def replacement(self, match: re.Match) -> str:
        return match.groupdict().get('text', '')


class PaddedInlineRenderer(Renderer):
    def replacement(self, match: re.Match) -> str:
        return f" {match.groupdict().get('text', '')} "


class MacroRenderer(Renderer):
    def __init__(self):
        super().__init__(
            (r'\[\[(date|datetime|br|include|목차|tableofcontents|각주|footnote'
             r'|pagecount|youtube|nicovideo|wikicommons)(?:\(.+?\))?\]\]'),
            (r'\[(date|datetime|br|include|목차|tableofcontents|각주|footnote'
             r'|pagecount|youtube)(?:\(.+?\))?\]'),
            r'\[\[분류\:.*?\]\]')

    def replacement(self, match: re.Match) -> str:
        return ' '


class HTMLRenderer(Renderer):
    def __init__(self):
        super().__init__(
            r'\{\{\{\#\!html[ \t\n]+(?P<text>[\s\S]*?)\}\}\}',
            r'\[\[html[ \t]*\((?P<text>[^\)]*)\)\]\]')
        self.remove_tags = re.compile(r'</?[^>]+>')

    def replacement(self, match: re.Match) -> str:
        return self.remove_tags.sub('', match.group('text'))


class ImageRenderer(PaddedInlineRenderer):
    def __init__(self):
        super().__init__(
            (r'\[\[파일\:[ \t]*.*?\.(?:jpg|jpeg|png|gif)(?:\|[\&a-z\=\d\%]*)?'
             r'\]\]'),
            r'(?:https?|ftp).*?\.(?:jpg|jpeg|png|gif)(?:[\?\&a-z\=\d\%]*)?',
            (r'attachment\:[ \t]*[\"\']?.*?\.(?:jpg|jpeg|png|gif)'
             r'(?:[\?\&a-z\=\d\%]*)?[\"\']?'))


class HyperLinkRenderer(InlineRenderer):
    def __init__(self):
        super().__init__(
            r'\[\[[^\|\]]*\|(?P<text>[^\]]*)\]\]',
            r'\[\[\\(?P<text>\#[^\]]*?)(?:\#[^\]]*)?\]\]',
            r'\[\[(?P<text>[^\#][^\]]*?)(?:\#[^\]]*)?\]\]',
            r'\[\[\#(?P<text>[^\]]*)\]\]')


class HorizontalRuleRenderer(PaddedInlineRenderer):
    def __init__(self):
        super().__init__(r'-{4,10}')


class HeadingRenderer(PaddedInlineRenderer):
    def __init__(self):
        super().__init__(r'={1,}[ \t]+(.*?)[ \t]+\={1,}')


class TextDecorationRenderer(InlineRenderer):
    def __init__(self):
        super().__init__(
            r"'''(?P<text>.*?)'''",
            r"''(?P<text>.*?)''",
            r'(~~|--)(.*?)\1',
            r'__(?P<text>.*?)__',
            r'\^\^(?P<text>.*?)\^\^',
            r',,(?P<text>.*?),,',
            r'\{\{\{\+\d+[ \t]+(?P<text>.*?)\}\}\}',
            r'\{\{\{\#(?:[0-9a-f]+|[a-z]+)[ \t]+(?P<text>.*?)\}\}\}')


class MathRenderer(Renderer):
    def __init__(self):
        super().__init__(
            r'<math>(?P<text>.*?)</math>',
            r'\$(?P<text>.*?)\$',
            r'\[math\((?P<text>.*?)\)\]')

    def replacement(self, match: re.Match) -> str:
        text = match.group('text').strip()
        return text if len(text) < 3 else ''


class BoxTextRenderer(PaddedInlineRenderer):
    def __init__(self):
        super().__init__(r'\{\{\|(?P<text>[\s\S]*?)\|\}\}')


class TableRenderer(PaddedInlineRenderer):
    def __init__(self):
        super().__init__(r'\|.*?\|(?:<[^>]*>)*(?P<text>[^\|]*)')


class ListRenderer(PaddedInlineRenderer):
    def __init__(self):
        super().__init__(
            r'^[ \t]+\*[ \t]*(?P<text>.*)$',
            r'^[ \t]+[1AaIi]\.[ \t]*(?:\#\d+)?[ \t]*(?P<text>.*)$')


class QuoteRenderer(PaddedInlineRenderer):
    def __init__(self):
        super().__init__(r'\>+[ \t]*(?P<text>.*)')


class ExtensionRenderer(PaddedInlineRenderer):
    def __init__(self):
        super().__init__(
            r'\{\{\{\#\!syntax[ \t\n]+[\s\S]*?\}\}\}',
            (r'\{\{\{\#\!wiki[ \t\n]+style[ \t]*\=[ \t]*\".*?\"[ \t]*'
             r'(?P<text>[\s\S]*?)\}\}\}'),
            r'\{\{\{\#\!folding[ \t\n]+(?P<text>[\s\S]*?)\}\}\}')


class PlainTextRenderer(PaddedInlineRenderer):
    def __init__(self):
        super().__init__(r'\{\{\{(?P<text>[\s\S]*?)\}\}\}')


class CommentRenderer(PaddedInlineRenderer):
    def __init__(self):
        super().__init__(r'\#\#.*')


class RedirectionRenderer(PaddedInlineRenderer):
    def __init__(self):
        super().__init__(r'\#(?:redirect|넘겨주기)[ \t\n]+.*')


class FootnoteRenderer(Renderer):
    def __init__(self):
        super().__init__(
            r'\[\*[^ \t]+\]',
            r'\[\*[^ \t]*[ \t]+(?P<text>[^\[\]]*)\]')

    def replacement(self, match: re.Match) -> str:
        footnote = match.groupdict().get('text', '').strip()
        return f'({footnote})' if footnote else ''


class NamuWikiRenderer:
    renderers = [
        MacroRenderer(),
        HTMLRenderer(),
        ImageRenderer(),
        HyperLinkRenderer(),
        HorizontalRuleRenderer(),
        HeadingRenderer(),
        TextDecorationRenderer(),
        MathRenderer(),
        BoxTextRenderer(),
        TableRenderer(),
        ListRenderer(),
        QuoteRenderer(),
        ExtensionRenderer(),
        PlainTextRenderer(),
        CommentRenderer(),
        RedirectionRenderer(),
        FootnoteRenderer()]

    @staticmethod
    def render(source: str) -> str:
        for renderer in NamuWikiRenderer.renderers:
            source = renderer.render(source)

        # Remove duplicated spaces.
        while '  ' in source:
            source = source.replace('  ', '')
        source = '\n'.join([line.strip() for line in source.splitlines()])

        return source
