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
    grouped = grouped.rename(
        {
            "Compilation":"Kompilace",
            "Single": "Single"
        }
    )
    Indexes = grouped.index
    Indexes.name = ""

    fig, ax = plt.subplots()
    grouped.plot().pie(x=grouped,labels=Indexes, autopct='%1.1f%%')
    ax.set_title("Rozdělení Alb do typů")

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
        Zde jde o nastavení hranic jak moc chceme být jistý, že určité songy jsou určitého charakteru
        Vytáhnuto z popisu Datasetu:
            Speechiness: detects the presence of spoken words in a track. 
                The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 
                describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech,
                either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
            Acousticness: a confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.
            Instrumentalness: predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. 
                Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, 
                the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks,
                but confidence is higher as the value approaches 1.0.
            Liveness: detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live.
                A value above 0.8 provides strong likelihood that the track is live.
        '''
        x["Speechiness"] = x["Speechiness"] > 0.1 and x["Speechiness"] < 0.66
        x["Acousticness"] = x["Acousticness"] > 0.75
        x["Instrumentalness"] = x["Instrumentalness"] > 0.5
        x["Liveness"] = x["Liveness"] > 0.8
        return x
    
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
    
    bar_colors = ['black', 'green', 'red', 'yellow', 'blue']
    helpMe = TypovyDataSet.plot.pie(colors=bar_colors)
    helpMe.set_title("Rozdělení do kategorií")
    plt.show()

KlasifikacePisnicek(DataSet)

def ZhlednutiAStreamy(DataSet):
    views_duration = pd.DataFrame(zip(DataSet["Stream"],DataSet["Views"]), columns=['Stream','Views'])
    views_duration["Stream"] = views_duration["Stream"].apply(lambda x : x /1000000)
    views_duration["Views"] = views_duration["Views"].apply(lambda x : x /1000000)  
    views_duration = views_duration.sort_values(by="Views")
    views_duration = views_duration.reset_index(drop=True)
    views_duration = views_duration.groupby(pd.qcut(views_duration.index, 10)).mean()
    views_duration = views_duration.reset_index(drop=True)
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
    ax1.set_ylabel("Průměr celkového počtu Zhlednutí(YT)/Streamu(Spotify)")
    ax1.set_title("Podíl Zhlednutí/Streamu podle popularity")
    ax1.legend(["Stream","Views"])
    print(views_duration)
    plt.show()

ZhlednutiAStreamy(DataSet)

def SongsAndLikes(DataSet):
    '''
        Youtube songy popularita a počet liků
    '''
    views_likes = pd.DataFrame(zip(DataSet["Views"],DataSet["Likes"]), columns=['Views','Likes'])
    views_likes = views_likes.dropna()
    views_likes = views_likes.sort_values(by="Views")
    views_likes = views_likes.reset_index(drop=True)
   
    label1 = "Views"
    label2 = "Likes"
    fig,ax1 =  plt.subplots()
    print(f"Průměrný podíl je: {( views_likes['Likes'].sum() / (views_likes['Views'].sum() + views_likes['Likes'].sum()))*100}%")

    views_likes["LikesRatio"] = views_likes["Likes"] / views_likes["Views"] * 100
    views_likes["ViewsRatio"] = 100 -  views_likes["LikesRatio"]

    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x,pos: ""))
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: f"{y/1000000:.0f} mil."))
    ax1.stackplot(views_likes["Views"], (views_likes["Likes"],views_likes["Views"]),colors=("green","orange"))
    ax1.set_xlabel("Popularita (percentil)")
    ax1.set_ylabel("Počet zhlédnutí/Liků")
    ax1.set_title("Podíl zhlednutí/Liků podle popularity na YT")
    ax1.legend(["Likes","Views"])
    plt.show()

SongsAndLikes(DataSet)

def PopularitaADelkaSongu(DataSet):
    duration = pd.DataFrame(zip(DataSet["Duration_ms"],DataSet["Stream"],DataSet["Views"]), columns=['Duration_ms','Stream','Views'])

    duration = duration.apply(lambda x : x /1000 / 60)
    duration["Popularity"] = duration.apply(lambda x : x["Stream"] + x["Views"] ,axis=1)
    duration = duration.sort_values(by="Popularity")
    duration = duration.reset_index(drop=True)
    duration = duration.groupby(pd.qcut(duration["Popularity"], 10)).mean()
    duration = duration.reset_index(drop=True)
    fig,ax1 =  plt.subplots()

    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: f"{y:.1f} min"))
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x,pos: f"{x*10:.0f} %"))
    
 
    ax1.set_title("Průměrná délka písniček v po 10 percentilech")
    
    bars = ax1.bar(duration.index,duration["Duration_ms"],color="lightblue")
    ax1.bar_label(bars,fmt="%.2f")
    ax1.set_title("Korelace Popularity a délky songů")
    ax1.set_xlabel("Popularita")
    ax1.set_ylabel("Délka songů (v minutách)")
    plt.show()

PopularitaADelkaSongu(DataSet) 

'''
    Korelace hluku a energičnosti písničky
'''
def HlukAEnergeticnost(DataSet):
    duration = pd.DataFrame(zip(DataSet["Loudness"],DataSet["Energy"]), columns=['Loudness','Energy'])
    duration = duration.sort_values(by="Loudness")
    duration = duration.reset_index(drop=True)

    fig,ax1 =  plt.subplots()
    ax1.scatter(duration["Loudness"],duration["Energy"],s=0.1,color="orange")

    line = duration
    line = line.dropna()
    line["Loudness"] = line["Loudness"].apply(lambda x : math.floor(x))
    
    line = line.groupby("Loudness").mean()
    ax1.set_title("Korelace hluku a energičnosti")
    ax1.set_xlabel("Hlučnost (db)")
    ax1.set_ylabel("Energičnost")
    
    ax1.plot(line.index,line["Energy"], label='Data', linewidth=1, color="red")
    plt.show()
    
HlukAEnergeticnost(DataSet)



#Nezahrnuté Grafy

def TempoVSDelka(DataSet):
    duration = pd.DataFrame(zip(DataSet["Tempo"],DataSet["Duration_ms"]), columns=['Tempo','Duration_ms'])
    duration["Duration_ms"] = duration["Duration_ms"].apply(lambda x : x /1000)
    fig,ax1 =  plt.subplots()
    print(duration)


    ax1.scatter(duration["Tempo"],duration  ["Duration_ms"],linewidth=0.1)
    plt.show()

#TempoVSDelka(DataSet)

def PocetAPopularita(DataSet):
    '''
        Počet songů u muzikantů a jejich popularita Nedodělaný... Nevhodný Dataset obsahuje max 10 sognů pro Muzikanta
    '''
    artist_views = DataSet.groupby("Artist").agg({'#':'count', 'Views': 'sum','Stream': 'sum'})
    artist_views = artist_views.sort_values(by="#")
    artist_views = artist_views.reset_index(drop=True)
    print(artist_views.head())
    fig,ax1 =  plt.subplots()
    ax1.scatter(artist_views["#"], sum(artist_views["Views"],artist_views["Stream"]),s=1)
    plt.show()

#PocetAPopularita(DataSet)