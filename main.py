from os import walk
from sys import exit
from player import render

video_path = None
media_folder_path = "media/"

def stdin(prompt: str) -> None:
    out = input(f"\n>>> {prompt}: ").strip()
    return out


def stdin_int_bounded(prompt: str, l_bound, u_bound:int) -> int:
    while True:
        try:
            out = input(f"\n>> {prompt} or 'E' to exit: ").strip()
            if out == 'E':
                return -1
            out = int(out)
            if out < l_bound or out > u_bound:
                print(f"\nPlease provide an int between {l_bound} and {u_bound}, or 'E' to exit.\n")
                continue
            return out
        except ValueError as e:
            print(f"\n{out} is not as integer.\n")


def get_media():
    for _, _, files in  walk(media_folder_path):
        return files


def print_media(files = get_media()):
    i = 0
    print("\n--------- MEDIA -----------\n")
    for file in files:
        print(f" {[i]} {file}")
        i += 1
    print("\n---------------------------")
    return len(files)


def set_video_path(path: str|int = 0):
    global video_path
    video_path = path


def select_video():
    global video_path
    files = get_media()
    i = print_media(files)
    
    selection = stdin_int_bounded("Select a video number", 0, i-1)
    if selection == -1:
        video_path = None
    video_path = f"{media_folder_path}{files[selection]}"
    

options = (
    ("Show media in media folder", print_media),
    ("Play file in media folder", select_video),
    ("Use Webcam as input", set_video_path),
    ("Exit", exit)
)

def main():
    global video_path

    while True:
        print("Choose an option:")
        i = 0
        for option in options:
            print(f"[{i}] {option[0]}")
            i +=1
        selection = stdin_int_bounded("Select an option", 0, len(options)-1)
        if selection == -1:
            break
        elif selection > 1:
            options[selection][1](0)
        else:
            options[selection][1]()
        
        if video_path is not None:
            render(video_path)
            video_path = None 


if __name__ == "__main__":
    main()