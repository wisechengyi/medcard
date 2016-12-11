# medcard


medcard is an experimental program to extract information from images of common medical insurance cards.

## Setup

```
virtualenv -p python3.5 venv  # Python2.7 should be okay as well
source venv/bin/activate
pip install -r requirement.txt
```
Credential file can be generated at https://console.developers.google.com/apis/credentials

## Example Run
```
$ GOOGLE_APPLICATION_CREDENTIALS=<credential>.json python text_detection.py
1.jpg	 id: dzw 920000000, rxbin: 004336
2.jpg	 id: 999999876, rxbin: 610014
3.jpg	 id: None, rxbin: None
ERROR:__main__:sample_data/4.jpg does not have enough resolution
ERROR:__main__:sample_data/5.jpg does not have enough resolution
6.png	 id: 01234567890, rxbin: 003858
ERROR:__main__:sample_data/7.png does not have enough resolution
8.jpg	 id: 112345000, rxbin: 00000
9.jpg	 id: 2234567890, rxbin: 444444
10.jpg	 id: ykf3hzn 12345678, rxbin: 016499
11.jpg	 id: smpl0001, rxbin: 016580
12.png	 id: 307791123456, rxbin: 610014
13.png	 id: None, rxbin: 610241
15.jpg	 id: None, rxbin: 004336
16.png	 id: None, rxbin: 011867
17.png	 id: yom 000000031, rxbin: None
18.jpg	 id: None, rxbin: 003858
19.png	 id: 742449531 00, rxbin: 004336
20.png	 id: 999999991 group number 9999999, rxbin: 000000
ERROR:__main__:sample_data/21.jpg does not have enough resolution
```