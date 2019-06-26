# wSentAnalyzer

![https://github.com/gustavotogni/wSentAnalyzer)](https://user-images.githubusercontent.com/19785036/60141859-b6871600-978d-11e9-9ef2-fbe4d861438c.png)

Our repository for a Python application that mines social network comments and classifies them according to the perceived prevailing sentiment using Machine Learning.

- Clarissa Rodrigues <clarissa.ar@gmail.com>
- Daniel Tamiosso <danieltamiosso@gmail.com>
- Gustavo Togni <gustavotogni@gmail.com>

# 1. Environment Setup

1. Download and install Python 3 from

> https://www.python.org/downloads/windows/

2. Run the following commands in cmd or similar terminal:

```
py -m pip install pandas
py -m pip install requests
py -m pip install squarify
py -m pip install sklearn
py -m pip install nltk
py -m nltk.downloader stopwords
```

4. To run the application:

- wAnalyzer is the main entry point.
- The 1st parameter is the path to the source csv file.
- If the provided file does not exist, the application will instantiate a WebCrawler and create one with life results from the web.

```
py wAnalyzer "source.csv"
```

# 2. Architecture

![Architecture Overview](https://user-images.githubusercontent.com/19785036/60141894-dd454c80-978d-11e9-9849-5dcdc9e1b178.png)

# 3. Inputs & Outputs

The Python program should be able to expect as input a CSV data-set with anonymized user-id and posts contents.

As output the program will provide a users‘ personality traits clustering about that social network sample and the feature set utilized as well as plots of interesting characteristics. The files are all created in "./output".