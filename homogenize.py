#!/usr/bin/env python
# coding: utf-8

# import argparse
# import sys
import os
from collections import defaultdict
from glob import glob

# def parse_args():
#     parser = argparse.ArgumentParser(description='Sort teams by number of cones over number of images')
#     parser.add_argument(
#         'table_file',
#         help='md file containing team data',
#         type=str
#     )
#
#     if len(sys.argv) < 1:
#         print("Error: specify an md file!")
#         parser.print_help()
#         sys.exit(1)
#
#     return parser.parse_known_args()[0]

desired_labels = {
    "big": 0,  # big orange
    "orange": 1,
    "yellow": 2,
    "blue": 3,
    "green": 4,
}
desired_labels_lookup = {v: k for k, v in desired_labels.items()}

remove_images_with_green_cones = True

if __name__ == '__main__':
    # file handling tips: https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    labels_dir = os.path.join(os.getcwd(), 'labels')
    team_names = [el for el in os.listdir(labels_dir) if os.path.isdir(os.path.join(labels_dir, el))]

    team_original_classes = {}
    team_map_classes = {}  # map between old numbers to new (desired) label numbers for each team
    label_counts = {}
    stats_output = ""
    for team_name in team_names:
        label_counts[team_name] = defaultdict(int)
        team_dir = os.path.join(labels_dir, team_name)

        team_classes_file = glob(team_dir + '/*classes.txt')

        if len(team_classes_file) == 0:
            print(f"W: cannot find '*classes.txt' file for '{team_name}', ignoring it...")
            continue

        """ load team classes """
        with open(team_classes_file[0], 'r') as f:
            team_original_classes[team_name] = [cl.strip().lower() for cl in f.readlines()]

        """ map them with the desired ones """
        team_map_classes[team_name] = {}
        for (current_id, class_name) in enumerate(team_original_classes[team_name]):
            for color in desired_labels.keys():
                if color in class_name:
                    team_map_classes[team_name][current_id] = desired_labels[color]
                    break  # 'big' is the first one, so it should not be overwritten by the small orange cone

        """ verify maps """
        print('\n' + team_name)
        for old_id, new_id in team_map_classes[team_name].items():
            print(f"{team_original_classes[team_name][old_id]}\t->\t{desired_labels_lookup[new_id]}")

        # if input("-> is this correct? Should I proceed? [y/N] ").lower() != 'y':
        #     print(f"skipping team '{team_name}'...")
        #     continue

        out_dir = os.path.join(os.getcwd(), 'homogenized_labels', team_name)
        for image_label_file in glob(team_dir + '/*/*.txt'):
            """ load old image label files """
            with open(image_label_file, 'r') as file:
                old_lines = file.readlines()

            """ substitute label IDs """
            new_lines = []
            has_green_cones = False
            for old_line in old_lines:
                if len(old_line.strip()) == 0:
                    continue
                old_label_id = int(old_line[0])
                new_label_id = team_map_classes[team_name].get(old_label_id, -1)

                # skip unknown labels
                if new_label_id == -1:
                    continue

                # check for green cones
                if remove_images_with_green_cones and new_label_id == desired_labels['green']:
                    has_green_cones = True
                    break

                new_lines.append(str(new_label_id) + old_line.strip()[1:] + '\n')

                if not (remove_images_with_green_cones and new_label_id == desired_labels['green']):
                    label_counts[team_name][new_label_id] += 1

            # do not generate the label file if you don't want green cones in your dataset
            if remove_images_with_green_cones and has_green_cones:
                continue

            """ write new label files """
            _, image_basename = os.path.split(image_label_file)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)

            with open(os.path.join(out_dir, image_basename), 'w') as file:
                file.writelines(new_lines)

        """ generate stats for each team """
        stats_output += f"{team_name}:\n"
        for label_id, count in label_counts[team_name].items():
            stats_output += f"- {desired_labels_lookup[label_id]}: {count} cones\n"
        stats_output += "\n"

    """ generate global stats """
    total_stats = defaultdict(int)
    for team_name in team_names:
        for label_id, count in label_counts[team_name].items():
            total_stats[label_id] += count

    stats_output += f"Total count:\n"
    for label_id, count in total_stats.items():
        stats_output += f"- {desired_labels_lookup[label_id]}: {count} cones\n"

    with open(os.path.join(os.getcwd(), 'homogenized_labels', 'stats.txt'), 'w') as file:
        file.writelines(stats_output)
