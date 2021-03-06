import re
import pandas as pd
import time
from os import listdir
from os.path import isfile, join
from gazpacho import Soup
from sklearn.preprocessing import LabelBinarizer
from fire import Fire

# Aggregate html files in data folder
def find_html_files():
    html_files = []
    for file in listdir('data/'):
        if isfile(join('data/', file)):
            if file.endswith(".html"):
                html_files.append(file)
    return html_files

#html_files = find_html_files()
#html_files

# Soup the html file to be able to work on it
def souper_finder(name):
    soup = Soup(open(f"data/{name}").read())
    found = soup.find('tr', {'class' : 'transaction-row'})
    return found

# soup = Soup(open(f"data/test_page_1.html").read())
# found = soup.find('tr', {'class' : 'transaction-row'})

#found = souper_finder('test_page_1.html')

# Pull the date from the transaction and build it into a list
def date_ripper(found):
    dates = []
    for i in found:
        x = str(i.find('td', {'class' : 'transactionDate'}))
        x = (x.split('>')[2])
        x = (x.split('<')[0])
        dates.append(x)
    return dates

# dates = date_ripper(found)
#dates

# Pull the description from the transaction and build it into a list
def desc_ripper(found):
    desc = []
    for i in found:
        y = i.find('span', {'class' : 'transactionDescription'})
        desc.append(y)
    return desc

# desc = desc_ripper(found)
#desc

# Pull the value from the transaction and build it into a list
def val_ripper(found):
    val = []
    for i in found:
        z = str(i.find('span', {'class' : 'negative'}))
        val.append(z)
    return val

# val = val_ripper(found)
#val

# Pull the image string from the transaction and build it into a list
# def img_old(found):
#     img = []
#     for i in found:
#         a = str(i.img)
#         a = (a.split('=')[-1])
#         img.append(a)
#     return img

def img_ripper(found):
    img = []
    for i in found:
        a = str(i.find('img'))
        a = (a.split('='))
        if (len(a)>=3):
            a = a[2]
        else:
            a = 'check'
        img.append(a)
    return img

#img = img_new(found)
#img

# Build a dataframe from the lists
def frame_builder(dates, desc, val, img):
    tog = list(zip(dates, desc, val, img))
    df = pd.DataFrame(tog, columns=['Date', "Desc", "Value", "Category"])
    df.Value = df['Value'].str.extract("(\d*\.?\d+)").astype(float)
    df.Date = pd.to_datetime(df.Date)
    return df

#df = frame_builder(dates, desc, val, img)
#df

# Stack the previous functions and return a dataframe
def html_to_frames():
    html_files = find_html_files()
    df = pd.DataFrame(columns=['Date', "Desc", "Value", "Category"])
    for i in html_files:
        found = souper_finder(i)
        dates = date_ripper(found)
        desc = desc_ripper(found)
        val = val_ripper(found)
        img = img_ripper(found)
        xf = frame_builder(dates, desc, val, img)
        df = df.append(xf, ignore_index=True)
    return df

# Cleanup date and binarize the category
def frame_cleaner(df):
    # df.Value = df['Value'].str.extract("(\d*\.?\d+)").astype(float)
    df.Date = pd.to_datetime(df.Date)
    lb = LabelBinarizer()
    df = df.join(pd.DataFrame(lb.fit_transform(df['Category']),
                         columns=lb.classes_,
                         index=df.index))
    return df

# Export dataframe to excel file, using date as title
def xport_frame(df):
    timestr = time.strftime("%Y%m%d")
    excel = df.to_excel(f"output/{timestr}.xlsx")

# One function to rule them all.
def convert():
    frame = html_to_frames()
    df = frame_cleaner(frame)
    xport_frame(df)

#convert()

# Use Fire to make it a CLI
if __name__ == '__main__':
    Fire({
        'convert': convert,
    })
