from pytube import YouTube

url = input("Enter YouTube video URL: ")

yt = YouTube(url)

stream = (
    yt.streams
    .filter(progressive=True, file_extension="mp4")
    .order_by("resolution")
    .desc()
    .first()
)

stream.download(output_path="downloads")

print("Download complete!")