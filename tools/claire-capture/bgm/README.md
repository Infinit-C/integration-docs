# 가이드 영상 BGM

`corporate.mp3` — Pixabay "Technology Corporate" (the_mountain, id 186320).
Pixabay 콘텐츠 라이선스: 상업적 사용 무료, 출처 표기 불요, **음원 파일 자체의
재배포는 금지**. 그래서 이 폴더는 gitignore 되어 있고, 완성 영상(mp4)에 믹싱된
형태로만 배포한다.

재다운로드:
https://pixabay.com/music/corporate-technology-corporate-186320/

믹싱(영상 재녹화 후):
```
ffmpeg -y -i out/claire-flow.mp4 -i bgm/corporate.mp3 -map 0:v -map 1:a \
  -c:v copy -c:a aac -b:a 128k \
  -filter:a "volume=0.28,afade=t=in:st=0:d=1.2,afade=t=out:st=<끝-3>:d=2.9" \
  -shortest -movflags +faststart ../../static/video/claire/claire-flow.mp4
```
