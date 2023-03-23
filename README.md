# Updates for 2023 are still in progress


# DAC 2022 Design Contest

For full contest details, please see the [2022 DAC System Design Contest](https://byuccl.github.io/dac_sdc_2022/) page.

For general questions regarding this contest, please use the Piazza page: piazza.com/dac_2018/winterterm12021/dacsdc2021

## Setup PYNQ on your Ultra96v2 board

  * Download the PYNQ 2.7 Ultra96v2 board image from <http://www.pynq.io/board.html>
  * Follow the instructions to image the SD card at <https://pynq.readthedocs.io/en/latest/getting_started/pynq_image.html>.  
  * Follow the instructions to setup and connect to the board at <https://ultra96-pynq.readthedocs.io/en/latest/getting_started.html>.

## Usage
The get started, users have to run the following command on the Ultra96 board:

```shell
cd /home/xilinx/jupyter_notebooks
git clone https://github.com/jgoeders/dac_sdc_2022.git
```
Remember the user name and password are both `xilinx` for super user.

After the above step is completed successfully, you will see a folder `dac_sdc_2022` under your 
jupyter notebook dashboard.  Open the `sample_team/dac_sdc.ipynb` notebook for directions on where to begin.

## Folder Structure

1. sample_team: This folder contains files for a sample team.  This includes a <teamname>.bit and <teamname>.tcl file that defines the hardware, and a `.ipynb` jupyter notebook, and a `hw` folder that is used to create a Vivado project.  You should create a new folder for your team, where you will keep all of your files.

2. images: All the test images are stored in this folder.  Replace the example images in this directory with the full training set.

3. result: The results contain the output xml produced when execution is complete, and contains the runtime, energy usage, and predicted location of each object in each image.


