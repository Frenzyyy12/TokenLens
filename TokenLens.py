import requests
import os
from colorama import init, Fore, Style

init(autoreset=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii():
    print(Fore.LIGHTMAGENTA_EX + r"""
___________     __                 .____                         
\__    ___/___ |  | __ ____   ____ |    |    ____   ____   ______
  |    | /  _ \|  |/ // __ \ /    \|    |  _/ __ \ /    \ /  ___/
  |    |(  <_> )    <\  ___/|   |  \    |__\  ___/|   |  \\___ \ 
  |____| \____/|__|_ \\___  >___|  /_______ \___  >___|  /____  >
                    \/    \/     \/        \/   \/     \/     \/ 
    """)
    print(Fore.RED + "=" * 58)
    print(Fore.LIGHTMAGENTA_EX + "             DISCORD TOKEN CHECKER TOOL")
    print(Fore.LIGHTMAGENTA_EX + "                Created by: Frenzyyy (@7._zip)")
    print(Fore.RED + "=" * 58)

def print_section(title):
    print(Fore.LIGHTMAGENTA_EX + f"\n[{title}]")

def get_token_info(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    res = requests.get("https://discord.com/api/v9/users/@me", headers=headers)

    if res.status_code == 200:
        user = res.json()
        return {
            "valid": True,
            "username": f"{user.get('username')}#{user.get('discriminator')}",
            "id": user.get('id'),
            "email": user.get('email'),
            "phone": user.get('phone') or 'Not linked',
            "verified": user.get('verified'),
            "mfa_enabled": user.get('mfa_enabled'),
            "locale": user.get('locale'),
            "flags": user.get('flags'),
            "bio": user.get('bio') or 'Empty'
        }
    elif res.status_code == 401:
        return {"valid": False, "error": "Invalid or expired token."}
    else:
        return {"valid": False, "error": f"Error {res.status_code}: {res.text}"}

def save_valid_token(token, info):
    if not os.path.exists("results"):
        os.makedirs("results")
    filepath = os.path.join("results", "Valid_Tokens.txt")
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"Token: {token}\n")
        f.write(f"Username      : {info['username']}\n")
        f.write(f"User ID       : {info['id']}\n")
        f.write(f"Email         : {info['email']}\n")
        f.write(f"Phone         : {info['phone']}\n")
        f.write(f"Email Verified: {info['verified']}\n")
        f.write(f"2FA Enabled   : {'Yes' if info['mfa_enabled'] else 'No'}\n")
        f.write(f"Locale        : {info['locale']}\n")
        f.write(f"Flags         : {info['flags']}\n")
        f.write(f"Bio           : {info['bio']}\n")
        f.write("="*40 + "\n")

def print_account_info(info):
    print_section("ACCOUNT DETAILS")
    print(Fore.LIGHTMAGENTA_EX + f"Username      : {info['username']}")
    print(Fore.LIGHTMAGENTA_EX + f"User ID       : {info['id']}")
    print(Fore.LIGHTMAGENTA_EX + f"Email         : {info['email']}")
    print(Fore.LIGHTMAGENTA_EX + f"Phone         : {info['phone']}")
    print(Fore.LIGHTMAGENTA_EX + f"Email Verified: {info['verified']}")
    print(Fore.LIGHTMAGENTA_EX + f"2FA Enabled   : {'Yes' if info['mfa_enabled'] else 'No'}")
    print(Fore.LIGHTMAGENTA_EX + f"Locale        : {info['locale']}")
    print(Fore.LIGHTMAGENTA_EX + f"Flags         : {info['flags']}")
    print(Fore.LIGHTMAGENTA_EX + f"Bio           : {info['bio']}")

def single_check():
    token = input(Fore.WHITE + "\nEnter your Discord token:\n> ").strip()
    info = get_token_info(token)
    if info["valid"]:
        print_account_info(info)
        save_valid_token(token, info)
        print(Fore.GREEN + "\n[+] Valid token info saved to results/Valid_Tokens.txt")
    else:
        print_section("INVALID TOKEN")
        print(Fore.RED + info.get("error", "Unknown error"))

def bulk_check():
    path = input(Fore.WHITE + "\nEnter the path to your tokens file:\n> ").strip()
    if not os.path.isfile(path):
        print(Fore.RED + "File not found.")
        return

    with open(path, "r", encoding="utf-8") as file:
        tokens = [line.strip() for line in file if line.strip()]

    total = len(tokens)
    valid_count = 0
    print(Fore.LIGHTMAGENTA_EX + f"\nStarting bulk check for {total} tokens...\n")

    for i, token in enumerate(tokens, start=1):
        print(Fore.CYAN + f"Checking token {i}/{total}...")
        info = get_token_info(token)
        if info["valid"]:
            valid_count += 1
            print_account_info(info)
            save_valid_token(token, info)
            print(Fore.GREEN + "[+] Valid token saved!\n")
        else:
            print(Fore.RED + "[!] Invalid token or error.\n")

    print(Fore.CYAN + "=" * 40)
    print(Fore.CYAN + f"Bulk check complete. Valid tokens found: {valid_count}/{total}")
    print(Fore.CYAN + "Valid tokens saved to results/Valid_Tokens.txt")

def main():
    clear()
    print_ascii()
    print(Fore.YELLOW + "\nSelect an option:")
    print(Fore.MAGENTA + "1. Check a single token")
    print(Fore.MAGENTA + "2. Check tokens in bulk from a file")
    choice = input(Fore.YELLOW + "Enter choice (1 or 2): ").strip()

    if choice == "1":
        single_check()
    elif choice == "2":
        bulk_check()
    else:
        print(Fore.RED + "Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
