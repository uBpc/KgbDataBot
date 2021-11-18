import praw
import matplotlib.pyplot as plt
import datetime
import time
def sort_dict_by_value(d, reverse = False):
  return dict(sorted(d.items(), key = lambda x: x[1], reverse = reverse))

CLIENT_ID = ""
SECRET_KEY = ""

reddit = praw.Reddit(username="",password="",client_id=CLIENT_ID,client_secret=SECRET_KEY,user_agent="KGB Daily Data by u/BpcU")
subreddit = reddit.subreddit("KGBTR")
day = datetime.datetime.now().day
vars = {
    "floods":{},
    "flooders":{},
    "freq_words":{},
    "commenters":{}
}
while True:
    try:

        for comment in subreddit.stream.comments(skip_existing=True):
            try:
                vars["commenters"][str(comment.author.name)] += 1
            except:
                vars["commenters"][str(comment.author.name)] = 1
            s = comment.body
            a = s.split(' ')
            for i in a:
                try:
                    vars["freq_words"][i] += 1
                except:
                    vars["freq_words"][i] = 1
            if len(a) >= 50:
                try:
                    vars["flooders"][str(comment.author.name)] += 1
                except:
                    vars["flooders"][str(comment.author.name)] = 1
                nm = ""
                for i in range(4):
                    nm += a[i]
                    nm += "\n"
                try:
                    vars["floods"][nm][0]  += 1
                except:
                    vars["floods"][nm] = [1,s]
            if datetime.datetime.now().hour == 18 and datetime.datetime.now().minute >= 0 and datetime.datetime.now().day != day:
                day = datetime.datetime.now().day
                break
        names = []
        top_floods = []    
        for base_key in vars:
            sorted_d = sort_dict_by_value(vars[base_key],True)
            fig = plt.figure(figsize=(10,10))
            axes = fig.add_axes([0.1,0.1,0.8,0.8])
            x,y = [],[]
            i = 0
            for key in sorted_d:
                x.append(key)
                if base_key == "floods":
                    y.append(sorted_d[key][0])
                    top_floods.append(sorted_d[key][1])
                else:    
                    y.append(sorted_d[key])
                i += 1
                if i >= 7:
                    break
            axes.bar(x,y)
            if base_key == "floods":
                axes.set_title(f"En çok paylaşılan {max(7,len(x))} flood")
            elif base_key == "flooders":
                axes.set_title(f"En çok flood atan {max(7,len(x))} kişi")
            elif base_key == "commenters":
                axes.set_title(f"En çok yorum atan {max(7,len(x))} kişi")
            else:
                axes.set_title(f"En çok kullanılan {max(7,len(x))} kelime")
            plt.xticks(fontsize=7)
            fig.savefig(f"{base_key}.png")
            names.append({"image_path":f"{base_key}.png"})
        subreddit.submit_gallery(title="KGB Günlük Veriler",images=names,flair_id="5fa2b1e2-cd1f-11e9-8ead-0e319e47d7bc")
        time.sleep(3)
        last_post = next(iter(reddit.redditor("NotBpc").submissions.new(limit=1)))
        rpl = f'''
        En çok paylaşılan {max(len(top_floods),3)} flood:
        '''
        for i in range(max(len(top_floods),3)):
            rpl += "\n"
            rpl += str(i+1) + '-'
            rpl += top_floods[i]
        last_post.reply(rpl)
        vars = {
            "floods":{},
            "flooders":{},
            "freq_words":{},
            "commenters":{}
        }
    except:
        time.sleep(30)
