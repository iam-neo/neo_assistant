import webbrowser

def execute(website_name: str):
    """
    Opens a website in the system's default web browser.
    """
    print(f"[*] Attempting to open website: '{website_name}'...")

    # Format the URL properly if it's missing standard elements
    if "." not in website_name:
        # If the user just says "youtube", convert it to "https://www.youtube.com"
        url = f"https://www.{website_name}.com"
    elif not website_name.startswith("http"):
        # If they say "youtube.com", convert it to "https://youtube.com"
        url = f"https://{website_name}"
    else:
        # User provided the full URL
        url = website_name

    try:
        # Open in the default browser instance
        success = webbrowser.open(url)
        if success:
            print(f"[+] Successfully opened {url}")
        else:
            print(f"[-] Browser did not respond to opening {url}.")
    except Exception as e:
        print(f"[!] An error occurred while opening the website: {str(e)}")
