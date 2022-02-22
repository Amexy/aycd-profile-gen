from ast import Index
from cgi import test
import random, json, csv, pycard, os, subprocess, re
from datetime import datetime
from discord_webhook import DiscordWebhook
from colorama import init, Fore, Back, Style

# Initializes Colorama
init(autoreset=True,convert=True)

def main():
    if not os.path.exists('profiles'):
        os.makedirs('profiles')
    import_valid_options = ['yes','y','no','n']
    geojson_path = get_geojson_path()
    geojson_data = parse_geojson(geojson_path)
    while True:
        print(f"{Fore.YELLOW}Would you like to import your own card info?{Style.RESET_ALL}")
        import_cards_input = input()
        if import_cards_input.lower() not in import_valid_options:
            print(f"{Fore.RED}Please enter a value of Yes or No{Style.RESET_ALL}")
            continue
        else:
            break  
    if import_cards_input.lower() in ['yes','y']:
        import_cards = True
    else:
        import_cards = False

    while True:
        print(f"{Fore.YELLOW}Would you like to use a catchall?{Style.RESET_ALL}")
        catchall_input = input()
        if catchall_input not in import_valid_options:
            print(f"{Fore.RED}Please enter a value of Yes or No{Style.RESET_ALL}")
            continue
        else:
            break  
    cards = []
    if catchall_input.lower() in ['yes','y']:
        use_catchall = True     
        print(f"{Fore.YELLOW}Enter your catchall (eg. @josh.com){Style.RESET_ALL}")       
        catchall = input()
    else:
        use_catchall = False
        emails = get_emails()


    if import_cards and not use_catchall:
        cards = get_cards()
        profile_count = len(cards)
        print(f"{Fore.YELLOW}Using the following emails..{Style.RESET_ALL}")
        for count, email in enumerate(emails):
            print(f"{count+1}. {email[0]}")
    elif not use_catchall:
        profile_count = len(emails)
        print(f"{Fore.YELLOW}Using the following emails..{Style.RESET_ALL}")
        for count, email in enumerate(emails):
            print(f"{count+1}. {email[0]}")
    elif use_catchall and not import_cards:
        print(f"{Fore.YELLOW}How many profiles would you like to make?{Style.RESET_ALL}")
        profile_count = input()
    try:
        if profile_count != len(cards) and cards:
            print(f"{Fore.RED}Card amount doesn't match email/profile count. Exiting..{Style.RESET_ALL}")
            print(f"Email Count: {profile_count}")
            print(f"Card Count: {len(cards)}")
            os._exit(0)
    except UnboundLocalError:
        print('Not filling anything in for card info')
    
    print(f"{Fore.CYAN}Creating {profile_count} profiles{Style.RESET_ALL}")

    header = ['Email Address','Profile Name','Only One Checkout','Name on Card','Card Type','Card Number','Expiration Month','Expiration Year','CVV','Same Billing/Shipping','Shipping Name','Shipping Phone','Shipping Address','Shipping Address 2','Shipping Address 3','Shipping Post Code','Shipping City','Shipping State','Shipping Country','Billing Name','Billing Phone','Billing Address','Billing Address 2','Billing Address 3','Billing Post Code','Billing City','Billing State','Billing Country','Size (Optional)']
    file_name = f"profiles_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    
    
    with open(f"profiles\{file_name}", 'w+', encoding='UTF8', newline='') as r:
        writer = csv.writer(r)
        writer.writerow(header)
        for x in range(0,int(profile_count)):
            with open ('config/used_numbers.txt', 'r+',newline='\n') as number_tracker:
                lines = number_tracker.readlines()
                while True:
                    n = random.randint(1,len(geojson_data))
                    if str(n) not in lines:
                        number_tracker.write(f"{n}" "\n")
                        try:
                            test_street_num = geojson_data[n]['properties']['number']
                            if test_street_num:
                                break
                        except:
                            continue
            print(f"{Fore.YELLOW}Enter billing name #{x+1}{Style.RESET_ALL}")
            name = input()
            if not use_catchall:
                email = emails[x][0]         
            else:
                name_split = name.split()
                try:
                    email = f"{name_split[0]}.{name_split[1]}{catchall}"
                except IndexError:
                    print('------Error when parsing name. Ensure you use a first and last name with a space inbetween------')
                print(f"{Fore.CYAN}Using email: {email}{Style.RESET_ALL}")
            phone_number = phn()
            street_number = geojson_data[n]['properties']['number']
            # some geojson files have a large amount of spaces in the street name
            street_name = re.sub(' +', ' ', geojson_data[n]['properties']['street'])
            city = geojson_data[n]['properties']['city']
            state = geojson_data[n]['properties']['region']
            zip = geojson_data[n]['properties']['postcode']
            street_full = f"{street_number} {street_name}"
            if import_cards:
                card_no = cards[x][0]
                month = int(cards[x][1])
                year = int(cards[x][2])
                if cards[x][3][0] == '0':
                    cvv = '{:04d}'.format(int(cards[x][3]))
                else:
                    cvv = int(cards[x][3])
                card = pycard.Card(
                    number=card_no,
                    month=month,
                    year=year,
                    cvc=cvv
                )
            else:
                card_no = ''
                month = ''
                year = ''
                cvv = ''
                card = pycard.Card(
                        number='111122223333444',
                        month=11,
                        year=1111,
                        cvc=111
                    )

            data = [email,name,'TRUE',name,card.friendly_brand,card_no,month,year,cvv,'TRUE',name,phone_number,street_full,'','',zip,city,state,'United States',name,phone_number,street_full,'','',zip,city,state,'United States','']
            writer.writerow(data)
            print('------PROFILE MADE------')
    print(f"{Fore.CYAN}Finished making {profile_count} profiles{Style.RESET_ALL}")
    current_dir = os.getcwd()
    full_file_path = f"{current_dir}\profiles\{file_name}"
    print(f"Profile file path: {full_file_path}")
    # open folder with file
    subprocess.Popen(f'explorer /select,{full_file_path}')
    try:
        webhook_url = get_webhook()
        webhook = DiscordWebhook(url=webhook_url,username='AYCD Profile Gen', rate_limit_retry=True)
        with open (full_file_path) as f:
            webhook.add_file(file=f.read(), filename=file_name)
        response=webhook.execute()
        print(f"{Fore.CYAN}Successfully sent file to Discord{Style.RESET_ALL}")
    except:
        print(f"{Fore.RED}Failed sending attachment to Discord.\nFile can be found here: {full_file_path}{Style.RESET_ALL}")

    os.system("pause")


def phn():
    with open ('config/config.json') as r:
        r = json.load(r)
        area_code = r["area_code"]
    n = '0000000'
    while '9' in n[3:6] or n[3:6]=='000' or n[6]==n[7]==n[8]==n[9]:
        n = str(random.randint(10**9, 10**10-1))
    return (area_code + n[3:6] + n[6:])

def get_emails():
    rows = []
    with open('config/emails.csv','r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
    return rows

def get_cards():
    rows = []
    with open('config/cards.csv','r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
    return rows

def get_geojson_path():
    file_paths = []
    for root, dirs, files in os.walk(r'config/'):
        for file in files:
            if file.endswith('.geojson'):
                file_paths.append(os.path.join(root, file))
    if file_paths:
        for counter, file_path, in enumerate(file_paths):
            print(f"{counter+1}. {file_path}")
        print(f"{Fore.YELLOW}Found {len(file_paths)} files. Which file would you like to use?{Style.RESET_ALL}")
        choice = int(input())
        try:
            if file_paths[choice-1]:
                geojson_path = file_paths[choice-1]
        except IndexError:
            print(f"Invalid choice. Please restart the program and try again-------")
            os.system("pause")
    return geojson_path

def parse_geojson(path):
    
    print(f"{Fore.CYAN}Parsing geojson file..{Style.RESET_ALL}")
    with open (path) as path_info:
        data = [json.loads(x) for x in path_info]
    return data

def get_webhook():
    with open ('config/config.json') as r:
        r = json.load(r)
        webhook_url = r["webhook_url"]
    return webhook_url

main()