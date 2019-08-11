# TJA-Practice
> A small tool to extract a specific part from a TJA chart

## Requirements
- Python 3 (tested on 3.7)
- [pydub](https://github.com/jiaaro/pydub)
- ffmpeg

## Setting up

For instructions on how to install ffmpeg, please see [this page.](https://github.com/jiaaro/pydub#getting-ffmpeg-set-up)

### Using pipenv
```sh
pipenv install
```

### Without pipenv
```sh
pip install pydub
```

## Usage

### Using pipenv
```sh
pipenv run python tjapractice.py [tja file] [start time] [end time]
```

### Without pipenv
```sh
python tjapractice.py [tja file] [start time] [end time]
```

Both start time and end time are in milliseconds (ms).
After running the script, two new files should appear in the directory, both prefixed with `practice_`.

## Bugs / limitations
- Both the TJA and audio files must be in the same directory as the script
- Balloon counts are not handled properly
- Code is a goddamn mess please save me