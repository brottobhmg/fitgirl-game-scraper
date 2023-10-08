
# Run
- Install the dependencies: ```pip install -r requirements.txt```

- In the same folder of main.py, create a empty folder called ```pages```

- ```python main.py```


# What it do ?

It scrape all games inside [Fitgirl site](https://fitgirl-repacks.site/).

Also save the page of every game visited.

Save all data in ```.txt``` file (use comma as separator) with the structure below:

| title | link | date upload | number of comment | genres | companies | languages | original size | repack size | link1337x | magnet | statsTorrentUrl | repack features |
| ----- | ---- | ----------- | ------------------| ------ | --------- | --------- | ------------- | ----------- | --------- | ------ | --------------- | --------------- |

- ```title```: title of the game
- ```link```: direct link to firtgirl's site
- ```date upload```: when the game was added
- ```number of comment```: number of comment
- ```genres```: gengres of the game
- ```companies```: companies that develop the game
- ```languages```: languages inside the game
- ```original size```: native size of the game
- ```repack size```: size of the game after repack
- ```link1337x```: url to download the game from [1337x](https://1337xto.to/)
- ```magnet```: url to direct download the game throught uTorrent magnet
- ```statsTorrentUrl```: direct url to the stats of the torrent game on [stats torrent site](https://torrent-stats.info/)
- ```repack features```: additional info about repacked game


Now (8 October 2023) it took around 30/40 minuts to navigate throught 77 page and 3800 games.

It's designed to restart from program error at random page, not for update already existing games list.

# Version
Developed with ```Python 3.9.13```
