import numpy
import pandas as pd
import matplotlib.pyplot as plt

DataSet = pd.read_csv("C:\\Users\\Matav\\Desktop\\Python\\SeminarniPraceKMSW\\2 - Vizualizace\\Dataset\\Dataset.csv")

#Rozdělení songů podle typu (Album, Single, Kompilace)
grouped = DataSet.groupby(["Album_type"]).size()

print(type(grouped.index))
grouped = grouped.rename(lambda x: x.title())
Indexes = grouped.index
Indexes.name = ""

print(Indexes)
'''fig, ax = plt.subplots()
grouped.plot().pie(x=grouped,labels=Indexes, autopct='%1.1f%%')
ax.set_title("Rozdělení Alb do kategorií")

#plt.show()
'''

'''Koláčový graf songů které jsou:
        Live concert,
        Pouze Lyrics
        Acoustic,
'''


'''
Speechiness: detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
Acousticness: a confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.
Instrumentalness: predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.
Liveness: detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.
'''
print(DataSet.columns)
TypovyDataSet = DataSet[["#","Speechiness","Acousticness","Instrumentalness","Liveness"]]

def zpracujDataSet(x):
    x["Speechiness"] = x["Speechiness"] > 0.1 and x["Speechiness"] <= 0.9
    x["Acousticness"] = x["Acousticness"] > 0.9
    x["Instrumentalness"] = x["Instrumentalness"] > 0.6
    x["Liveness"] = x["Liveness"] > 0.8
#    x["TalkShow"] = x["Speechiness"] > 0.95

    return x
TypovyDataSet = TypovyDataSet.apply(zpracujDataSet, axis=1)

SongCount = TypovyDataSet["#"].count()
TypovyDataSet=TypovyDataSet[TypovyDataSet==True].count(axis=0)
TypovyDataSet["#"] = SongCount
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
#TypovyDataSet.plot.bar(rot=0, color=bar_colors)
#plt.show()


views_duration = pd.DataFrame(zip(DataSet["Stream"],DataSet["Views"]), columns=['Stream','Views'])

views_duration["Stream"] = views_duration["Stream"].apply(lambda x : x /1000000)
views_duration["Views"] = views_duration["Views"].apply(lambda x : x /1000000)  
views_duration = views_duration.sort_values(by="Stream")
#print(views_duration["Duration_ms"].apply(lambda x : x /1000))
#views_duration.plot(x = "Duration_ms", y = "Views", alpha=0.5)

fig, ax1 = plt.subplots(1,2,sharex=True)
ax1.set_xlabel('Písničky')

ax1.plot(views_duration["Stream"], color="green")
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

ax2.plot(views_duration["Views"], color="red")
ax1.set_box_aspect(1)

plt.show()



