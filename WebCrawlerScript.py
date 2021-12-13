import requests, time, lxml, os
from bs4 import BeautifulSoup
from datetime import datetime
import winsound

URL = "https://www.brack.ch/it-multimedia/pc-komponenten/grafikkarten/pc-grafikkarten"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"
}
LOG_FOLDER = "./sessionlogs/"
NEXT_CHECK = 30 # In seconds

storeOptionsList = []
firstOptionList = []


def getDateNowFormatted(format = "%Y-%m-%d %H:%M:%S"):
    return datetime.now().strftime(format)

file = open(LOG_FOLDER + "log " + getDateNowFormatted("%Y-%m-%d %H-%M-%S") + ".txt", "w+")

def main():
    if not os.path.exists(LOG_FOLDER):
        os.mkdir(LOG_FOLDER)
    scrapHTMLWebPage()

def scrapHTMLWebPage():
    global storeOptionsList, firstOptionList
    while True:
        sessionResult = ''
        printLog("Starting New Session Request")
        session = requests.session()
        for _ in range(10):
            f = session.get(URL, headers = HEADERS)

        printLog("Site responded with " + str(f.status_code) + (" OK" if f.status_code == 200 else ""))

        if f.status_code == 200:
            soup = BeautifulSoup(f.content, 'lxml')
            options = soup.find_all('a', {
                'class': 'product__imageTitleLink product__imageTitleLink--title'
            })

            # first initialization
            if not storeOptionsList:
                storeOptionsList = initStoreList(options)
                sessionResult = "First initialization"
                printLog("Store page initialized! Will check in " + str(NEXT_CHECK) + " seconds! Store options amount are " + str(len(storeOptionsList)) + ".")
            else:
                optionsStringList = []
                # Check if anything new appeared
                for option in options:
                    optionName = option.string.strip()
                    optionsStringList.append(optionName)
                    if not optionName in storeOptionsList:
                        sessionResult = 'New Items'
                        printLog("NEW ENTRY! \"" + optionName + "\" link: " "https://brack.ch" + option['href'])
                        storeOptionsList.append(optionName)
                        winsound.PlaySound('sound.wav', winsound.SND_FILENAME)
                # Check if any was removed
                i = 0
                while i < len(storeOptionsList):
                    if not storeOptionsList[i] in optionsStringList:
                        printLog("AN ENTRY HAS BEEN REMOVED FOR \"" + storeOptionsList[i] + "\"")
                        if sessionResult != '': sessionResult += ' && '
                        sessionResult = 'ITEMS WERE REMOVED'
                        storeOptionsList.remove(storeOptionsList[i])
                        winsound.PlaySound('sound.wav', winsound.SND_FILENAME)
                        i -= 1
                    i += 1

            printLog("Final result of this session: " + (sessionResult if sessionResult else "All clear! Nothing changed on sight") + ".")
        else:
            printLog("Site failed to respond retrying...")
        time.sleep(NEXT_CHECK)
           

def initStoreList(options):
    printLog("Initializing the list!")
    for option in options:
        optionName = option.string.strip()
        printLog("Adding \"" + optionName + "\" link: " "https://brack.ch" + option['href'])
        firstOptionList.append(optionName)
    return firstOptionList

def printLog(s):
    s = "[" + getDateNowFormatted() + "] " + s
    print(s)
    file.write(s + "\n")
    file.flush()

main()

