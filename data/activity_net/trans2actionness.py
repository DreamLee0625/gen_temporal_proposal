# coding:utf-8

from __future__ import print_function
import json
import os
import sys
import random
import argparse

"""
gen actionness dataset from activity_net
"""


SEC = 3


def eprint(str):
    print(str, file=sys.stderr)


def main(input_data_file='activity_net.v1-2.min.json', output_data_file='actionness_v1-2', video_dir=None):
    
    output_data_file = output_data_file + "_{}"
    for out_path in [output_data_file.format(x) for x in ['training', 'validation']]:
        if os.path.exists(out_path):
            os.remove(out_path)

    fh = open(input_data_file, 'r')
    dataset = json.load(fh) # key: database, version, taxonomy
    fh.close()
    dataset_data = dataset['database']
    for vid, video_info in dataset_data.iteritems():
        # video_info: key: annotations(list) duration(float) resolution(str) subset(str) url(str)
        
        subset = video_info['subset']
        if subset == 'testing':
            continue
        
        if video_dir:
            video_path = os.path.join(video_dir, vid)
            video_path += '.mp4'
            if not os.path.exists(video_path):
                continue
        else:
            video_path = "no_file"
        
        duration = video_info['duration']
        annotations_list = video_info['annotations']
        annotation = annotations_list[0]
        segment = annotation['segment']
        if segment[1] - segment[0] < SEC:
            continue
        if duration - segment[1] < SEC and segment[0] < SEC:
            continue
        # output_format: vid video_path segment label
        # actionness segment label = 1
        _s = random.uniform(segment[0], segment[1]-SEC)
        with open(output_data_file.format(subset), 'a') as fh:
            fh.write("{}\t{}\t{}\t{}\n".format(vid, video_path, json.dumps([_s, _s+3]), 1))
        # actionness segment label = 0
        if segment[0] > SEC:
            _s = random.uniform(0, segment[0]-3)
            with open(output_data_file.format(subset), 'a') as fh:
                fh.write("{}\t{}\t{}\t{}\n".format(vid, video_path, json.dumps([_s, _s+3]), 0))
        else:
            _s = random.uniform(segment[1], duration-3)
            with open(output_data_file.format(subset), 'a') as fh:
                fh.write("{}\t{}\t{}\t{}\n".format(vid, video_path, json.dumps([_s, _s+3]), 0))
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_data_file", type=str, default="activity_net.v1-2.min.json")
    parser.add_argument("output_data_file", type=str, default="actionness_v1-2")
    args = parser.parse_args()
    main(args.input_data_file, args.output_data_file)