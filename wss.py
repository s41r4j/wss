#!/usr/bin/python3

#==============================================================================#
#                                                                              #
# [prog]   : WebScrapeSite (wss)                                               #
# [ver]    : 0.0.1                                                             #
# [desc]   : It scrapes websites and gives insight into the data within secs   #
# [usage]  : python3 wss.py -u <url>                                           #
# [dev]    : @s41r4j                                                           #
# [license]: MIT License                                                       #
# [github] : https://github.com/s41r4j/wss                                     #
#                                                                              #
#==============================================================================#

#==============================================================================#
#                                                                              #
#   [!] Legal/Ethical disclaimer:                                              #
#                                                                              #
#   > `wss` is a tool designed to grather information about a target           #
#     which is publicly available.                                             #
#   > It is the end user's responsibility to obey all applicable               #
#     local, state and federal laws.                                           #
#   > Developers assume no liability and are not responsible for any misuse    #
#     or damage caused by this program.                                        #
#                                                                              #
#==============================================================================#


# ----------------------IMPORTS--------------------------
import requests
import argparse
import re
import random
import time
import sys
import os
import whois
import rich
import socket
from rich.table import Table
from bs4 import BeautifulSoup


# ----------------------FUNCTIONS------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="\33[7;49;97m[WebScrapeSite]\033[0m: FAST, EASY & INSIGHTFUL Website Analysis Tool")
    parser.add_argument("-u", "--url", help="url to scrape", required=True)
    parser.add_argument("-o", "--output", help="output filename, default: `<website_name>.csv`")
    parser.add_argument("-f", "--filetype", help="output filetype (`csv`, `json`), default: csv")
    parser.add_argument("-d", "--download", help="download & save html file only", action="store_true")
    parser.add_argument("-a", "--download-all", help="download & save all files (html, css, js, images)", action="store_true")
    parser.add_argument("-b", "--debug", help="debug mode", action="store_true")
    args = parser.parse_args()
    return args

def get_html(url):
    # combinations: windows, mac, linux, android, ios - chrome, firefox, safari, edge, opera
    user_agent = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
                  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
                  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Android 11; Pixel 5 Build/RQ3A.210205.001"]
    try:
        r = requests.get(url, headers={"User-Agent": random.choice(user_agent)})
        r.raise_for_status()
        return r.text
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

def same_domain(url1, url2):
    # extract domain from url using regex (with removal of subdomains)
    domain1 = re.findall(r"(?:https?:\/\/)?(?:[^@\n]+@)?([^:\/\n?]+)", url1)[0]
    domain2 = re.findall(r"(?:https?:\/\/)?(?:[^@\n]+@)?([^:\/\n?]+)", url2)[0]

    # if there are more than 1 "." in domain, remove subdomains
    if domain1.count(".") > 1:
        domain1 = domain1[domain1.find(".")+1:]
    if domain2.count(".") > 1:
        domain2 = domain2[domain2.find(".")+1:]
    
    # check if domains are the same
    if domain1 == domain2:
        return True
    else:
        return False

def space(n):
    if n == 1:
        return '  '
    elif n == 2:
        return ' '
    else:
        return ''

def save_file(data, opfile, url, ftype):
    # file type
    ext = ".csv" # default
    if ftype != None and ftype.lower() == "json":
        ext = ".json"

    # output data
    file = (opfile if (opfile).endswith(ext) else opfile + ext) if opfile else (url.split("//")[1].split("/")[0].replace(".", "_") + ext)


    # open file (create if not exists / overwrite if exists)
    with open(file, "w") as f:
        # csv
        if ext == ".csv":
            # write data headers
            f.write(f"[WebScrapeSite], Data_Insights\n[GITHUB], https://github.com/s41r4j/wss\n[ERROR/ISSUE], https://github.com/s41r4j/wss/issues\n\n\nDOMAIN_NAME, {data['Whois'][0]['domain_name'][1] if type(data['Whois'][0]['domain_name']) == list else data['Whois'][0]['domain_name']}\nORGANIZATION, {data['Whois'][0]['org']}\nREGISTRAR, {data['Whois'][0]['registrar']}\nIP_ADDRESS, {data['IP_Address']}\nCREATION_DATE, {data['Whois'][0]['creation_date'][1] if type(data['Whois'][0]['creation_date']) == list else data['Whois'][0]['creation_date']}\nUPDATED_DATE, {data['Whois'][0]['updated_date'][1] if type(data['Whois'][0]['updated_date']) == list else data['Whois'][0]['updated_date']}\nEXPIRY_DATE, {data['Whois'][0]['expiration_date'][1] if type(data['Whois'][0]['expiration_date']) == list else data['Whois'][0]['expiration_date']}\nHTML_SIZE, {data['HTML_Size']} bytes\n\n\n")

            # write emails
            f.write("EMAILS:\n")
            for email in data["Emails"]:
                f.write(f",{email}\n")

            # write numbers
            f.write("\nNUMBERS:\n")
            for number in data["Numbers"]:
                f.write(f",{number}\n")

            # write images
            f.write("\nIMAGES:\n")
            for image in data["Images"]:
                f.write(f",{image}\n")

            # write files
            f.write("\nSCRIPTS (.js):\n")
            for afile in data["Files"][0]:
                f.write(f",{afile}\n")

            f.write("\nSTYLES (.css):\n")
            for afile in data["Files"][1]:
                f.write(f",{afile}\n")

            # write links
            f.write("\nINTERNAL LINKS:\n")
            for link in data["Links"][0]:
                f.write(f",{link}\n")
            
            f.write("\nEXTERNAL LINKS:\n")
            for link in data["Links"][1]:
                f.write(f",{link}\n")

        # json                
        elif ext == ".json":
            # write data headers
            f.write('[\n  {\n    "[WebScrapeSite]": "Data_Insights",\n    "[GITHUB]": "https://github.com/s41r4j/wss",\n    "[ERROR/ISSUE]": "https://github.com/s41r4j/wss/issues"\n  },\n  {\n    "domain_name": "' + data['Whois'][0]['domain_name'][1] if type(data['Whois'][0]['domain_name']) == list else data['Whois'][0]['domain_name'])
            f.write('",\n    "organization": "' + data['Whois'][0]['org'] + '",\n    "registrar": "' + data['Whois'][0]['registrar'] + '",\n    "ip_address": "' + data['IP_Address'] + '"\n  },\n  {\n    "creation_date": "' + str(data['Whois'][0]['creation_date'][1] if type(data['Whois'][0]['creation_date']) == list else data['Whois'][0]['creation_date']) + '",\n    "updated_date": "' + str(data['Whois'][0]['updated_date'][1] if type(data['Whois'][0]['updated_date']) == list else data['Whois'][0]['updated_date']) + '",\n    "expiration_date": "' + str(data['Whois'][0]['expiration_date'][1] if type(data['Whois'][0]['expiration_date']) == list else data['Whois'][0]['expiration_date']) + '"\n  },\n  {\n    "emails": [\n')
            # write emails
            for i in range(len(data["Emails"])-1):
                f.write(f'        "{data["Emails"][i]}",\n')
            # write numbers
            f.write(f'        "{data["Emails"][-1]}"\n    ],\n    "numbers": [\n')
            for i in range(len(data["Numbers"])-1):
                f.write(f'        "{data["Numbers"][i]}",\n')
            # write images
            f.write(f'        "{data["Numbers"][-1]}"\n    ],\n    "images": [\n')
            for i in range(len(data["Images"])-1):
                f.write(f'        "{data["Images"][i]}",\n')
            # write files
            f.write(f'        "{data["Images"][-1]}"\n    ],\n    "scripts": [\n')
            for i in range(len(data["Files"][0])-1):
                f.write(f'        "{data["Files"][0][i]}",\n')
            f.write(f'        "{data["Files"][0][-1]}"\n   ],\n    "styles": [\n')
            for i in range(len(data["Files"][1])-1):
                f.write(f'        "{data["Files"][1][i]}",\n')
            # write links
            f.write(f'        "{data["Files"][1][-1]}"\n    ],\n    "internal_links": [\n')
            for i in range(len(data["Links"][0])-1):
                f.write(f'        "{data["Links"][0][i]}",\n')
            f.write(f'        "{data["Links"][0][-1]}"\n    ],\n    "external_links": [\n')
            for i in range(len(data["Links"][1])-1):
                f.write(f'        "{data["Links"][1][i]}",\n')
            f.write(f'        "{data["Links"][1][-1]}"\n')
            f.write('    ]\n  }\n]\n')

    return file

def data_parser(html, url):
    # variables
    files = [[], []]   # script/style > src/href  (0: script, 1: style)
    links = [[],[]]   # a > href  (0: internal/same domain, 1: external)
    emails = []  # regex
    images = []  # img > src/href

    # parsing
    soup = BeautifulSoup(html, "html.parser")

    # links
    for link in soup.find_all("a"):
        try:
            if link.get("href").startswith("http"):
                if same_domain(url, link.get("href")):
                    links[0].append(link.get("href"))
                else:
                    links[1].append(link.get("href"))
            else:
                if same_domain(url, url + link.get("href")):
                    links[0].append(url + link.get("href"))
                else:
                    links[1].append(url + link.get("href"))
        except: pass

    # files
    # script
    # get all scripts that have src attribute only
    for script in soup.find_all("script", src=True):
        try:
            if script.get("src").endswith(".js"):
                if script.get("src").startswith("http"):
                    files[0].append(script.get("src"))
                else:
                    files[0].append(url + script.get("src"))
        except: pass
    # style
    # get all styles that have href attribute only
    for style in soup.find_all("link", href=True):
        try:
            if style.get("href").endswith(".css"):
                if style.get("href").startswith("http"):
                    files[1].append(style.get("href"))
                else:
                    files[1].append(url + style.get("href"))
        except: pass

    # images
    for image in soup.find_all("img"):
        try:
            if image.get("src").startswith("http"):
                images.append(image.get("src"))
            else:
                images.append(url + image.get("src"))
        except AttributeError: pass
        except Exception as e:
            if args.debug: print('\33[1;49;91m  [WSS_ERR]: ', e, '\033[0m')
    # remove duplicates, blank spaces and None
    images = list(filter(lambda x: x.strip(),list(filter(None, list(dict.fromkeys(images))))))

    # emails
    # emails = re.findall(r'^[a-zA-Z0-9\_\-]+@[a-zA-Z0-9\_\-]+\.[a-zA-Z0-9]*', html)
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', html)
    emails = list(dict.fromkeys(emails)) # remove duplicates

    # numbers
    # numbers = re.findall(r'^(\+?\d{1,2}\s?)?([\s\-]?\d{1,3}|\(\d{1,4}\))[\s\-]?\d{1,4}[\s\-]?\d{2,4}$', html)
    numbers = re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', html)                                                          
    numbers = list(dict.fromkeys(numbers)) # remove duplicates

    # html file size (bytes)
    html_size = sys.getsizeof(html)

    # whois info
    whois_data = whois.whois(url)
    whois_keys = ['clear', 'copy', 'dayfirst', 'domain', 'fromkeys', 'get', 'items', 'load', 'parse', 'pop', 'popitem', 'setdefault', 'text', 'update', 'values', 'yearfirst']
    whois_detials = [whois_data, whois_keys]

    # get ip address (socket.gaierror)
    ip = socket.gethostbyname(whois_data["domain_name"][1] if type(whois_data["domain_name"]) == list else whois_data["domain_name"])
    
    return {"Links": links, "Files": files, "Images": images, "Emails": emails, "Numbers": numbers, "HTML_Size": html_size, "Whois": whois_detials, "IP_Address": ip}

# need some fixing
def downloader(data, args, html):
    # download all files
    if args.download_all:
        # create folder & file name
        plain_name = args.url.split("//")[1].split("/")[0].replace(".", "_")
        try: os.mkdir(plain_name)
        except FileExistsError: pass

        # download html
        with open(plain_name + "/" + plain_name + ".html", "w") as f:
            try: f.write(html)
            except Exception as e: 
                if args.debug: print('\33[1;49;91m  [WSS_ERR]: ', e, '\033[0m')

        try:
            # download files
            for file in data["Files"][0]:
                try:
                    r = requests.get(file)
                    with open(plain_name + "/" + file.split("/")[-1], "wb") as f:
                        f.write(r.content)
                except Exception as e: 
                    if args.debug: print('\33[1;49;91m  [WSS_ERR]: ', e, '\033[0m')
            for file in data["Files"][1]:
                try:
                    r = requests.get(file)
                    with open(plain_name + "/" + file.split("/")[-1], "wb") as f:
                        f.write(r.content)
                except Exception as e: 
                    if args.debug: print('\33[1;49;91m  [WSS_ERR]: ', e, '\033[0m')
            # download images
            for image in data["Images"]:
                try:
                    r = requests.get(image)
                    with open(plain_name + "/" + image.split("/")[-1], "wb") as f:
                        f.write(r.content)
                except MissingSchema:
                    pass
                except Exception as e: 
                    if args.debug: print('\33[1;49;91m  [WSS_ERR]: ', e, '\033[0m')
        except Exception as e: 
            if args.debug: print('\33[1;49;91m  [WSS_ERR]: ', e, '\033[0m')
    elif args.download:
        # download html
        with open(args.url.split("//")[1].split("/")[0].replace(".", "_") + ".html", "w") as f:
            try: f.write(html)
            except Exception as e: 
                if args.debug: print('\33[1;49;91m  [WSS_ERR]: ', e, '\033[0m')


# ----------------------MAIN-----------------------------
def main():
    args = parse_args()

    # start time
    start_time = time.time()
    
    # check if url starts with http
    if not args.url.startswith("http"):
            args.url = "https://" + args.url

    # get html
    html = get_html(args.url)

    # parsing data
    data = data_parser(html, args.url)

    # download files (if specified)
    downloader(data, args, html)

    # save csv
    op_loc = save_file(data, args.output, args.url, args.filetype) # output location

    # print data insights
    print(f'''    
  \33[1;49;97m/=====================\\
  |\33[7;49;97m[wss] DATA_INSIGHTS  \033[0m\33[1;49;97m|    \33[7;49;31mhttps://github.com/s41r4j/wss\033[0m
  \33[1;49;97m|=====================|
  \33[1;49;97m|\33[1;49;92m[+] \33[1;49;96mlinks            \33[3;49;97m|    \33[1;49;96mdomain_name  : \33[4;49;92m{data["Whois"][0]["domain_name"][1] if type(data["Whois"][0]["domain_name"]) == list else data["Whois"][0]["domain_name"]}\033[0m
  \33[1;49;97m|    \33[1;49;93m-  \33[1;49;96minternal: \33[3;49;91m{str(len(data["Links"][0]))+space(len(str(len(data["Links"][0]))))} \33[1;49;97m|    \33[3;49;96morganization :\33[1;49;92m {data["Whois"][0]["org"]}\033[0m
  \33[1;49;97m|    \33[1;49;93m-  \33[1;49;96mexternal: \33[3;49;91m{str(len(data["Links"][1]))+space(len(str(len(data["Links"][1]))))} \33[1;49;97m|    \33[3;49;96mregistrar    :\33[1;49;92m {data["Whois"][0]["registrar"]}\033[0m
  \33[1;49;97m|---------------------|    \33[3;49;96mip_address   : \33[4;49;92m{data["IP_Address"]}\033[0m
  \33[1;49;97m|\33[1;49;92m[+] \33[1;49;96mfiles            \33[1;49;97m|
  \33[1;49;97m|    \33[1;49;93m-  \33[1;49;96mscripts: \33[3;49;91m{str(len(data["Files"][0]))+space(len(str(len(data["Files"][0]))))}  \33[1;49;97m|    \33[3;49;96mcreation_date:\33[1;49;92m {data["Whois"][0]["creation_date"][1] if type(data["Whois"][0]["creation_date"]) == list else data["Whois"][0]["creation_date"]}\033[0m
  \33[1;49;97m|    \33[1;49;93m-  \33[1;49;96mstyles: \33[3;49;91m{str(len(data["Files"][1]))+space(len(str(len(data["Files"][1]))))}   \33[1;49;97m|    \33[3;49;96mupdated_date :\33[1;49;92m {data["Whois"][0]["updated_date"][1] if type(data["Whois"][0]["updated_date"]) == list else data["Whois"][0]["updated_date"]}\033[0m
  \33[1;49;97m|---------------------|    \33[3;49;96mexpiry_date  :\33[1;49;92m {data["Whois"][0]["expiration_date"][1] if type(data["Whois"][0]["expiration_date"]) == list else data["Whois"][0]["expiration_date"]}\033[0m
  \33[1;49;97m|\33[1;49;92m[+] \33[1;49;96mimages: \33[3;49;91m{str(len(data["Images"]))+space(len(str(len(data["Images"]))))}      \33[1;49;97m|
  \33[1;49;97m|---------------------|    \33[3;49;96mhtml_size    :\33[1;49;92m {data["HTML_Size"]} bytes\033[0m
  \33[1;49;97m|\33[1;49;92m[+] \33[1;49;96memails: \33[3;49;91m{str(len(data["Emails"]))+space(len(str(len(data["Emails"]))))}      \33[1;49;97m|
  \33[1;49;97m|---------------------|    \33[3;49;96moutput_file  : \33[4;49;93m{op_loc}\033[0m
  \33[1;49;97m|\33[1;49;92m[+] \33[1;49;96mnumbers: \33[3;49;91m{str(len(data["Numbers"]))+space(len(str(len(data["Numbers"]))))}     \33[1;49;97m|    \33[3;49;96mscan_time    :\33[1;49;93m {round(time.time() - start_time, 2)}s\033[0m
  \33[1;49;97m|=====================|
  |\33[7;49;97m   [WebScrapeSite]   \033[0m\33[1;49;97m|    \33[7;49;31mall data is saved in `output_file`\033[0m
  \33[1;49;97m\\=====================/
''')


if __name__ == "__main__":
    main()
