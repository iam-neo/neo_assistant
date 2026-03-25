import webbrowser

def execute(website_name: str):
    """
    Opens a recognized website or domain in the system's default browser.
    """
    print(f"[*] Attempting to open website: '{website_name}'...")

    # Normalize url format (Adds https://www. if missing)
    if "." not in website_name:
        url = f"https://www.{website_name}.com"
    elif not website_name.startswith("http"):
        url = f"https://{website_name}"
    else:
        url = website_name

    try:
        success = webbrowser.open(url)
        if success:
            print(f"[+] Successfully opened {url}")
        else:
            print(f"[-] Could not open {url}. Ensure your default browser is set.")
    except Exception as e:
        print(f"[!] An error occurred while opening the website: {str(e)}")
