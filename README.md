# YT-to-Drumless

```
docker build -t remove-drums-from-yt .
echo "alias create-backing-track='docker run -v /Your/Path:/Your/Path remove-drums-from-yt --out /Your/Path --uri'" >> ~/.zshrc
source ~/.zshrc
```

