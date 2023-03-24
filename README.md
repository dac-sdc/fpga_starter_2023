# Updates for 2023 are still in progress


# DAC 2023 Design Contest

For full contest details, please see the [2023 DAC System Design Contest](https://dac-sdc.github.io/2023/) page.

For general questions regarding this contest, please use the Slack workspace: <https://join.slack.com/t/dac-sdc/shared_invite/zt-1rrtmgjad-NCYE2leBfOw8xTOp52KR7w>

## Setup PYNQ on your Kria KV260 board

  * Setup the Ubuntu 22.04 image on your Kria KV260 board <https://www.xilinx.com/products/som/kria/kv260-vision-starter-kit/kv260-getting-started/getting-started.html>
    * *Note:* You may need to update the Boot FW in order to boot the Ubuntu 22.04 image.  There are instructions here <https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/1641152513/Kria+K26+SOM#Boot-FW-update-with-xmutil>.  This requires first booting the Ubuntu 20.04 image, installing the Xilinx software tools with in the Ubuntu 20.04 environment, and then using the `xlnx-config --xmutil <cmd>` tool to install the new firmware.  Follow the instructions on that page carefully.
  * Follow the instructions at <https://github.com/Xilinx/Kria-PYNQ> to install the PYNQ system (includes Jupyter notebooks).

## Usage
The get started, users have to run the following command on the Ultra96 board:

```shell
cd /home/root/jupyter_notebooks
git clone https://github.com/dac-sdc/fpga_starter_2023.git
```
Remember the user name and password are both `xilinx`.

After the above step is completed successfully, you will see a folder `fpga_starter_2023` under your 
jupyter notebook dashboard.  Open the `sample_team/dac_sdc.ipynb` notebook for directions on where to begin.

## Folder Structure

1. sample_team: This folder contains files for a sample team.  This includes a <teamname>.bit and <teamname>.tcl file that defines the hardware, and a `.ipynb` jupyter notebook, and a `hw` folder that is used to create a Vivado project.  You should create a new folder for your team, where you will keep all of your files.

2. images: All the test images are stored in this folder.  Replace the example images in this directory with the full training set.

3. result: The results contain the output xml produced when execution is complete, and contains the runtime, energy usage, and predicted location of each object in each image.


