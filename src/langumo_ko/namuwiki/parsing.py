import ijson
from typing import Iterable
from langumo.building import Parser
from langumo.utils import AuxiliaryFile
import langumo_ko.utils as utils
from langumo_ko.namuwiki.rendering import NamuWikiRenderer


class NamuWikiParser(Parser):
    single_quotes_pattern = re.compile('[\x60\xb4\u2018\u2019]')
    double_quotes_pattern = re.compile('[\u201c\u201d]')

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
        filtered = []
        for line in NamuWikiRenderer.render(text).strip().splitlines():
            if (not line
                    or '.' not in line
                    or utils.korean_character_ratio(line) < 0.1):
                continue

            # Remove duplicated spaces.
            line = line.replace('\n', ' ').replace('\t', ' ')
            while '  ' in line:
                line = line.replace('  ', ' ')

            # Normalize the quotes by replacing unusual ones to the standard
            # ones.
            line = NamuWikiParser.single_quotes_pattern.sub('\'', line)
            line = NamuWikiParser.double_quotes_pattern.sub('"', line)

            filtered.append(line)

        return '\n'.join(filtered)
