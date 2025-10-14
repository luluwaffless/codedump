@echo off
setlocal enabledelayedexpansion
if "%~1"=="" ( echo Usage: %~nx0 ID OUTPUT & exit /b 1 )
if "%~2"=="" ( echo Usage: %~nx0 ID OUTPUT & exit /b 1 )
set ID=%~1
set OUTPUT=%~2
yt-dlp -f "bv/bestvideo" --remux-video mp4 -o "%OUTPUT%.mp4" https://www.youtube.com/watch?v=%ID%