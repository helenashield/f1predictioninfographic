# F1 Preseason Predictions Infographic Maker
***
This project transforms the unreadable google forms results into beautiful infographics for easy comparison
***
## packages
This project requires: 

* argparse
* pandas
* PIL
***
## How to run
1. Download the google sheets responses file "Preseason Predictions! (Responses)" with the .xslx extension and save in the same folder as the f1predictions.py file
2. From the terminal run f1predictions.py 
    * running with no added arguments will create one infographic with all entries for drivers and one for teams. 
    * running with -h will bring up the help menu for possible added arguments
    * running with -n will separate the infographics for each entry

    * running with -s followed by a string of entry names will only use those entries in the infographics. Example: -s "jonah helena" will only use jonah's and helena's entries. This can also be used to set the order of the entries in the infographics
    * running with -g will determine which groups to use for the infographics. The options for this are "teams" "drivers" or "both"
3. Resulting infographics will be saved in the preds folder as .png