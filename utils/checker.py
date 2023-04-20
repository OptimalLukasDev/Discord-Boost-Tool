import requests, json, datetime, ctypes
from colorama import Fore, init
init(convert=True)
import time
class data:
    notused = 0
    used = 0
    total = 0
    locked = 0
    invalid = 0
tokens = open("./tokens.txt", encoding="UTF-8").read().splitlines()
nitro = open('./utils/data/nitro-tokens.txt','a')
def validate_token(e):
    check = requests.get(f"https://discord.com/api/v9/users/@me", headers={'authorization': e})

    if check.status_code == 200:
        profile_name = check.json()["username"]
        profile_discrim = check.json()["discriminator"]
        profile_of_user = f"{profile_name}#{profile_discrim}"
        return profile_of_user

def removedups(file):
    lines_seen = set()
    with open(file, "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if i not in lines_seen:
                f.write(i)
                lines_seen.add(i)
        f.truncate()
for i in tokens:
    token = i
    boost_data = requests.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers={'Authorization': i})
    if boost_data.status_code == 200:
        jsx = json.loads(boost_data.text)
        hm = 0
        if jsx == []:
            print(f'{Fore.RESET}[{Fore.RED}!{Fore.RESET}] No nitro found on this token')
            continue
        nitro.write(token+'\n')
        try:
            for i in jsx:
                if not i['canceled']:
                    hm+=1
                    expr = datetime.datetime.strptime(i['cooldown_ends_at'],'%Y-%m-%dT%H:%M:%S.%f%z')
                    timeTill = expr - datetime.datetime.now(datetime.timezone.utc)
                    timeTill = str(timeTill).split('.')[0]
                    if '-' in timeTill:
                        timeTill = 'No cooldown!'
                    profile_of_user = validate_token(token)
                    print(f"""
{Fore.RESET}[{Fore.GREEN}+{Fore.RESET}] Profile: {profile_of_user}
{Fore.RESET}[{Fore.GREEN}+{Fore.RESET}] Token: {token} 
{Fore.RESET}[{Fore.RED}!{Fore.RESET}] Boost Cooldown: {timeTill}""")
                    with open("./utils/data/used.txt", 'a') as f:
                        f.write(token + '\n')
                    data.used += 0.5; data.total += 0.5 
                    ctypes.windll.kernel32.SetConsoleTitleW(f"Total Checked: {data.total} | Not Used: {data.notused} | Used: {data.used}")
        except TypeError:
            data.notused += 1; data.total += 1
            ctypes.windll.kernel32.SetConsoleTitleW(f"Total Checked: {data.total} | Not Used: {data.notused} | Used: {data.used} | Locked: {data.locked} | Invalid: {data.invalid}")
            profile_of_user2 = validate_token(token)
            print(f"""
{Fore.RESET}[{Fore.GREEN}+{Fore.RESET}] Profile: {profile_of_user2}
{Fore.RESET}[{Fore.GREEN}+{Fore.RESET}] Token: {token}
{Fore.RESET}[{Fore.GREEN}+{Fore.RESET}] BOOSTS UNUSED""")
            with open("./utils/data/not-used.txt", 'a') as f:
                f.write(token + '\n')
    elif boost_data.status_code == 401:
        print(f'{Fore.RESET}[{Fore.RED}!{Fore.RESET}] Invalid token: {token}')
        data.invalid += 1
    elif boost_data.status_code == 403:
        print(f'{Fore.RESET}[{Fore.RED}!{Fore.RESET}] Token has been locked: {token}')
        data.locked += 1
    else:
        print(f'[!] Unknown return code {boost_data.status_code}')
print(f'{Fore.RESET}\n[{Fore.GREEN}+{Fore.RESET}] Finished Checking {Fore.GREEN}[Not Used]: {data.notused} {Fore.RED}[Used]: {data.used} [Locked]: {data.locked} [Invalid]: {data.invalid}')
removedups("./utils/data/used.txt")
time.sleep(864000)
