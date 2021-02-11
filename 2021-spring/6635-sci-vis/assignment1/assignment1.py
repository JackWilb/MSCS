import matplotlib.pyplot as plt
import random
import numpy as np
import pandas as pd
import pickle
import plotly.graph_objects as go

## Q1.1
# Generate data
df1_1 = np.array(range(1,201))

# Create plot
fig1_1,ax1_1 = plt.subplots()

ax1_1.boxplot(df1_1)
ax1_1.set_title("Boxplot for numbers 1-200")
ax1_1.set_xticks([])
ax1_1.set_yticks([0, 50, 100, 150, 200])
ax1_1.set_ylabel('Values')
plt.show()

## Q1.2
# Generate data
df1_2 = np.array([random.random() for x in range(0, 10000)])

# Create plot
fig1_2,ax1_2 = plt.subplots()

ax1_2.hist(df1_2, bins = 20)
ax1_2.set_title("Histogram of 10,000 random numbers (0-1)")
ax1_2.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
ax1_2.set_xlabel('Random Value')
ax1_2.set_ylabel('Occurrences')
plt.show()

## Q1.3
df1_3 = np.array([random.gauss(50, 25) for x in range(0, 100)])

with open('binary_file.pkl', 'wb') as file:
    pickle.dump(df1_3, file)

# Create plot
fig1_3,ax1_3 = plt.subplots()

ax1_3.plot(range(0, 100), df1_3)
ax1_3.set_title("Line plot of 100 random numbers (0-100 Gaussian dist)")
ax1_3.set_xlabel('Index')
ax1_3.set_ylabel('Random Value')
plt.show()


## Q1.4
with open('binary_file.pkl', 'rb') as file:
    df1_4 = pickle.load(file)

# Create plot
fig1_4,ax1_4 = plt.subplots()

ax1_4.hist(df1_4, bins = 7)
ax1_4.set_title("Histogram of 100 random numbers (0-100 Gaussian dist)")
ax1_4.set_xlabel('Random Value')
ax1_4.set_ylabel('Occurrences')
plt.show()



## Q2.1
df2_1 = pd.read_csv('NOAA-Temperatures.csv', skiprows=4)

# Create plot
fig2_1,ax2_1 = plt.subplots()

ax2_1.bar(df2_1['Year'], df2_1['Value'])
ax2_1.set_title("Temperature Difference From Average vs. Year")
ax2_1.set_xlabel('Year')
ax2_1.set_ylabel('Degrees F +/- From Average')
plt.show()

## Q2.2
# df2_2 = pd.read_csv('congress-terms.csv')

# # Number of variables
# N = df2_2.shape[1]

# angles=np.linspace(0, 2 * np.pi, N, endpoint=False)
# angles=np.concatenate((angles,[angles[0]]))

# stats = df2_2.iloc[30]
# stats=np.concatenate((stats,[stats[0]]))

# fig2_2 = plt.figure()
# ax2_2 = fig2_2.add_subplot(111, polar=True)

# ax2_2.plot(angles, stats, 'o-', linewidth=2)
# ax2_2.fill(angles, stats, alpha=0.25)
# ax2_2.set_thetagrids(angles * 180/np.pi, labels)
# ax2_2.set_title('')
# ax2_2.grid(True)
# plot.show()


# Q2.3
df2_3 = pd.read_csv("US_births_2000-2014_SSA.csv")

# Create plot
fig2_3_1,ax2_3_1 = plt.subplots()

ax2_3_1.bar(df2_3["date_of_month"], df2_3["births"])
ax2_3_1.set_title("Histogram of day of month of birth")
ax2_3_1.set_xlabel('Day of Month')
ax2_3_1.set_ylabel('Occurrences')
plt.show()

# Create plot
fig2_3_2,ax2_3_2 = plt.subplots()

ax2_3_2.bar(df2_3["month"], df2_3["births"])
ax2_3_2.set_title("Number of Births per Month")
ax2_3_2.set_xlabel('Month of Year')
ax2_3_2.set_ylabel('Occurrences')
plt.show()

# Q2.4

# Load datasets
df2_4_1 = pd.read_csv("538_fandango_score_comparison.csv")
df2_4_2 = pd.read_csv("538_fight_songs.csv")
df2_4_3 = pd.read_csv("538_weather_check.csv")

# Create plot 2.4.1.1
fig2_4_1_1,ax2_4_1_1 = plt.subplots()

ax2_4_1_1.hist(df2_4_1["IMDB_user_vote_count"], bins=20)
ax2_4_1_1.set_title("Histogram of IMDB User Vote Count")
ax2_4_1_1.set_xlabel('IMDB User Vote Count')
ax2_4_1_1.set_ylabel('Occurrences')
plt.show()

# Create plot 2.4.1.2
fig2_4_1_2,ax2_4_1_2 = plt.subplots()

ax2_4_1_2.scatter(df2_4_1["RottenTomatoes_User"], df2_4_1["RottenTomatoes"])
ax2_4_1_2.set_title("Scatterplot of Rotten Tomatoes Score vs. Rotten Tomatoes User Score")
ax2_4_1_2.set_xlabel('Rotten Tomatoes Score')
ax2_4_1_2.set_ylabel('Rotten Tomatoes User Score')
plt.show()

# Create plot 2.4.2.1
ax2_4_2_1 = df2_4_2[df2_4_2["year"] != "Unknown"]["year"].astype('int32').plot.kde()

ax2_4_2_1.set_title("Density Of Year For Fight Songs")
ax2_4_2_1.set_xlabel('Year')
ax2_4_2_1.set_ylabel('Density')
plt.show()

# Create plot 2.4.2.2
fig2_4_2_2,ax2_4_2_2 = plt.subplots()

ax2_4_2_2.scatter(df2_4_2[df2_4_2["year"] != "Unknown"]["year"].astype('int32'), df2_4_2[df2_4_2["year"] != "Unknown"]['bpm'])
ax2_4_2_2.set_title("Scatterplot of Fight Song BPM vs. Year")
ax2_4_2_2.set_xlabel('Year')
ax2_4_2_2.set_ylabel('BPM')
ax2_4_2_2.set_xticks([1890, 1910, 1930, 1950, 1970])
plt.show()

# Create plot 2.4.3.1
ax2_4_3_1 = df2_4_3["Do you typically check a daily weather report?"].value_counts().plot.bar()

ax2_4_3_1.set_title("Do You Typically Check A Daily Weather Report?")
ax2_4_3_1.set_xlabel("Choices")
ax2_4_3_1.set_ylabel('Occurrences')
plt.show()

# Create plot 2.4.3.2
df2_4_3 = df2_4_3.dropna().groupby(["How much total combined money did all members of your HOUSEHOLD earn last year?", "What is your gender?"]).size()
df2_4_3 = df2_4_3.unstack()
df2_4_3 = df2_4_3.drop('-')
df2_4_3.index = df2_4_3.index.str.replace("to", "-")
df2_4_3 = df2_4_3.reindex([
    "$0 - $9,999",
    "$10,000 - $24,999",
    "$25,000 - $49,999",
    "$50,000 - $74,999",
    "$75,000 - $99,999",
    "$100,000 - $124,999",
    "$125,000 - $149,999",
    "$150,000 - $174,999",
    "$175,000 - $199,999",
    "$200,000 and up",
])
del df2_4_3["-"]
ax2_4_3_2 = df2_4_3.plot.bar()

ax2_4_3_2.set_title("Income Breakdown By Gender")
ax2_4_3_2.set_xlabel("Income")
ax2_4_3_2.set_ylabel('Occurrences')
plt.xticks(rotation=-15, ha="left")
plt.show()


# Q4
import nibabel as nib
t2 = nib.load('T2.nii.gz')
t2.get_fdata()

fig4, ax4 = plt.subplots()
ax4.matshow(t2.dataobj[100, :, :])
plt.savefig("Figure_4.png")
