def find_usb_media_dir(custom_usb_videodir):
    import subprocess

    # Command to execute
    command = ["/usr/bin/find", "/media", "-maxdepth", "3", "-mindepth", "2", "-type", "d", "-name", custom_usb_videodir]

    # Execute the command
    result = subprocess.run(command, capture_output=True, text=True)

    # Check the result
    if result.returncode == 0:
        paths = result.stdout.split()
        return paths[-1]
    else:
        print("Error:", result.stderr)
        return False



if __name__ == "__main__":
    dir = find_usb_media_dir('media')
    print(dir)
