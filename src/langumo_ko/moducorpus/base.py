import os
import re
import ijson
import zipfile
from typing import Iterable, IO
import langumo_ko.utils as utils
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
        text = utils.normalize_quotes(text)
        text = utils.remove_duplicated_spaces(text)
        return text
