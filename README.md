# langumo-ko
![PyPI](https://img.shields.io/pypi/v/langumo-ko?color=brightgreen)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/langumo-ko)
![PyPI - Format](https://img.shields.io/pypi/format/langumo-ko?color=orange)

한국어 말뭉치용 langumo parser 모음

## Introduction
`langumo-ko`는 [`langumo`](https://github.com/affjljoo3581/langumo)
라이브러리에서 사용할 수 있는 한국어용 `Parser`를 제공합니다. `langumo`를 사용하여
데이터셋을 빌드할 시, 해당 라이브러리에서 구현된 `Parser`를 사용하여 다양한 말뭉치
데이터를 간단하게 사용할 수 있습니다. `langumo-ko`가 지원하는 말뭉치 종류는 다음과
같습니다.

- [나무위키](https://namu.wiki/w/%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4:%EB%8C%80%EB%AC%B8)
  (`langumo_ko.NamuWikiParser`):
  나무위키 덤프 파일을 파싱합니다. 7z 형식으로 압축된 덤프 파일에 포함된 원본 json
  파일을 사용해야 합니다.
- [모두의 말뭉치](https://corpus.korean.go.kr/) - 신문 말뭉치
  (`langumo_ko.ModuNewsParser`): 모두의 말뭉치에서 제공하는 신문 말뭉치
  데이터를 파싱합니다.
- [모두의 말뭉치](https://corpus.korean.go.kr/) - 문어 말뭉치
  (`langumo_ko.ModuWrittenParser`): 모두의 말뭉치에서 제공하는 문어
  말뭉치 데이터를 파싱합니다.
- [모두의 말뭉치](https://corpus.korean.go.kr/) - 웹 말뭉치
  (`langumo_ko.ModuWebParser`): 모두의 말뭉치에서 제공하는 웹
  말뭉치 데이터를 파싱합니다.


## Installation

### With pip
`langumo-ko`는 [PyPI 저장소](https://pypi.org/)에 배포되어 있습니다. `pip`을
이용하여 다음과 같이 설치할 수 있습니다.

```bash
$ pip install langumo-ko
```

### From source
`pip`을 사용하는 대신, 해당 레포지토리를 내려받고 직접 빌드해 설치할 수 있습니다.

```bash
$ git clone https://github.com/affjljoo3581/langumo-ko.git
$ cd langumo-ko
$ python setup.py install
```

## Usage
[`langumo`](https://github.com/affjljoo3581/langumo)로 위에서 나열한 말뭉치를
빌드하기 위해서 다음과 같이 `build.yml`을 수정하면 됩니다.

```yaml
langumo:
  inputs:
  - path: src/NIKL_NEWSPAPER(v1.0).zip
    parser: langumo_ko.ModuNewsParser
  
  # other configurations...
```

## License
`langumo-ko` 라이브러리는 [Apache-2.0 라이센스](/LICENSE)를 갖습니다.