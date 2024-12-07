import streamlit as st
import pandas as pd

st.set_page_config(page_title='Spotify Wrapped', layout="wide")

st.title("Your very own Spotify Wrapped")

#########################
#       data prep
#########################

@st.cache_data
def read_data():
    songs_df = pd.read_json("StreamingHistory0.json")
    songs_df["endTime"] = pd.to_datetime(songs_df["endTime"])
    return songs_df

songs = read_data()

def get_artists(data):
    return sorted(data["artistName"].unique())

artist_select = st.multiselect("Select artist(s) to exclude",
                               get_artists(songs),
                               label_visibility="collapsed",
                               default=None,
                               placeholder="Select artist(s) to exclude...")

songs_filtered = None

if len(artist_select) > 0:
    songs_filtered = songs[songs["artistName"].isin(artist_select) == False]
else:
    songs_filtered = songs.copy()

#########################
# calculations
#########################
artists_excluded = ""

if len(artist_select) > 0:
    artists_excluded = "Excluding: " + ", ".join(artist_select)


total_ms = songs_filtered["msPlayed"].sum()
total_mins = (total_ms/1000)/60
total_hours = total_mins / 60

total_listening_time = ""
if total_mins > 60:
    total_listening_time = f"{total_hours:.2f} hours"
else:
    total_listening_time = f"{total_mins:.2f} minutes"

by_day = songs_filtered.set_index("endTime").resample("D")["msPlayed"].sum()
by_day_sorted = by_day.sort_values(ascending=False)
top_day = by_day_sorted.index[0]
top_day_mins = (by_day_sorted.values[0]/1000)/60

top_day_len = ""
if top_day_mins > 60:
    top_day_len = f'{top_day_mins/60:.1f} hours'
else:
    top_day_len = f'{top_day_mins:.0f} minutes'

top_day_str = f'{top_day.strftime("%A %d %B %Y")} ({top_day_len})'

songs_filtered["song_display_name"] = songs_filtered.apply(lambda row: f'{row["trackName"]} ({row["artistName"]})', axis=1)
song_count = songs_filtered["song_display_name"].value_counts()
top_song = song_count.index[0]
top_song_plays = song_count.values[0]

top_song_str = f'{top_song} ({top_song_plays} plays)'

top_artists = songs_filtered["artistName"].value_counts().reset_index().head()
top_artists.columns = ["Artist", "Plays"]

#########################
# actual widgets go here
#########################
st.text(artists_excluded)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.text("Total listening time")
    st.subheader(total_listening_time)
with col2:
    st.text("Longest listening day")
    st.subheader(top_day_str)
with col3:
    st.text("Top played song")
    st.subheader(top_song_str)
with col4:
    st.text("Top 5 artists")
    st.dataframe(top_artists, hide_index=True)