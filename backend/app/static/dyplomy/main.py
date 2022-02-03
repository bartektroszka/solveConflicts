from datetime import date
import imgkit

def fill_certificate(name, html_path):
    with open(html_path) as inf:
        txt = inf.read()
        txt = txt.replace('user_name', name)
        txt = txt.replace('date', date.today().strftime("%d/%m/%Y"))

        f2 = open('new_file.html', 'w')
        f2.write(txt)
        f2.close()
        imgkit.from_file('new_file.html', 'out.jpg')

fill_certificate('andrzej', './index.html')