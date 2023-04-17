""" This script scores the results of a team's submission."""
from argparse import ArgumentParser
import json
import pathlib
import sys


def main():
    """Main function."""

    parser = ArgumentParser()
    parser.add_argument(
        "teams_folder", help="Path to teams folder (example: './sample_team')", type=pathlib.Path
    )
    parser.add_argument(
        "label_folder",
        help="Path to golden label directory (example: './train/label')",
        type=pathlib.Path,
    )
    parser.add_argument(
        "--multiple_teams",
        help="Score multiple teams (teams_folder contains a directory of multiple teams)",
        action="store_true",
    )
    parser.add_argument("--debug", help="Enable debug mode", action="store_true")
    args = parser.parse_args()

    teams_folders = args.teams_folder
    if not teams_folders.is_dir():
        sys.exit("Error: teams_folder is not a directory")

    if args.multiple_teams:
        teams_folders = [t for t in teams_folders.iterdir() if t.is_dir()]
    else:
        teams_folders = [teams_folders]

    for team in teams_folders:
        score_group(team, args.label_folder, args.debug)
        print("")


def bb_intersection_over_union(box_a, box_b):
    """Compute the intersection over union of two bounding boxes, each specified
    as a list of (x, y)-coordinates."""

    # determine the (x, y)-coordinates of the intersection rectangle
    x_a = max(box_a[0], box_b[0])
    y_a = max(box_a[1], box_b[1])
    x_b = min(box_a[2], box_b[2])
    y_b = min(box_a[3], box_b[3])

    # compute the area of intersection rectangle
    inter_area = max(0, x_b - x_a + 1) * max(0, y_b - y_a + 1)

    # compute the area of both the prediction and ground-truth
    # rectangles
    box_a_area = (box_a[2] - box_a[0] + 1) * (box_a[3] - box_a[1] + 1)
    box_b_area = (box_b[2] - box_b[0] + 1) * (box_b[3] - box_b[1] + 1)

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = inter_area / float(box_a_area + box_b_area - inter_area)

    # return the intersection over union value
    return iou


def get_closest_object(golden_object, candidate_user_objects):
    """Given a list of candidate user objects, find the one that has the largest IOU
    with the golden object and is the same type.
    Golden object has properties x, y, width and height and type.
    The function returns a tuple with the candiate object with the largest IOU, and the IoU value.
    """
    max_iou = -1
    max_iou_object = None
    for user_object in candidate_user_objects:
        if user_object["type"] != golden_object["type"]:
            continue

        iou = bb_intersection_over_union(
            [
                golden_object["x"],
                golden_object["y"],
                golden_object["x"] + golden_object["width"],
                golden_object["y"] + golden_object["height"],
            ],
            [
                user_object["x"],
                user_object["y"],
                user_object["x"] + user_object["width"],
                user_object["y"] + user_object["height"],
            ],
        )

        if iou > max_iou:
            max_iou = iou
            max_iou_object = user_object

    return max_iou_object, max_iou


def score_group(group, label_dir_path, debug):
    """Score a group"""

    result_json = group / "results.json"
    print("Scoring group", group, "results file:", result_json)

    # Parse tree
    if not result_json.is_file():
        sys.exit("Missing results:", result_json)

    result_data = json.load(result_json.open())

    # Print runtime
    runtime = float(result_data["runtime"])
    print("Runtime (s):", round(runtime, 1))

    # Score object detection
    global_true_positives = 0
    global_false_positives = 0
    global_false_negatives = 0

    label_files = sorted(label_dir_path.iterdir())

    # img = root.find('image')
    for img in label_files:
        true_positives = 0
        false_positives = 0
        false_negatives = 0

        filename = img.with_suffix(".jpg").name
        if debug:
            print(filename)

        if filename not in result_data["objects"]:
            print("Skipping", filename, "because it was not in results.json")
            continue

        golden_data = json.load(img.open())
        user_data = result_data["objects"][filename]

        for labelled_object in golden_data:
            if labelled_object["type"] >= 8:
                continue

            if debug:
                print("  Golden object:", labelled_object)

            # Find the closest object in the user's results
            user_object, iou = get_closest_object(labelled_object, user_data)

            # Print closes object and IoU
            if debug:
                print("    Closest object:", user_object)
                if user_object:
                    print("    IoU:", iou)

            if user_object and iou > 0.5:
                if debug:
                    print("    IoU > 0.5, true positive")
                true_positives += 1
                user_data.remove(user_object)
            else:
                false_negatives += 1
                if debug:
                    print("    IoU <= 0.5, false negative")

        # False positives are any objects left in the user's results that have type between 1 and 7
        false_positives = len([o for o in user_data if o["type"] >= 1 and o["type"] <= 7])

        if debug:
            print("  Remaining user objects:")
            for obj in user_data:
                print("    ", obj)

        if debug:
            print("  True positives:", true_positives)
            print("  False positives:", false_positives)
            print("  False negatives:", false_negatives)

        global_true_positives += true_positives
        global_false_positives += false_positives
        global_false_negatives += false_negatives

    if debug:
        print("")
        print("Global true positives:", global_true_positives)
        print("Global false positives:", global_false_positives)
        print("Global false negatives:", global_false_negatives)
        print("")

    # Calculate precision, recall and F1 score
    precision = global_true_positives / (global_true_positives + global_false_positives)
    recall = global_true_positives / (global_true_positives + global_false_negatives)
    f1_score = 2 * (precision * recall) / (precision + recall)

    print("# images:", len(label_files))
    print("Precision:", round(precision, 3))
    print("Recall:", round(recall, 3))
    print("F1 score:", round(f1_score, 3))

    fps = len(label_files) / runtime
    print("fps: ", round(fps, 2))


if __name__ == "__main__":
    main()
