import os
import re
import gzip
import time

def search(gui):
    gui.res.SetLabel('')
    gui.address = gui.choose_text.GetValue()
    gui.search_button.Disable()
    gui.search_button.SetLabel('検索中')
    starttime = time.time()
    word = gui.search_text.GetValue()
    gui.res.AppendText('検索ワード: ' + word + '\n')
    gui.res.AppendText('\n----------------------------------------\n')
    hit = 0
    count = 0
    for fname in get_filelist(gui):
        f = read_file(gui, fname)
        if f is not False:
            gui.SetStatusText(fname + 'を検索中')
            find = False
            while 1:
                line = readtext(f)
                if line is '':
                    break
                if matching(gui, word, line):
                    hit += 1
                    if find == False:
                        gui.res.AppendText('\n' + fname + '\n')
                        find = True
                    gui.res.AppendText(line)
                count += 1
            f.close()
    output(gui, word)
    gui.res.AppendText('\n----------------------------------------\n\n')
    gui.res.AppendText('ヒット件数: ' + str(hit) + ' / ' + str(count) + '\n')
    elapsedtime = round(time.time() - starttime, 3)
    gui.res.AppendText('経過時間: ' + str(elapsedtime) + '[sec]\n')
    gui.search_button.SetLabel('検索')
    gui.search_button.Enable()
    gui.SetStatusText('検索終了')

def readtext(f):
    try:
        return f.readline()
    except:
        return ''

def output(gui, word):
    if gui.check2.GetValue():
        name = re.sub(r'\\|\/|:|,|;|\*|\?|"|<|>|\|', '_', word) + '.txt'
        with open(gui.path + '\\' + name, 'w', encoding='cp932') as f:
            f.write(gui.res.GetValue())

def matching(gui, word, line):
    if gui.check1.GetValue():
        return re.search(word, line, re.IGNORECASE)
    else:
        return re.search(word, line)

def get_filelist(gui):
    ls = os.listdir(gui.address)
    length = len(ls)
    for i in range(length):
        if length <= i: break
        fname = ls[i]
        if re.search('.log$', fname, re.IGNORECASE) and (fname + '.gz') in ls:
            ls.pop(i)
            length -= 1
            i -= 1
    return ls

def read_file(gui, fname):
    if re.search('.log.gz$', fname, re.IGNORECASE):
        return gzip.open(gui.address + '\\' + fname, 'rt', encoding='cp932', errors='ignore')
    elif re.search('(.log|.txt)$', fname, re.IGNORECASE):
        return open(gui.address + '\\' + fname, 'r', encoding='cp932', errors='ignore')
    else:
        return False
