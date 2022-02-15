# aycd-profile-gen
 This tool is essentially a random, but real, profile generator for AYCD. This will generate profiles using real addresses from https://batch.openaddresses.io/data and optionally card and email info supplied in the csv files

 This is very much a demo, as I made it in a few hours for personal use. `Expect bugs!`

# Questions / Support

DM me on Discord at `Josh#1373` or open a Github issue

# Requirements
1. AYCD (aycd.io)
2. geojson file from https://batch.openaddresses.io/data
3. Discord webhook (https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)

# Running the program
1. See Installation section
2. Run main.exe
3. Follow the prompts

    a. Select the geojson file you want to use by entering the number at the beginning of the line


    b. `Would you like to import your own card info?` -> This will not fill in any card data from `cards.csv`. Card management will be handled by you in AYCD

    c. `Would you like to use a catchall?` -> This will ignore `gmails.csv` and generate profiles with the catchall you're asked for in the next step. 

    d. `Enter your catchall (eg. @josh.com)` -> Simple enough, don't forget the `@`

    e. `How many profiles would you like to make?` -> This only appears if you use a catchall, otherwise it will create as many profiles as you have emails in `emails.csv`

    f. `Enter profile # name` -> AYCD profile name

5. Once the script is finished, it will open the `folder containing the CSV file`  and send the file in a `discord webhook`

6. Import the file into AYCD, select the `CSV/Google Sheet/Form` option

7. The profiles will appear under the `GoogleForm-Import` category
# Installation
1. Download the code as a ZIP and extract it to the folder of your choosing

    ![](https://i.imgur.com/yHV2utr.png)

2. Get geojson data

    a. Download geojson data from Openaddresses.io and store in the `config` folder 
        
        Note: 
        You'll need to create a free account on their website
        You'll also need a program like 7zip installed as native Windows zip functions can't extract .tar.gz archives
    
    b. You can find valid sources from https://github.com/openaddresses/openaddresses/tree/master/sources

    c. An example would be `us/ca/city_of_irvine` ![](https://i.imgur.com/pvOyw0q.png)

3. Edit config files

    a. Rename `sample_emails.csv` to `emails.csv` and enter a list of emails you'd like to use. Leave blank if using a catchall

    b. Rename `sample_cards.csv` to `cards.csv` and enter card info you'd like to use. Leave blank if you'll enter card data from within AYCD

    c. Rename `sample_config.json` to `config.json`. Edit the file and enter a `valid discord webhook URL` (https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks), and a `3 digit area code`
