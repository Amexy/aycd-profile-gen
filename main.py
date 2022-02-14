import random, json, csv, pycard, os, subprocess
from datetime import datetime

def main():
    if not os.path.exists('profiles'):
        os.makedirs('profiles')
        print('------Created profiles folder------')
    import_valid_options = ['yes','y','no','n']
    
    while True:
        import_cards_input = input('Would you like to import your own card info?: ')
        if import_cards_input not in import_valid_options:
            print("Please enter a value of Yes or No.")
            continue
        else:
            break  
    if import_cards_input.lower() in ['yes','y']:
        import_cards = True
    else:
        import_cards = False

    while True:
        catchall_input = input('Would you like to use a catchall?: ')
        if catchall_input not in import_valid_options:
            print("Please enter a value of Yes or No.")
            continue
        else:
            break  
    cards = []
    if catchall_input.lower() in ['yes','y']:
        use_catchall = True            
        catchall = input('Enter your catchall (eg. @josh.com): ')
    else:
        use_catchall = False
        emails = get_emails()


    if import_cards:
        cards = get_cards()
        profile_count = len(cards)
    elif not use_catchall:
        profile_count = len(emails)
    elif use_catchall and not import_cards:
        profile_count = input('How many profiles would you like to make?: ')  
    
    try:
        if profile_count != len(cards) and cards:
            print("Card amount doesn't match email/profile count. Exiting..")
            print(f"Email Count: {profile_count}")
            print(f"Card Count: {len(cards)}")
            os._exit(0)
    except UnboundLocalError:
        print('Not filling anything in for card info')
    
    print(f"------Creating {profile_count} profiles------")

    header = ['Email Address','Profile Name','Only One Checkout','Name on Card','Card Type','Card Number','Expiration Month','Expiration Year','CVV','Same Billing/Shipping','Shipping Name','Shipping Phone','Shipping Address','Shipping Address 2','Shipping Address 3','Shipping Post Code','Shipping City','Shipping State','Shipping Country','Billing Name','Billing Phone','Billing Address','Billing Address 2','Billing Address 3','Billing Post Code','Billing City','Billing State','Billing Country','Size (Optional)']
    file_name = f"profiles_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    with open(f"profiles\{file_name}", 'w+', encoding='UTF8', newline='') as r:
        writer = csv.writer(r)
        writer.writerow(header)

        for x in range(0,int(profile_count)):
            with open ('used_numbers.txt', 'r+',newline='\n') as number_tracker:
                lines = number_tracker.readlines()
                n = random.randint(1,500000)
                valid = False
                while not valid:
                    if str(n) not in lines:
                        number_tracker.write(f"{n}" "\n")
                        valid = True
            name = input(f"Enter profile #{x+1} name: ")
            if not use_catchall:
                email = emails[x][0]         
            else:
                name_split = name.split()
                try:
                    email = f"{name_split[0]}.{name_split[1]}{catchall}"
                except IndexError:
                    print('------Error when parsing name. Ensure you use a first and last name with a space inbetween------')
                print(f"Using email: ------{email}------")
            phone_number = phn()
            geojson_path = get_config()
            with open(geojson_path) as f:
                data = json.load(f)
                street_number = data[n]['properties']['number']
                street_name = data[n]['properties']['street']
                city = data[n]['properties']['city']
                state = data[n]['properties']['region']
                zip = data[n]['properties']['postcode']
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
    print(f"------Finished making {profile_count} profiles------")
    current_dir = os.getcwd()
    full_file_path = f"{current_dir}\profiles\{file_name}"
    print(f"------Profile file path: {full_file_path}------")
    # open folder with file
    subprocess.Popen(f'explorer /select,{full_file_path}')

def phn():
    area_code = '314'
    n = '0000000'
    while '9' in n[3:6] or n[3:6]=='000' or n[6]==n[7]==n[8]==n[9]:
        n = str(random.randint(10**9, 10**10-1))
    return (area_code + n[3:6] + n[6:])

def get_emails():
    rows = []
    with open('emails.csv','r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
    return rows

def get_cards():
    rows = []
    with open('cards.csv','r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
    return rows

def get_config():
    with open ('config.json') as r:
        r = json.load(r)
        geojson_path = r["geojson_path"]
    return geojson_path

main()