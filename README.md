# cortez

cortez is a simple command line tool which allows you to seamlessly and quickly download your faviorite tracks and playlists off SoundCloud.

**Note that cortez is still being actively developed with a plethora of features in the pipeline, create an issue for any bugs found or pull requests.**

# Install
  - git clone https://github.com/leokhachatorians/cortez
  - python cortez.py to view **help**
  - pip -r install requirements.txt

# Usage
#### Downloading
##### Single File download
     python cortez.py download https://soundcloud.com/travisscott-2/wonderful-ftthe-weeknd
##### Multiple Files (space delimited)
    python cortez.py download https://soundcloud.com/travisscott-2/wonderful-ftthe-weeknd https://soundcloud.com/harlem_fetty/fetty-wap-jimmy-choo
##### Playlist
    python cortez.py download https://soundcloud.com/hongdotmy/sets/deepmixnation


#### Edit Configuration
- python cortez.py config


#### Authenticate
- python cortez.py login

# To Do
* When items are downloaded, actually direct the files to the proper location as specified by the users config file
* Add support for multi-processing/multi-threading for large batches of downloads
* Allow option to enable/disable colors
* Settings for verbose or regular error messages
* Tackle the behemoth that is terminal display of SoundCloud
