# gve_devnet_thousandeyes_test_configuration
This project allows test configurations from a CSV file to be uploaded to ThousandEyes and ensures that all additions, changes and deletions are taken into account. Note, the CSV file must have the structure as shown in the test_underlay.csv and test_overlay.csv files.


## Contacts
* Vanessa Rottke

## Solution Components
* ThousandEyes

## Workflow
![/IMAGES/workflow.png](/IMAGES/workflow.png)

## Installation/Configuration

1. Make sure you have [Python 3.8.0](https://www.python.org/downloads/) and [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed.

2. Create a virtual environment for the project in the corresponding folder. ([See instructions here](https://docs.python.org/3/tutorial/venv.html)).

3. Clone this GitHub repository:
  ```git clone [add github link here]```

4. Access the downloaded folder:
  ```cd gve_devnet_thousandeyes_test_configuration```

5. Install all dependencies:
  ```pip3 install -r requirements.txt```

6. Fill in your variables in the **.env** file:
  ```  
    TOKEN="[Add ThousandEyes token]"
    AGENT="[Add ThousandEyes agent]"
    UNDERLAY_CSV_FILE="[Add CSV file for underlays]"
    OVERLAY_CSV_FILE="[Add CSV file for overlays]"
  ```


## Usage
To run the code, use the command:
```
$ python3 main.py
```

# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.