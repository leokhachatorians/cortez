# cortez

cortez is a simple command line tool which allows you to seamlessly and quickly download your faviorite tracks and playlists off SoundCloud.

**Note make sure you adjust your save directory in your config to properly save your tracks**

# Install
  - Get Python3
  - git clone https://github.com/leokhachatorians/cortez
  - python cortez.py to view **help**
  - pip -r install requirements.txt

# Usage
#### Downloading
##### Single File download
    python cortez.py download https://soundcloud.com/tsyn/tsyn-deep-house-mix-3
##### Multiple Files
    python cortez.py download https://soundcloud.com/tsyn/tsyn-deep-house-mix-3 https://soundcloud.com/harlem_fetty/fetty-wap-jimmy-choo
##### Playlist
    python cortez.py download https://soundcloud.com/hongdotmy/sets/deepmixnation
    
#### Edit Configuration
    python cortez.py config


#### Authenticate
    python cortez.py login

# To Do
* Allow option to enable/disable colors
* Settings for verbose or regular error messages
* Tackle the behemoth that is terminal display of SoundCloud
* Anything and everything else I can think of
