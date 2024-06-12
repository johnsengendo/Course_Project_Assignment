#!/usr/bin/env python3
import argparse
import subprocess
import time

def usage():
    print("Usage: ./stream_video.py [-i video] [-o] [-d]")
    print("    -i video = input video filepath, with default value 'Video/big_buck_bunny_720p_5mb.mp4'")
    print("    -o = stream the video once, without looping on it (the default behaviour is an infinite loop)")
    print("    -d = disable the capture of the video stream outgoing packets through tcpdump (the capture is enabled by default, with output file 'shared/server_out.pcap')")

def start_tcpdump():
    tcpdump_command = [
        "tcpdump", "-U", "-s0", "-i", "server-eth0", "src port 1935", "-w", "shared/server_out.pcap"
    ]
    return subprocess.Popen(tcpdump_command)

def stop_tcpdump(tcpdump_process):
    tcpdump_process.terminate()
    tcpdump_process.wait()
    time.sleep(3)

def stream_video(video):
    ffmpeg_command = [
        "ffmpeg", "-re",
        "-i", video, "-c:v", "copy", "-c:a", "aac",
        "-ar", "44100", "-ac", "1", "-t", "8", "-f", "flv", "rtmp://localhost:1935/live/video.flv"
    ]
    subprocess.run(ffmpeg_command)

def main():
    parser = argparse.ArgumentParser(description='Stream video over RTMP')
    parser.add_argument('-i', '--input', type=str, default='Video/big_buck_bunny_720p_5mb.mp4',
                        help="input video filepath, with default value 'Video/big_buck_bunny_720p_5mb.mp4'")
    parser.add_argument('-d', '--disable', action='store_true',
                        help="disable the capture of the video stream outgoing packets through tcpdump")

    args = parser.parse_args()
    video = args.input
    capture_traffic = not args.disable

    tcpdump_process = None
    if capture_traffic:
        tcpdump_process = start_tcpdump()
        time.sleep(2)

    stream_video(video)

    if capture_traffic and tcpdump_process:
        stop_tcpdump(tcpdump_process)

if __name__ == "__main__":
    main()
