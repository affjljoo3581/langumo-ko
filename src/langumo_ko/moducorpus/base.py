import os
import re
import ijson
import zipfile
from typing import Iterable, IO
from langumo.building import Parser
from langumo.utils import AuxiliaryFile


class ModuBaseParser(Parser):
    single_quotes_pattern = re.compile('[\x60\xb4\u2018\u2019]')
    double_quotes_pattern = re.compile('[\u201c\u201d]')

    def _extract_json_file(self, fp: IO[str]) -> Iterable[str]:
        paragraph = []

        for prefix, event, value in ijson.parse(fp):
            if prefix == 'document.item.paragraph.item.form':
                paragraph.append(value)
            elif prefix == 'document.item.paragraph' and event == 'end_array':
                yield '\n'.join(paragraph)
                paragraph.clear()

    def extract(self, raw: AuxiliaryFile) -> Iterable[str]:
        with zipfile.ZipFile(raw.name, 'r') as zfp:
            for filename in zfp.namelist():
                if os.path.basename(filename).startswith('#'):
                    continue

                with zfp.open(filename, 'r') as fp:
                    yield from self._extract_json_file(fp)

    def parse(self, text: str) -> str:
        filtered = []
        for line in text.strip().splitlines():
            if not line:
                continue

            # Remove duplicated spaces.
            line = line.replace('\n', ' ').replace('\t', ' ')
            while '  ' in line:
                line = line.replace('  ', ' ')

            # Normalize the quotes by replacing unusual ones to the standard
            # ones.
            line = ModuBaseParser.single_quotes_pattern.sub('\'', line)
            line = ModuBaseParser.double_quotes_pattern.sub('"', line)

            filtered.append(line)

        return '\n'.join(filtered)
