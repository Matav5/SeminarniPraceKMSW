from pathlib import Path
import numpy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math

DataSet = pd.read_csv(str(Path.cwd())+"\\2 - Vizualizace\\Dataset\\Dataset.csv")

def TypySongu(DataSet):
  
    '''
    Rozdělení songů podle typu:
        Album,
        Single,
        Kompilace
    '''
    grouped = DataSet.groupby(["Album_type"]).size()
    grouped = grouped.rename(lambda x: x.title())
    Indexes = grouped.index
    Indexes.name = ""

    print(Indexes)
    fig, ax = plt.subplots()
    grouped.plot().pie(x=grouped,labels=Indexes, autopct='%1.1f%%')
    ax.set_title("Rozdělení Alb do kategorií")

    plt.show()
    
#TypySongu(DataSet)



def KlasifikacePisnicek(DataSet):
    '''
    Koláčový graf songů které jsou:
        Live concert,
        Pouze Lyrics
        Acoustic,
    '''
    def zpracujDataSet(x):
        '''
        Vytáhnuto z popisu Datasetu:
            Speechiness: detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
            Acousticness: a confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.
            Instrumentalness: predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.
            Liveness: detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.
        '''
        x["Speechiness"] = x["Speechiness"] > 0.1 
        x["Acousticness"] = x["Acousticness"] > 0.9
        x["Instrumentalness"] = x["Instrumentalness"] > 0.6
        x["Liveness"] = x["Liveness"] > 0.8
        return x
    
    print(DataSet.columns)
    TypovyDataSet = DataSet[["#","Speechiness","Acousticness","Instrumentalness","Liveness"]]
    TypovyDataSet = TypovyDataSet.apply(zpracujDataSet, axis=1)

    SongCount = TypovyDataSet["#"].count()
    TypovyDataSet=TypovyDataSet[TypovyDataSet==True].count(axis=0)
    TypovyDataSet["Nezařazené"] = SongCount-sum(TypovyDataSet)
    TypovyDataSet=TypovyDataSet.rename(
        {
            "#":"Počet Songů",
            "Speechiness": "Se zpěvem",
            "Acousticness": "Akustické",
            "Instrumentalness": "Instrumentální",
            "Liveness": "Naživo"
        }
    )
    print(TypovyDataSet)

    bar_colors = ['black', 'green', 'red', 'yellow', 'blue']
    TypovyDataSet.plot.pie(colors=bar_colors)
    plt.show()

#KlasifikacePisnicek(DataSet)

def ShlednutiAStreamy(DataSet):
    views_duration = pd.DataFrame(zip(DataSet["Stream"],DataSet["Views"]), columns=['Stream','Views'])
    views_duration["Stream"] = views_duration["Stream"].apply(lambda x : x /1000000)
    views_duration["Views"] = views_duration["Views"].apply(lambda x : x /1000000)  
    views_duration = views_duration.sort_values(by="Views")
    views_duration = views_duration.reset_index(drop=True);
    views_duration = views_duration.groupby(pd.qcut(views_duration.index, 10)).mean()
    views_duration = views_duration.reset_index(drop=True);
    label1 = "Stream"
    label2 = "Views"
    fig,ax1 =  plt.subplots()
    

    views_duration["Stream"] = views_duration["Stream"].apply(lambda x : round(x,3))
    views_duration["Views"] = views_duration["Views"].apply(lambda x : round(x,3))  
    views_duration["ViewsRatio"] = views_duration["Views"] / (views_duration["Views"] +  views_duration["Stream"]) * 100
    views_duration["StreamRatio"] = views_duration["Stream"] / (views_duration["Views"] +  views_duration["Stream"]) * 100

    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: f"{y:.0f} Mil"))
    for index, row in views_duration.iterrows():
        p = plt.bar(str((index)*10)+"-"+str((index+1)*10)+"%",row["Stream"],width=0.6,label=label1, color="green")
        ax1.bar_label(p,fmt=f"{row.StreamRatio:.0f}%", label_type='center')
        p = plt.bar(str((index)*10)+"-"+str((index+1)*10)+"%",row["Views"],width=0.6,label=label2,bottom=row["Stream"],color="red")
        ax1.bar_label(p,fmt=f"{row.ViewsRatio:.0f}%", label_type='center')

    ax1.set_xlabel("Popularita (percentil)")
    ax1.set_ylabel("Průměr celkového počtu Shlednutí(YT)/Streamu(Spotify)")
    ax1.set_title("Podíl Shlednutí/Streamu podle popularity")
    ax1.legend(["Stream","Views"])
    print(views_duration)
    plt.show()

#ShlednutiAStreamy(DataSet)







def SongsAndLikes(DataSet):
    '''
        Youtube songy popularita a počet liků
    '''
    views_likes = pd.DataFrame(zip(DataSet["Views"],DataSet["Likes"]), columns=['Views','Likes'])
    views_likes = views_likes.dropna()
    views_likes = views_likes.sort_values(by="Views")
    views_likes = views_likes.reset_index(drop=True);
   
    label1 = "Views"
    label2 = "Likes"
    fig,ax1 =  plt.subplots()


    views_likes["LikesRatio"] = views_likes["Likes"] / views_likes["Views"] * 100
    views_likes["ViewsRatio"] = 100 -  views_likes["LikesRatio"]

    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x,pos: f"{x/1000000:.0f} Mil"))
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: f"{y /1000000:.0f} Mil"))
    ax1.stackplot(views_likes["Views"], (views_likes["Likes"],views_likes["Views"]))

    ax1.set_xlabel("Popularita (percentil)")
    ax1.set_ylabel("Průměr celkového počtu Shlednutí/Likesu")
    ax1.set_title("Podíl Shlednutí/Likesu podle popularity na YT")
    ax1.legend(["Likes","Views"])
    plt.show()

#SongsAndLikes(DataSet)



def PocetAPopularita(DataSet):
    '''
        Počet songů u muzikantů a jejich popularita Nedodělaný... Nevhodný Dataset obsahuje max 10 sognů pro Muzikanta
    '''
    artist_views = DataSet.groupby("Artist").agg({'#':'count', 'Views': 'sum','Stream': 'sum'})
    artist_views = artist_views.sort_values(by="#")
    artist_views = artist_views.reset_index(drop=True);
    print(artist_views.head())
    fig,ax1 =  plt.subplots()
    ax1.scatter(artist_views["#"], sum(artist_views["Views"],artist_views["Stream"]),s=1)
    plt.show()

#PocetAPopularita(DataSet)


def DelkaSongu(DataSet):
    duration = pd.DataFrame(zip(DataSet["Duration_ms"]), columns=['Duration_ms'])

    duration = duration.apply(lambda x : x /1000 / 60)
    duration = duration.sort_values(by="Duration_ms")

    duration = duration.reset_index(drop=True);
    aaaa = numpy.float64(len(duration.index) / 10)
    duration = duration.groupby(pd.qcut(duration.index, 10)).mean()
    duration = duration.reset_index(drop=True);
    fig,ax1 =  plt.subplots()

    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: f"{y:.0f} Min"))
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x,pos: f"{(x *aaaa):.0f}."))

    ax1.bar(duration.index,duration["Duration_ms"])
    plt.show()

DelkaSongu(DataSet) 

def TempoVSDelka(DataSet):
    duration = pd.DataFrame(zip(DataSet["Tempo"],DataSet["Duration_ms"]), columns=['Tempo','Duration_ms'])
    duration["Duration_ms"] = duration["Duration_ms"].apply(lambda x : x /1000 / 60)
    fig,ax1 =  plt.subplots()
    print(duration)
    ax1.scatter(duration["Tempo"],duration["Duration_ms"])
    plt.show()

TempoVSDelka(DataSet)


'''
    Korelace hluku a energičnosti písničky
'''
def HlukAEnergeticnost(DataSet):
    duration = pd.DataFrame(zip(DataSet["Loudness"],DataSet["Energy"]), columns=['Loudness','Energy'])
    duration = duration.sort_values(by="Loudness")
    duration = duration.reset_index(drop=True);

    fig,ax1 =  plt.subplots()
    ax1.scatter(duration["Loudness"],duration["Energy"],s=0.1)

    line = duration
    line = line.dropna()
    line["Loudness"] = line["Loudness"].apply(lambda x : math.floor(x))
    
    line = line.groupby("Loudness").mean()
    print(line) 
    ax1.plot(line.index,line["Energy"], label='Data', linewidth=1, color="red")
    plt.show()
HlukAEnergeticnost(DataSet)