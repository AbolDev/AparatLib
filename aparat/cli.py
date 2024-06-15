import argparse
from aparat import Aparat

def main():
    parser = argparse.ArgumentParser(description='A tool to download videos or playlists from Aparat.')

    parser.add_argument('url', type=str, help='URL or ID of the Aparat video or playlist')
    parser.add_argument('resolution', type=str, nargs='?', default='480p', help='Resolution of the video (default: 480p)')
    parser.add_argument('path', type=str, nargs='?', default=None, help='Path to save the video or playlist (default: current directory)')

    args = parser.parse_args()

    url = args.url
    resolution = args.resolution
    path = args.path

    aparat = Aparat()

    if 'playlist=' in url or url.isdigit():
        if 'playlist=' in url:
            playlist_id = url.split('playlist=')[1]
        else:
            playlist_id = url

        print("Downloading playlist...")
        playlist = aparat.get_playlist(playlist_id)
        print(f"Number of videos in playlist: {len(playlist.videos)}")
        for video in playlist.videos:
            video_path = video.download(resolution=resolution, path=path, show_progress_bar=True)
            print("Video downloaded to:", video_path, end='\n\n')
    else:
        if 'aparat.com/v/' in url:
            video_id = url.split('/')[-1]
        else:
            video_id = url

        print("Downloading video...")
        video = aparat.get_video(video_id)

        video_path = video.download(resolution=resolution, path=path, show_progress_bar=True)
        print("Video downloaded to:", video_path)

if __name__ == '__main__':
    main()
