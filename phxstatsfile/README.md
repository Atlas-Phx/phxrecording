# phxstatsfile Toolkit
Phoenix tools for stats file

- phxstatsfile.py -- The lib to operate the stats file
- unit_tests.py -- Unit tests
- run_tests.ipynb -- Interactive unit test runner and function documentions
- stats_example -- An example stats file used by unit tests
- test_result.json -- Standard test result for unit test
- phxstatstojson -- Easy script to allow the JSON converter running directly from the OS
- phxstatsshrink -- Easy script to allow the shrinker running directly from the OS

### Quick start guide for calling phxstatsfile library in Python
1. Get header information
```python
import phxstatsfile as stats
stats.getstatsinfo("<path_to_stats>")
```

2. Convert to JSON file
```python
stats.tojsonfile("<path_to_stats>", "<path_to_json>")
```

3. Get partial data json
```python
startminute = 3
endminute = 10
json_str = stats.tojson("<path_to_stats>", startminute, endminute)
```

> **Detailed usage and examples please refer to the run_tests notebook.**

### Usage for calling phxstatstojson.py in OS command line
1. Get complete file converted to same directory with same name:
   ```shell
   python  .\phxstatstojson.py -i "C:\Users\xwork\Work\Phx\code\statsPython\phxstatsfile\stats_example"
   ```
   output:
   ```
   276709
   ```
   The command line will output how much data it wrote. You will get JSON file the same name as the source stas file.

2. Get specific n minutes of the stats instead all of the data
   ```shell
   python .\phxstatstojson.py -i "C:\Users\xwork\Work\Phx\code\statsPython\phxstatsfile\stats_example" -o "C:\Users\xwork\Work\Phx\code\statsPython\testout.json" -s 1 -e 3
   ```
   output:
   ```
   1809
   ```

3. Get help
   ```shell
   python  .\phxstatstojson.py -h
   ```
   output:
   ```
   usage: phxstatstojson.py [-h] [-i, --infile INPATH] [-o, --outfile OUTPATH] [-s, --startmin START] [-e, --stopmin STOP]
   A converter that converts Phoenix stats binary to json

    options:
    -h, --help            show this help message and exit
    -i, --infile INPATH   Specify stats file path
    -o, --outfile OUTPATH Specify output json file path, if not specified, will use the same path as the source file
    -s, --startmin START  Starting point of the output data, how many minutes from the recording start
    -e, --stopmin STOP    Stop point of the output data, how many minutes from the recording start
   ```

### Usage for calling phxstatsshrink.py in OS command line
1. Get specific n minutes of the stats (from minute 1 to minute 3 inclusive in following example)
   ```shell
   python .\phxstatsshrink.py -i "C:\Users\xwork\Work\Phx\code\statsPython\phxstatsfile\stats_example" -o "C:\Users\xwork\Work\Phx\code\statsPython\testout.bin" -s 1 -e 3
   ```
   output:
   ```
   1813
   ```
   > The command line will output how much data it wrote. 

2. Get help
   ```shell
   python  .\phxstatsshrink.py -h
   ```
   output:
   ```
   usage: phxstatstojson.py [-h] [-i, --infile INPATH] [-o, --outfile OUTPATH] [-s, --startmin START] [-e, --stopmin STOP]
   A shrinker that could pick a subset of minutes from Phoenix stats binary and spawn a new binary.

    options:
    -h, --help            show this help message and exit
    -i, --infile INPATH   Specify stats file path, required
    -o, --outfile OUTPATH Specify output json file path, required
    -s, --startmin START  Starting point of the output data, how many minutes from the recording start
    -e, --stopmin STOP    Stop point of the output data, how many minutes from the recording start
   ```