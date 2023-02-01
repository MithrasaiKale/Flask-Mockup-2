import csv
all_movies=[]
with open("final.csv") as f:
    r=csv.reader(f)
    data=list(r)
    all_movies=data[1:]
liked_movies=[]
disliked_movies=[]
did_not_watch=[]
