# YT-to-Drumless

A script to strip drums from the music of a Youtube video for recording covers.

## How it Works

1. Downloads Youtube audio
2. Uploads to [music.ai](https://music.ai) and runs my drum-removal workflow
3. Downloads the processed file

## Installation

```
git clone https://github.com/anthonydandrea/YT-to-Drumless.git
cd YT-to-Drumless
docker build -t remove-drums-from-yt .
echo "alias create-backing-track='docker run -v /Your/Output/Path:/Your/Output/Path remove-drums-from-yt --out /Your/Output/Path --uri'" >> ~/.zshrc
source ~/.zshrc
```

## Usage

```
create-backing-track [YouTube URI]
```

This will run the container and store the resulting audio file whever you specified in the installed shell alias.
