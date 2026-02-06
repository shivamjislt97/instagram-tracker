import subprocess
import os
import sys

def download_hd_dp(username):
    print("🚀 Instaloader START")

    cmd = [
        sys.executable,
        "-m",
        "instaloader",
        "--profile-pic-only",
        "--no-posts",
        "--no-videos",
        "--no-metadata-json",
        username
    ]

    subprocess.run(cmd, check=True)

    print("📥 Instaloader DONE")

    folder = username
    if not os.path.exists(folder):
        print("❌ Instaloader folder nahi mila")
        return None

    for file in os.listdir(folder):
        if file.endswith(".jpg"):
            return os.path.join(folder, file)

    print("❌ JPG file nahi mili")
    return None
