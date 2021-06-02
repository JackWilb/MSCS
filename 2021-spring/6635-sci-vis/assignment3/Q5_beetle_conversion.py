from pathlib import Path

with Path('stagbeetle208x208x123.dat').open('rb') as in_file:
    with Path('stagbeetle208x208x123.raw').open('wb') as out_file:
        out_file.write(in_file.read()[6:])

with Path('stagbeetle832x832x494.dat').open('rb') as in_file:
    with Path('stagbeetle832x832x494.raw').open('wb') as out_file:
        out_file.write(in_file.read()[6:])