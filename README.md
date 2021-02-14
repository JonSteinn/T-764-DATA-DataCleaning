# Data cleaning
Finding duplicates of individual in an old Icelandic volleyball database that was in use
some time ago and is quite distorted.

**Note**
The data is private and therefore not included in the repository. Without it this won't work.

## Setup and run
Place the data files in `./data_cleaning/resources/` and run
```sh
pip install -r requirements.txt
python -m data_cleaning.main
```
This will take about 5 minutes to finish. The output is 
* A json file containing a map from the "original" to the copies
* A csv file with the groups of duplicates where groups are seperated by an empty entry
* A tikz picture with lines drawn for duplicates 

## Implementation
The detection is quite simple. We begin by grouping the individuals by first letter as
typos are rare for the first letter. This reduces the amount of comparisons we make.
Then we compare each entry in each group to every other with a similarity function and
if we match, they are declared as duplicates. A graph is used to group together those
that are the same individual. The entry with the earliest timestamp of each group is
used as the "original".

## Similarity 
We begin by mapping the names to lower case and replacing some Icelandic letters to
their English counterparts (e.g. ð becomes d). We also remove `dottir` and `son` from
names that end with either as it skews the comparison in favor of being duplicates.
We set an initial threshold at 0.95 but based on some criteria it can be lowered such
as if they share a birthday, email or phone. If they share no information we don't
even compare the names as two person can easily be named the same. Let `L` be the
Levenshtein distance between the two mapped names, `M` the length of the longer one
and `T` the threshold (possibly lower than 0.95). Two entries are considered to
be the same if `1-L/M > T`.
