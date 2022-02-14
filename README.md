# aycd-profile-gen
 This tool is essentially a random, but real, profile generator for AYCD. This will generate profiles using real addresses from https://batch.openaddresses.io/data and optionally card and email info supplied in the csv files

 This is very much a demo, as I made it in a few hours for personal use. `Expect bugs!`

# Questions / Support

DM me on Discord at `Josh#1373` or open a Github issue
# Requirements
1. Python3+ (https://www.python.org/downloads/)
2. AYCD (aycd.io)
3. geojson file from https://batch.openaddresses.io/data
4. Discord webhook (https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)

# Running the script
1. See Installation section
2. Open a `command prompt` or `powershell` window and navigate to the folder containing `main.py` 

    e.g. Run `CD c:\users\amexy\downloads\aycd-profile-gen`
3. Run `python3 main.py`
4. Follow the prompts

    a. `Would you like to import your own card info?` -> This will not fill in any card data from `cards.csv`. Card management will be handled by you in AYCD

    b. `Would you like to use a catchall?` -> This will ignore `gmails.csv` and generate profiles with the catchall you're asked for in the next step. 

    c. `Enter your catchall (eg. @josh.com)` -> Simple enough, don't forget the `@`

    d. `How many profiles would you like to make?` -> This only appears if you use a catchall, otherwise it will create as many profiles as you have emails in `emails.csv`

    e. `Enter profile # name` -> AYCD profile name

5. Once the script is finished, it will open the folder containing the CSV file containing your profile. 

6. Import the file into AYCD, select the `CSV/Google Sheet/Form` option

7. The profiles will appear under the `GoogleForm-Import` category
# Installation
1. Ensure you have python3 or higher installed (I use 3.10)

    https://www.python.org/downloads/

2. Install required python packages by running 

    `python3 -m pip install -r requirements.txt`

3. Get geojson data

    a. Download geojson data from Openaddresses.io and store in the folder containing `main.py`
    
    b.  You can find valid sources  from https://github.com/openaddresses/openaddresses/tree/master/sources

    c. An example would be `us/ca/city_of_irvine` ![](https://i.imgur.com/pvOyw0q.png)

4. Edit config files

    a. Rename `sample_emails.csv` to `emails.csv` and enter a list of emails you'd like to use. Leave blank if using a catchall

    b. Rename `sample_cards.csv` to `cards.csv` and enter card info you'd like to use. Leave blank if you'll enter card data from within AYCD

    c. Rename `sample_config.json` to `config.json` and enter the `filename` you downloaded in step 3a, a `valid discord webhook URL` (https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks), and a `3 digit area code`
