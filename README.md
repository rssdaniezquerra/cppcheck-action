<div align="center">
<p align="center"><a href="https://github.com/deep5050/cppcheck-action"><img src="https://i.imgur.com/bDs8nfo.png" title="cpp-check action" align="center" height="180px" width="180px" /></a></p>

<p align="center"><h3 align="center">A github action to perform C/C++ code analysis using popular cppcheck tool</h3></p>

</div>

[![HitCount](http://hits.dwyl.com/deep5050/cppcheck-action.svg)](http://hits.dwyl.com/deep5050/cppcheck-action)
![Downloads](https://img.shields.io/github/downloads/deep5050/cppcheck-action/total?style=flat-square)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/deep5050/cppcheck-action?style=flat-square)



## What is cppcheck?

[cppcheck](https://github.com/danmar/cppcheck)  is a static analysis tool for C/C++ code. It provides unique code analysis to detect bugs and focuses on detecting undefined behavior and dangerous coding constructs.
The goal is to have very few false positives. Cppcheck is designed to be able to analyze your C/C++ code even if it has non-standard syntax (common in embedded projects).

## How to use?
Create ``cppcheck.yml`` under ``.github/workflows``
With the following contents

### Default configuration

```yml
name: cppcheck-action
on: [push]

jobs:
  build:
    name: cppcheck
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: cppcheck
        uses: deep5050/cppcheck-action@master
        with:
          github_token: ${{ secrets.GITHUB_TOKEN}}

```
### Advanced configuration

```yml
name: cppcheck-action
on: [push]

jobs:
  build:
    name: cppcheck
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: cppcheck
        uses: deep5050/cppcheck-action@master
        with:
          github_token: ${{ secrets.GITHUB_TOKEN}}
          check_library:
          skip_preprocessor:
          enable:
          exclude_check:
          inconclusive:
          inline_suppression:
          force_language:
          max_ctu_depth:
          platform:
          output_file:
```

### Input options

``check_library`` : ``enable`` Show information messages when library files have incomplete info.

``skip_preprocessor`` : ``enable`` Print preprocessor output on stdout and don't do any further processing.

``enable`` : Enable additional checks. The available ids are: ``all``, ``warning`` ,``style`` , ``performance`` , ``portability`` ,``information`` , ``unusedFunction`` ,``missingInclude`` . Default value is ``all`` if you want to enable multiple checking at once, separate them using ``,`` without any blank space.  example:  ``style,warning,performance``.

``exclude_check`` : Give a file or directory path to exclude from checking. example: ``./no_check.cpp``

``inconclusive`` : ``disable``,  default value is ``enable`` . Allow that Cppcheck reports even though the analysis is inconclusive.

``inline_suppression``: ``enable`` , default is ``disable`` . Enable inline suppressions. Use them by placing one or more comments, like: '// cppcheck-suppress warningId'.

``force_language`` : Forces cppcheck to check all files as the given language. Valid values are: ``c``, ``c++`` .

``max_ctu_depth`` :   Max depth in whole program analysis. The default value is 2. A larger value will mean more errors can be found but also means the analysis will be slower. Example : ``4``.

``platform`` : Specifies platform specific types and sizes. The available builtin platforms are: ``unix32`` ,``unix64`` , ``win32A`` , ``win32W`` ,``win64`` ,``avr8 `` , ``native``.

``output_file`` :  Give a filename for the output report. Default is ``./cppcheck_report.txt``



<b> For further details check [cppcheck documentations](http://cppcheck.sourceforge.net/manual.pdf) </b>
## License
>MIT License

>Copyright (c) 2020 Dipankar Pal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Thanks
Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
