#!/bin/bash

curl -X POST http://localhost:7071/api/convert \
  -H "Content-Type: application/json" \
  -d '{
    "vtt_content": "WEBVTT\n\n00:00:00.000 --> 00:00:05.000\nHello, this is a test subtitle\n\n00:00:05.000 --> 00:00:10.000\nSecond line of the subtitle",
    "video_id": "123",
    "video_title": "Test Video",
    "vimeo_url": "https://vimeo.com/1130708144/465cda8ea0?share=copy&fl=sv&fe=ci"
  }'