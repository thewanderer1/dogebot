#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Shantam
#
# Created:     25/12/2013
# Copyright:   (c) Shantam 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame
import os
import random
import praw,time,re
from collections import Counter

pygame.init()
basepic = pygame.image.load(os.path.join('shibe.jpg'))
picw,pich = basepic.get_size()
pygame.font.init()
# get sub
# figure out what the words are
# create the rects and make sure they dont overlap
# blit it on
# upload it to imgur and post

r = praw.Reddit('DogeBot')
already_done = []
r.login('chlorinequeen','password')
prefixes = ['much','so','very','such']

temp = 0

def GetPost():
    #RETURN FOUR MOST imp words in subs
    stop = open('stopwords')
    stow = stop.read();
    stows = re.findall(r'\w+',stow)
    cap_stows = [word.upper() for word in stows]
    stop.close()
    subreddit = r.get_subreddit('adviceanimals+dogecoin+')

    for submission in subreddit.get_hot(limit=20):
        print('doing a sub')
        submission.replace_more_comments(limit=None, threshold=0)
        fcomments = praw.helpers.flatten_tree(submission.comments) #arry of comments objects
        allbdy = ''
        for comments in fcomments:
            allbdy += comments.body

        #STRIP OUT NUMBERS AND URLS


        allbdy = re.sub(r'^https?:\/\/.*[\r\n]*', '', allbdy, flags=re.MULTILINE)
        allbdy = re.sub('[.1234567890_-]','',allbdy)

        words = re.findall(r'\w+', allbdy)
        corrwords = []

        cap_words = [word.upper() for word in words]

        for w in cap_words:
                if w not in cap_stows:
                    corrwords.append(w)

        word_counts = Counter(corrwords)
        mostcomm = word_counts.most_common(4)
        CreatImg([x[0] for x in mostcomm])
        print("done a sub")


def CreatImg(words):
    #create rects and make sure they dont' overplap and return and save the image
    normwords = [word.lower() for word in words]
    print('blitting')
    random.shuffle(prefixes)
    prinwords = []
    for p,w in zip(prefixes,normwords):
        prinwords.append(p+' '+w)
    font = pygame.font.SysFont("Comic Sans MS",24)#this works
    colarray = [(247,255,24),(255,0,0),(0,0,255),(0,255,0),(255,0,255)]

    random.shuffle(colarray)
    sc = []


    for w,color in zip(prinwords,colarray):
        i = 1
        w.strip()
        while i:
            scoretext=font.render(w, 1,color)
            textw,texth = scoretext.get_size()
            h = random.randrange(pich-texth)
            w = random.randrange(picw-textw)
            if(pygame.Rect(w,h,textw,texth).collidelist(sc) == -1):
                print(basepic.blit(scoretext, (w, h)))
                i = 0
        sc.append(pygame.Rect(w,h,textw,texth))

    pygame.image.save(basepic, "stuff.jpg")


def Finis(thread):
    #upload to imgur and post to thread
    pass


def main():
    GetPost()


    pygame.image.save(basepic, "stuff.jpg")

if __name__ == '__main__':
    main()


