import streamlit as st
import yt_dlp
import os
from pathlib import Path

def get_available_formats(url):
    ydl_opts = {'quiet': True, 'no_warnings': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info['formats']
        return [(f['format_id'], f'{f.get("height", "audio")}p - {f["ext"]}') for f in formats if f.get('vcodec', 'none') != 'none' or f.get('acodec', 'none') != 'none']

def download_video(url, format_id, progress_bar):
    download_path = str(Path.home() / "Downloads")
    ydl_opts = {
        'format': format_id,
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'progress_hooks': [lambda d: update_progress(d, progress_bar)],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def update_progress(d, progress_bar):
    if d['status'] == 'downloading':
        percent = d['_percent_str']
        progress_bar.progress(float(percent.strip('%')) / 100)
    elif d['status'] == 'finished':
        progress_bar.progress(1.0)

st.title("Video Downloader")

url = st.text_input("Enter the video URL:")

if url:
    try:
        formats = get_available_formats(url)
        format_dict = dict(formats)
        selected_format = st.selectbox("Choose resolution:", [f[1] for f in formats])
        selected_format_id = [k for k, v in format_dict.items() if v == selected_format][0]

        if st.button("Download"):
            progress_bar = st.progress(0)
            download_video(url, selected_format_id, progress_bar)
            st.success("Download completed!")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
else:
    st.info("Please enter a valid URL to start.")
