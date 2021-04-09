from bs4 import BeautifulSoup
import requests
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import docx
from requests_html import HTMLSession


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"}

def main():
    url = "https://mishka-knizhka.ru/skazki-dlay-detey/page/1"
    #response = requests.get(url, headers=headers)
    #soup = BeautifulSoup(response.text, 'lxml')
    session = HTMLSession()

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    urls = []
    for i in range(1, int(soup.select("div.nav-links:nth-child(2) > a:nth-child(4)")[0].text)+1):
        urls.append(f"https://mishka-knizhka.ru/skazki-dlay-detey/page/{i}")

    for url in urls:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        for url in soup.find_all("div", class_="excerpt-content"):
            url = url.find("a")["href"]
            response = session.get(url, headers=headers)
            response.html.render()
            skazka = str(response.html.find(".entry-content")[0].text).replace("к оглавлению ↑", "\n").split("\n")
            skazka = skazka[2:]
            if "Оглавление:" in skazka:
                skazka = skazka[skazka.index("Оглавление:") + 1:]
            skazka = skazka[:-1]

            skazkaBody = ""
            for i in skazka:
                if "♦" in i: continue
                elif " " in i: i = i.replace(" ", " ")
                #if i in skazka and len(i) > 5 and i[-5:] == "читать": i = i[:-5]
                skazkaBody += i + "\n"


            mydoc = docx.Document()

            style = mydoc.styles['Normal']
            font = style.font
            font.name = 'Arial'
            font.size = Pt(13)
            title = str(response.html.find('.entry-title')[0].text)
            for i in ["?", ":", "~", "#", "%", "*", "&", "*", "{", "}", "\\", "<", ">", "/", "+", "|", '"']:
                title = title.replace(i, " ")
            print(title)
            par = mydoc.add_paragraph(skazkaBody)
            par.alignment =1
            mydoc.save(f"out/{title}.docx")




if __name__ == '__main__':
    main()
    print("END_________________________________")
