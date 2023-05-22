# import os
import json
import time
import xml.dom.minidom
import pathlib
# import pynq
import cv2
import sys

DAC_CONTEST = pathlib.Path("/home/root/jupyter_notebooks/fpga_starter_2023/prelim1/")
IMG_DIR = DAC_CONTEST.parent / "images"
RESULT_DIR = DAC_CONTEST / "result"

BATCH_SIZE = 1000

# Return a batch of image dir  when `send` is called
class Team:
    def __init__(self, team_name):
        self._result_path = RESULT_DIR / team_name
        self.team_dir = DAC_CONTEST / team_name

        folder_list = [self.team_dir, self._result_path]
        for folder in folder_list:
            if not folder.is_dir():
                folder.mkdir()

        self.img_list = self.get_image_paths()
        self.current_batch_idx = 0

    def get_image_paths(self):
        names_temp = [f for f in IMG_DIR.iterdir() if f.suffix == ".jpg"]
        names_temp.sort(key=lambda x: int(x.stem))
        return names_temp

    # Returns list of images paths for next batch of images
    def get_next_batch(self):
        start_idx = self.current_batch_idx * BATCH_SIZE
        self.current_batch_idx += 1
        end_idx = self.current_batch_idx * BATCH_SIZE
        return self.img_list[start_idx:end_idx]

    def get_bitstream_path(self):
        return str(self.team_dir / "dac_sdc.bit")

    def reset_batch_count(self):
        self.current_batch_idx = 0

    def load_images_to_memory(self):
        # Read all images in this batch from the SD card.
        # This part doesn't count toward your time/energy usage.
        image_paths = self.get_next_batch()

        rgb_imgs = []
        for image_path in image_paths:
            bgr_img = cv2.imread(str(image_path))
            rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
            rgb_imgs.append((image_path, rgb_img))

        return rgb_imgs

    def run(self, callback, debug=True):
        self.__total_time = 0
        self.__total_energy = 0
        self.__object_data = {}

        # rails = pynq.get_rails()
        # rails_to_monitor = ["1V2", "PSDDR", "INT", "PSINT_LP", "PSINT_FP", "PSPLL"]

        while True:
            # Load images to memory
            rgb_imgs = self.load_images_to_memory()
            if not rgb_imgs:
                break

            if debug:
                print("Batch", self.current_batch_idx, "starting.", len(rgb_imgs), "images.")

            # Run user callback, recording runtime and power usage
            start = time.time()
            # recorder = pynq.DataRecorder(*[rails[r].power for r in rails_to_monitor])
            # with recorder.record(0.05):
            object_locations = callback(rgb_imgs)
            end = time.time()

            if len(object_locations) != len(rgb_imgs):
                raise ValueError(
                    str(len(rgb_imgs))
                    + " images provided, but "
                    + str(len(object_locations))
                    + " object locations returned."
                )
            self.__object_data = self.__object_data | object_locations

            runtime = end - start
            # energy = (
            #     sum([recorder.frame[r + "_power"].mean() for r in rails_to_monitor])
            #     * runtime
            # )

            if debug:
                print(
                    "Batch",
                    self.current_batch_idx,
                    "done. Runtime =",
                    runtime,
                    "seconds.",
                    # "Energy =",
                    # energy,
                    # "J.",
                )

            self.__total_time += runtime
            # self.__total_energy += energy

            # Delete images from memory
            del rgb_imgs[:]
            del rgb_imgs

        print(
            "Done all batches. Total runtime =",
            self.__total_time,
            "seconds. Total energy =",
            self.__total_energy,
            "J.",
        )

        print("Savings results to JSON...")
        self.save_results_json()
        print("JSON results written successfully.")

    def save_results_json(self):
        if len(self.__object_data) != len(self.img_list):
            raise ValueError(f"Result length ({self.__object_data}) not equal to number of images ({self.img_list}).")

        save_data = {
            "runtime" : self.__total_time,
            "objects" : self.__object_data
        }

        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=4)
        return
