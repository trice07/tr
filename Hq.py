import pyscreenshot as ImageGrab
# from pynput.mouse import Listener
import pytesseract
from apiclient import discovery
import webbrowser
import time
from PIL import Image, ImageEnhance, ImageFilter
from threading import Thread
# from urllib import request
# import pprint
if __name__ == '__main__':
    top = None
    left = None
    bottom = None
    right = None
    spell_fix = ''
    def get_num_hits(q):
        service = discovery.build("customsearch", "v1",
        developerKey="AIzaSyCc9NNrv-KYWRFEMqV-Y1KlTJnnsLPtsgA")
        res = service.cse().list(
        q=q,
        cx='006073199718997073925:stkucngizey',
        fields='searchInformation'
        ).execute()
        return res['searchInformation']['totalResults']


    def search(q):
        service = discovery.build("customsearch", "v1",
        developerKey="AIzaSyCc9NNrv-KYWRFEMqV-Y1KlTJnnsLPtsgA")
        res = service.cse().list(
        q=q,
        cx='006073199718997073925:stkucngizey'
        ).execute()
        global spell_fix
        if "spelling" in res:
            spell_fix = res["spelling"]["correctedQuery"]
        try:
            return res['items']
        except KeyError:
            print("FIX QUESTION NO RESULTS")
            return []

    def threaded_function(query):
        webbrowser.open(query)

    def analyze(search_results, a1, a2, a3):
        a1count = 0
        a2count = 0
        a3count = 0
        for s in search_results:
            title = s["title"].lower()
            snippet = s["snippet"].lower()
            tc1 = title.count(a1)
            tc2 = title.count(a2)
            tc3 = title.count(a3)
            sc1 = snippet.count(a1)
            sc2 = snippet.count(a2)
            sc3 = snippet.count(a3)

            a1count += tc1
            a1count += sc1
            a2count += tc2
            a2count += sc2
            a3count += tc3
            a3count += sc3
        scan_option1 = [a1count, a1]
        scan_option2 = [a2count, a2]
        scan_option3 = [a3count, a3]
        scan_ranked = sorted([scan_option1, scan_option2, scan_option3])
        scan_ranked.reverse()
        return scan_ranked

    def print_answers(scan_ranked):
        if not_count < 1:
            print("Best Option: ", scan_ranked[0][1], scan_ranked[0][0])
            print("Option 2 : ", scan_ranked[1][1], scan_ranked[1][0])
            print("Option 3 : ", scan_ranked[2][1], scan_ranked[2][0])
        else:
            print("NOT Question: Best Answer: ", scan_ranked[2][1], scan_ranked[2][0])
            print("Option 2 : ", scan_ranked[1][1], scan_ranked[1][0])
            print("Option 3 : ", scan_ranked[0][1], scan_ranked[0][0])
        return


    # def on_click(x, y, button, pressed):
    #     global top
    #     global left
    #     global right
    #     global bottom
    #     if pressed:
    #         left = x
    #         top = y
    #     else:
    #         bottom = y
    #         right = x
    #     if not pressed:
    #         # Stop listener
    #         return False
    #
    # # Collect events until released
    # with Listener(on_click=on_click) as listener:
    #     listener.join()
    # if top > bottom:
    #     temp = bottom
    #     bottom = top
    #     top = temp
    # if left > right:
    #     temp = left
    #     left = right
    #     right = temp
    left = 67
    top = 265
    # top = 300
    right = 476
    bottom = 651
    total_start = time.time()
    start = time.time()
    im = ImageGrab.grab(bbox=(left, top, right, bottom))  # X1,Y1,X2,Y2
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    # im.show()
    text = pytesseract.image_to_string(im, lang='eng')
    count = 0
    question = ''
    answers = ''
    questionDone = False
    newlineCount = 1
    bad_chars = ["`", "'", '"', "“", '”', "’", '‘']
    for i in text:
        if not questionDone:
            if i == '?':
                question += i
                questionDone = True
            elif i != "\n" and i not in bad_chars:
                question += i
            else:
                question += " "
        else:
            if i == "\n":
                newlineCount += 1
            else:
                newlineCount = 0
            if newlineCount > 1:
                continue
            if i in bad_chars:
                continue
            if i == "&":
                answers += 'and'
                continue
            answers += i.lower()
    answers = answers.split("\n")

    if len(answers) > 3:
        for a in answers:
            if a == '':
                answers.remove(a)

    ans1 = answers[0].lower()
    ans2 = answers[1].lower()
    try:
        ans3 = answers[2].lower()
    except IndexError:
        print("ERROR")
        ans3 = "error"

    ans1 = ans1.replace(" /", "")
    ans2 = ans2.replace(" /", "")
    ans3 = ans3.replace(" /", "")
    not_count = question.count(" NOT ") + question.count(" NEVER ") + question.count(" not ")
    question = question.replace(" NOT ", " ").replace(" NEVER ", " ").replace("wmcn ", "which ").replace("wnlcn ", "which ").replace(" not ", " ").replace("&", "and").replace("5", "s")
    to_search = question + " " + "(" + '"' + ans1 + '"' + " | " + '"' + ans2 + '"' + " | " + '"' + ans3 + '"' + ")"

    chrome = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s"
    query = "http://google.com/search?q=" + to_search
    thread = Thread(target = threaded_function, args = (query.replace(" ", "+").replace('"', "%22"), ))
    thread.start()
    # webbrowser.open(query.replace(" ", "+").replace('"', "%22"))

    results = search(to_search)
    if spell_fix != "":
        print("CHANGE MADE SEE BELOW")
        spell_fix = spell_fix.split("(")
        question = spell_fix[0]
        spell_fix = spell_fix[1].split("\"")
        f1 = spell_fix[1]
        f2 = spell_fix[3]
        f3 = spell_fix[5]
        if ans1 != f1:
            ans1 = f1.lower()
        if ans2 != f2:
            ans2 = f2.lower()
        if ans3 != f3:
            ans3 = f3.lower()
        to_search = question + " " + "(" + '"' + ans1 + '"' + " | " + '"' + ans2 + '"' + " | " + '"' + ans3 + '"' + ")"
        to_search.replace('"', "%22")
        results = search(to_search)
        query = "http://google.com/search?q=" + to_search
        thread2 = Thread(target = threaded_function, args = (query.replace(" ", "+").replace('"', "%22"), ))
        thread2.start()
        thread2.join()
        # webbrowser.open(query.replace(" ", "+").replace('"', "%22"))

    # Part 1
    print(question)
    scan_ranked = analyze(results, ans1, ans2, ans3)
    print_answers(scan_ranked)

    # Part 2
    # res1 = search(question)
    # scan_ranked = analyze(res1, ans1, ans2, ans3)
    # print_answers(scan_ranked)

    total_end = time.time()
    print(total_end-total_start)
    thread.join()
