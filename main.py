# -*- coding: utf-8 -*-
# Copyright (C) 2021 github.com/ItsChasa
#
# This source code has been released under the GNU Affero General Public
# License v3.0. A copy of this license is available at
# https://www.gnu.org/licenses/agpl-3.0.en.html

import os
os.system("cls")
from startup import Setup
clnt = Setup("Backup", "v1.1.3")

# local imports
import console, backup, restore
c = console.prnt(clnt)

# 3rd party imports
import time, sys, base64, os, json
from pathlib import Path
from easygui import fileopenbox


try: cwd = sys.argv[2]
except: account_id = None
else:
    os.chdir(cwd)
    account_id = sys.argv[1]

while True:
    choice = 0
    if account_id == None:
        print(f""" 
{clnt.white}> Main Menu
{clnt.white}1: {clnt.maincol}Backup
{clnt.white}2: {clnt.maincol}Restore
{clnt.white}3: {clnt.maincol}Add to Startup
{clnt.white}4: {clnt.maincol}Help

{clnt.blue}>{clnt.white} Choice ({clnt.maincol}int{clnt.white}) """, end="")
        choice = input()
        try: choice = int(choice)
        except: choice = "wtf are u retarded, do you know what numbers are"
    else:
        choice = 1
    print()
    if choice == 1:
        token_info = False
        if account_id != None:
            c.info(f"Launching Auto-Backup on ID: {clnt.maincol}{account_id}")
            account_id_b64 = base64.b64encode(str(account_id).encode()).decode().replace('=', '')
            import fetch_tokens
            c.info(f"Scanning for tokens...")
            tokens = fetch_tokens.fetch()
            for tkn in tokens:
                if str(tkn[0]).startswith(account_id_b64):
                    token_info = tkn
                    break
            if token_info is False:
                c.fail("Could not find valid token with the provided ID.")
                c.fail("Exiting in 5 seconds...")
                time.sleep(5)
                os._exit(1)
            else:
                c.success(f"Found token with matching ID: {clnt.maincol}{token_info[1]}")
                c.info("Starting Backup...")
        else:
            c.inp(f"Scan for tokens? ({clnt.maincol}y/n{clnt.white}) ", end=clnt.white)
            if input().lower() == "y":
                import fetch_tokens
                c.info(f"Scanning for tokens...")
                tokens = fetch_tokens.fetch()
                if len(tokens) != 0:
                    print()
                    while True:
                        c.info(f"Select which token you want to be auto-backed up:")
                        for tkn in tokens:
                            print(f"{clnt.white}{tokens.index(tkn)}: {clnt.maincol}{tkn[1]}{clnt.white} from {clnt.maincol}{tkn[3]}")
                        print()
                        c.inp(f"Choice {clnt.maincol}(int) """, end=clnt.white)
                        try: tknchoice = int(input())
                        except ValueError: c.fail(f"Invalid Choice")
                        else:
                            try:
                                token_selected = tokens[tknchoice]
                            except:
                                c.fail(f"Invalid Choice")
                            else:
                                break
                    c.success(f"Selected {clnt.maincol}{token_selected[1]}")
                    token_info = token_selected
                else:
                    c.fail(f"No tokens were found on your system.")
            else:
                c.inp("Token: ", end="")
                token_info = [input(), ""]
                
        
        if token_info != False:
            bkup = backup.backup(token_info[0], c, clnt.version)
            if bkup.fatal_error != False:
                c.fail(bkup.fatal_error)
        if len(sys.argv) > 2:
            print()
            c.warn("Closing in 5 seconds...")
            time.sleep(5)
            os._exit(0)


    elif choice == 2:
        c.info(f"1: {clnt.maincol}Restore Everything")
        c.info(f"2: {clnt.maincol}Restore Server Folders")
        c.info(f"See help for more info.")
        print()
        c.inp(f"Choice ({clnt.maincol}int{clnt.white}) ", end="")
        try:
            choice = int(input())
            if choice not in [1,2]: raise Exception
        except:
            c.fail(f"Invalid Choice")
        else:
            restore_server_folders = False
            start_restore = False
            if choice == 1:
                try:
                    c.inp(f"Select backup file in new window.")
                    backupfile = fileopenbox(title="Load .bkup File", default="*.bkup")
                    backup_data = json.loads(open(backupfile, "r", encoding="utf-8").read())
                except Exception as e:
                    c.fail("Encountered Error whilst loading backup file.")
                    c.fail(f"{e}")
                else:
                    c.success(f"Loaded backup data.")
                    start_restore = True
            else:
                restore_server_folders = True
                try:
                    c.inp(f"Select backup file in new window.")
                    backupfile = fileopenbox(title="Load .bkup File", default="*.bkup")
                    backup_data = json.loads(open(backupfile, "r", encoding="utf-8").read())
                except Exception as e:
                    c.fail("Encountered Error whilst loading backup file.")
                    c.fail(f"{e}")
                else:
                    c.success(f"Loaded server folders.")
                    start_restore = True

            if start_restore is True:
                c.inp(f"Scan for tokens? ({clnt.maincol}y/n{clnt.white}) ({clnt.maincol}account to restore on to{clnt.white}) ", end=clnt.white)
                if input().lower() == "y":
                    import fetch_tokens
                    c.info(f"Scanning for tokens...")
                    tokens = fetch_tokens.fetch()
                    if len(tokens) != 0:
                        while True:
                            print()
                            c.info(f"Select which token you want to be auto-backed up:")
                            for tkn in tokens:
                                print(f"{clnt.white}{tokens.index(tkn)}: {clnt.maincol}{tkn[1]}{clnt.white} from {clnt.maincol}{tkn[3]}")
                            print()
                            c.inp(f"Choice {clnt.maincol}(int) """, end=clnt.white)
                            try: tknchoice = int(input())
                            except ValueError: c.fail(f"Invalid Choice")
                            else:
                                try:
                                    token_selected = tokens[tknchoice]
                                except:
                                    c.fail(f"Invalid Choice")
                                else:
                                    break
                        c.success(f"Selected {clnt.maincol}{token_selected[1]}")
                        token_info = token_selected
                    else:
                        c.fail(f"No tokens were found on your system.")
                else:
                    c.inp("Token: ", end="")
                    token_info = [input(), ""]
                
                c.info("A Bot Token is required to fetch Usernames from IDs (used for friends/blocked). You can create one in the Discord Developer Portal.")
                c.inp("Bot Token: ", end="")
                bot_token = input()
                
                rstr = restore.restore(token_info[0], c, restore_server_folders, backup_data, bot_token, clnt.version)
                if rstr.fatal_error != False:
                    c.fail(rstr.fatal_error)


    
    elif choice == 3:
        c.inp(f"By adding to startup, you agree that this program is allowed to search for tokens on your PC.")
        c.inp(f"Your Account Token does not leave this machine and is not sent to our servers. ({clnt.maincol}y/n{clnt.white}) ", end=f"{clnt.white}")
        if input().lower() == "y":
            import fetch_tokens
            c.info(f"Scanning for tokens...")
            tokens = fetch_tokens.fetch()
            if len(tokens) != 0:
                while True:
                    print()
                    c.info(f"Select which token you want to be auto-backed up:")
                    for tkn in tokens:
                        print(f"{clnt.white}{tokens.index(tkn)}: {clnt.maincol}{tkn[1]}{clnt.white} from {clnt.maincol}{tkn[3]}")
                    print()
                    c.inp(f"Choice {clnt.maincol}(int) """, end=clnt.white)
                    try: tknchoice = int(input())
                    except ValueError: c.fail(f"Invalid Choice")
                    else:
                        try:
                            token_selected = tokens[tknchoice]
                        except:
                            c.fail(f"Invalid Choice")
                        else:
                            break

                c.success(f"Selected {clnt.maincol}{token_selected[1]}")
                
                try:
                    if getattr(sys, 'frozen', False): # if pyinstaller
                        tmp_path = ""
                        dirs_list = sys.executable.split("\\")
                        for dir in dirs_list[0:-1]:
                            tmp_path += f"{dir}\\"
                        application_path = tmp_path[0:-1]
                        application_name = dirs_list[-1]
                    else:
                        application_path = os.path.dirname(os.path.abspath(__file__))
                        application_name = Path(__file__).name

                except:
                    c.fail(f"Failed to find Executable.")
                else:
                    roaming = os.getenv('APPDATA')
                    f = open(f"{roaming}\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\backupStartup.vbs", "w")
                    f.write(f'Set oShell = CreateObject ("WScript.Shell")')
                    f.write("\n")
                    f.write(f'oShell.run ("""{application_path}\{application_name}"" {token_selected[2]} ""{application_path}""")')
                    f.close()
                    
                    c.success(f"Added to startup! ({clnt.maincol}{roaming}\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\backupStartup.vbs{clnt.white})")
            else:
                c.fail(f"No tokens were found on your system.")
    
    elif choice == 4:
        c.info('Go to: https://github.com/itschasa/Discord-Backup#how-to-use')
        c.info('For additional help, join the Discord Server: https://discord.gg/MUP5TSEPc4')
        c.info("If it's invalid, go to https://chasa.wtf and click the Discord icon.")
    
    else:
        c.fail(f"Invalid Choice")
    
    time.sleep(1)

