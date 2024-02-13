from tkinter import *
from tkinter import scrolledtext
from bs4 import BeautifulSoup
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import time

def extractMetaData():
    st.config(state=NORMAL)
    global entetered_url
    entered_url = url.get()
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    response = requests.get(entered_url)

    soup = BeautifulSoup(response.content, 'html.parser')
    meta_tags = soup.find_all('meta')

    title = ''
    description = ''
    keywords = []

    for tag in meta_tags:
        if tag.get('property')=='og:title':
            title=tag.get('content')
        if tag.get('property')=='og:description':
            description=tag.get('content')
        if tag.get('name')=='keywords':
            keywords=tag.get('content')

    content = soup.get_text()
    tokens = word_tokenize(content)
    filtered_tokens = [token.lower() for token in tokens if token.lower() not in stop_words]
    stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
    preprocessed_content = ''.join(stemmed_tokens)

    stheading = "Meta data of geeksforgeeks.org"
    st.insert(END, stheading)
    st.insert(END, "\n\n")

    root.update_idletasks()
    time.sleep(0.5)

    title = "Title : "+title
    st.insert(END, title)
    st.insert(END, "\n\n")

    root.update_idletasks()
    time.sleep(1)
    
    description = "Description : "+description
    st.insert(END, description)
    st.insert(END, "\n\n")

    keywords = "Keywords : "+keywords
    st.insert(END, keywords)
    st.insert(END, "\n\n")
    
    preprocessed_content = "Preprocessed Content : "+preprocessed_content[0:200]
    st.insert(END, preprocessed_content)
    st.insert(END, "\n")
    st.config(state=DISABLED)

    with open('GFG_Meta.txt', 'w') as f:
        f.write(stheading)
        f.write('\n\n')
        f.write(title)
        f.write('\n\n')
        f.write(description)
        f.write('\n\n')
        f.write(keywords)
        f.write('\n\n')
        f.write(preprocessed_content) 

def myGui():
    global root, url, st
    root = Tk()
    root.title("Extracting meta data of GeeksforGeeks Website")
    root.geometry("500x500")
    root.resizable(0,0)
    root.config(bg="#99ffcc")

    url = Entry(root, font=('dubai', 15), relief = FLAT, fg="grey", bd=3)
    url.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.07)
    url.insert(0,"https://www.geeksforgeeks.org/")

    startBtn = Button(root, text="START", font=('dubai', 18), bd=4, bg="#ff9966", fg="white", command=extractMetaData)
    startBtn.place(relx=0.375, rely=0.24, relwidth=0.25, relheight=0.1)

    exitBtn = Button(root, text="EXIT", font=('dubai', 15), bd=3, bg="#ff3f3f", fg="white",command=root.destroy)
    exitBtn.place(relx=0.425, rely=0.4, relwidth=0.15, relheight=0.075)

    st = scrolledtext.ScrolledText(root, font=("courier",12), state=DISABLED, fg="#4f4c4c", relief=RIDGE, bd=4)
    st.place(relx=0.1,rely=.55,relwidth=0.8,relheight=0.3)
    
    root.mainloop()

myGui()
