@echo off
del /s /f /q C:\Windows\Temp
del /s /f /q C:\Windows\Prefetch
del /s /f /q %temp%
ipconfig /flushdns