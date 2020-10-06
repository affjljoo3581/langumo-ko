import os
import ijson
import zipfile
from typing import Iterable, IO
from langumo.building import Parser
from langumo.utils import AuxiliaryFile


class ModuBaseParser(Parser):
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
