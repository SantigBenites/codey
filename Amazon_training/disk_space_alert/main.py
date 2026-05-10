import logging,sys,argparse
import subprocess, time
import shutil

logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(message)s")




def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("threshhold",type=int, required=True)
    ap.add_argument("mount_point",nargs="+")

    args = ap.parse_args()
    exit_code = 0
    for mp in args.mount_points:

        try:
            usage = shutil.disk_usage(mp)
        except FileNotFoundError:
            logging.error(f"Mount point {mp} not found")
            exit_code = 1
            continue
        
        usage_percentage = usage.used / usage.total * 100
        if usage_percentage > args.threshold:
            logging.warning(f"Mount point {mp} is at {usage_percentage:.1f}% usage, surpassing {args.threshold}%")
    return exit_code
            

if __name__=="__main__":

    sys.exit(main())