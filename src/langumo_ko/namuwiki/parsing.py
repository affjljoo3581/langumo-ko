import ijson
from typing import Iterable
from langumo.building import Parser
from langumo.utils import AuxiliaryFile
import langumo_ko.utils as utils
from langumo_ko.namuwiki.rendering import NamuWikiRenderer


class NamuWikiParser(Parser):
    def extract(self, raw: AuxiliaryFile) -> Iterable[str]:
        with raw.open('r') as fp:
            for prefix, event, value in ijson.parse(fp):
                if not prefix.endswith('.text'):
                    continue

                # Skip the redirection pages.
                if value.lower().strip().startswith('#redirect'):
                    continue

                yield value

    def parse(self, text: str) -> str:
        text = NamuWikiRenderer.render(text)
        return '\n'.join([line for line in text.splitlines()
                          if utils.korean_character_ratio(line) > 0.1
                          and '.' in line])
