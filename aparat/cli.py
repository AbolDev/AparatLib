import argparse
from aparat import Aparat

def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Download video from Aparat.')

    # Add arguments
    parser.add_argument('url', type=str, help='URL of the Aparat video')
    parser.add_argument('resolution', type=str, nargs='?', default='480p', help='Resolution of the video (default: 480p)')
    parser.add_argument('path', type=str, nargs='?', default=None, help='Path to save the video (default: current directory)')

    # Parse the arguments
    args = parser.parse_args()

    # Extract arguments
    url = args.url
    resolution = args.resolution
    path = args.path

    # Initialize the Aparat client
    aparat = Aparat()

    # Extract video ID from the URL
    video_id = url.split('/')[-1]

    # Get the video object
    video = aparat.get_video(video_id)

    # Download the video
    video_path = video.download(resolution=resolution, path=path, show_progress_bar=True)
    print("Video path:", video_path)

if __name__ == '__main__':
    main()
