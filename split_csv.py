#!/usr/bin/env python3
from typing_extensions import Final
from typing import List

import sys
import pandas 
from pathlib import Path

if (len(sys.argv) != 3):
    print("Usage: python3 split_csv.py chatlog.csv size")
    exit(1)

filename:Final = sys.argv[1]
size:Final[int] = int(sys.argv[2])

dataframe = pandas.read_csv(filename)
filename_without_extension = Path(filename).stem

count = 0
for split_dataframe in [dataframe.loc[i:i+size-1,:] for i in range(0, len(dataframe),size)]:
    count += 1
    new_file = filename_without_extension + str(count) + ".csv"
    print("Saving " + new_file)
    split_dataframe.to_csv(new_file, index=False)