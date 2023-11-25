import sys
import vlc
import time
import subprocess

def check_for_stop():
    try:
        with open("/home/roseann/scripts/flag", "r") as f:
            return f.read().strip() == "stop"
    except FileNotFoundError:
        return False

def create_player(vlc_instance, video_path):
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(video_path)
    player.set_media(media)
    player.set_fullscreen(True)
    return player

def turn_off_display():
    """Turn off the display by setting brightness to zero."""
    try:
        subprocess.run('echo 0 | sudo tee /sys/class/backlight/10-0045/brightness', shell=True, check=True)
        print("Display turned off.")
    except subprocess.CalledProcessError:
        print("Error turning off the display.")

def play_video(video_path, loop_option):
    vlc_instance = vlc.Instance()
    player = create_player(vlc_instance, video_path)

    player.video_set_adjust_int(vlc.VideoAdjustOption.Enable, 1)
    brightness_value = 1.0
    player.video_set_adjust_float(vlc.VideoAdjustOption.Brightness, brightness_value)

    player.play()
    time.sleep(1)

    try:
        while True:
            if check_for_stop():
                break  # Exit the loop if stop signal is detected

            if not player.is_playing() and loop_option.lower() == 'loop':
                player.set_media(vlc_instance.media_new(video_path))
                player.play()

            time.sleep(0.1)  # Small delay to avoid too frequent checks
    except KeyboardInterrupt:
        pass
    
    # Stop and clean up
    turn_off_display()
    player.stop()
    player.release()
    print("\nVideo playback stopped.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 play_video.py <path_to_video> <loop/no_loop>")
        sys.exit(1)

    video_path = sys.argv[1]
    loop_option = sys.argv[2]

    play_video(video_path, loop_option)
    

