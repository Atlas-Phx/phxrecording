# Author: Phoenix Geohysics Ltd.
# Creation: 2024-07-26

import phxstatsfile as stats
import os, json, difflib

# header reading test
def test1():
    dir = os.path.dirname(__file__)
    info = stats.getstatsinfo(os.path.join(dir, "stats_example"))
    if info["version"] == 1 and info["recordingid"] == "10766_2024-05-08-130213" and info["numchannels"] == 5 and info["duration(min)"] == 327:
        return "pass"
    else:
        return "fail"

# Reading data test
def test2():
    dir = os.path.dirname(__file__)
    resultJSON = json.loads(stats.tojson(os.path.join(dir, "stats_example"), 1, 2))
    with open(os.path.join(dir, "test_result.json"), "rb") as file:
        json_file = file.read()
    standardJSON = json.loads(json_file)
    a, b = json.dumps(resultJSON, sort_keys=True), json.dumps(standardJSON, sort_keys=True)
    if a == b:
        return "pass"
    else:
        d = difflib.SequenceMatcher(None, a, b)
        print("a: "+a)
        print("b: "+b)
        print(d.find_longest_match(), "total a: ", len(a), "total b: ", len(b))
        return "fail"

def run_tests():
    print("Test 1: " + test1())
    print("Test 2: " + test2())