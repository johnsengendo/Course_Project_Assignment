#!/usr/bin/env python3
import argparse
import subprocess
import time

def usage():
    print("Usage: ./get_streaming.py [-o stream_output_filename] [-d]")
    print("    -o stream_output_filename = name of the (.flv) output file without extension (the default value is 'stream_output')")
    print("    -d = disable the capture of the video stream incoming packets through tcpdump (the capture is enabled by default, with output file 'shared/client_out.pcap')")

def start_tcpdump():
    tcpdump_command = [
        "tcpdump", "-U", "-s0", "-i", "client-eth0", "src port 1935", "-w", "shared/client_out.pcap"
    ]
    return subprocess.Popen(tcpdump_command)

def stop_tcpdump(tcpdump_process):
    tcpdump_process.terminate()
    tcpdump_process.wait()
    time.sleep(3)

def get_stream(out_file):
    start_time = time.time()
    ffmpeg_command = [
        "ffmpeg", "-i", "rtmp://10.0.0.1:1935/live/video.flv",
        "-probesize", "80000", "-analyzeduration", "15",
        "-c:a", "copy", "-c:v", "copy", out_file
    ]
    subprocess.run(ffmpeg_command)
    run_time = time.time() - start_time
    return run_time

def main():
    parser = argparse.ArgumentParser(description='Get video streaming')
    parser.add_argument('-o', '--output', type=str, default='stream_output',
                        help="name of the (.flv) output file without extension (default is 'stream_output')")
    parser.add_argument('-d', '--disable', action='store_true',
                        help="disable the capture of the video stream incoming packets through tcpdump")

    args = parser.parse_args()
    out_file = f"{args.output}.flv"
    capture_traffic = not args.disable

    tcpdump_process = None
    if capture_traffic:
        tcpdump_process = start_tcpdump()
        time.sleep(2)

    run_time = get_stream(out_file)

    if capture_traffic and tcpdump_process:
        stop_tcpdump(tcpdump_process)

    print("\nThe stream acquisition run time is {:.0f}s".format(run_time))

if __name__ == "__main__":
    main()
