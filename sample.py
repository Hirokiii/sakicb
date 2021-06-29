# ステップ1. インポート
# 参考にさせていただいたwebです
# https://search.n2sm.co.jp/cache/?docId=054b38181656458e8b32bab25667ea35&hq=%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB
import PySimpleGUI as sg
import os

# ステップ2. デザインテーマの設定
sg.theme('DarkTeal7')

# ステップ3. ウィンドウの部品とレイアウト
layout = [
    [sg.Text('読み取り対象のファイルとページを指定してください')],
    [sg.Text('ファイル', size=(10, 1)), sg.Input(), sg.FileBrowse('ファイルを選択', key='inputFilePath')],
    [sg.Text('ページ', size=(10, 1)), sg.InputText('', size=(10, 1), key='pages'), sg.Text('複数ページのときは\n3-10 のように指定してください', size=(30, 2))],
    [sg.Text('表の罫線', size=(10, 1)),sg.Combo(('あり', 'なし'), default_value="あり",size=(10, 1), key='lattice')],
    [sg.Button('読み取り', key='read'), sg.Button('csvに保存', key='save')],
    [sg.Output(size=(80,20))]
]

# ステップ4. ウィンドウの生成
window = sg.Window('PDFの表を抜き出すツール', layout)

# ステップ5. イベントループ
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED: #ウィンドウのXボタンを押したときの処理
        break

    if event == 'read': #「読み取り」ボタンが押されたときの処理
        if values['lattice'] == 'あり':
            isLattice = True
        else:
            isLattice = False

        readTableFromPDF(values['inputFilePath'], isLattice, values['pages'])

    if event == 'save': #「csvに保存」ボタンが押されたときの処理
        if values['lattice'] == 'あり':
            isLattice = True
        else:
            isLattice = False

        dfs = readTableFromPDF(values['inputFilePath'], isLattice, values['pages'])

        for index, df in enumerate(dfs):
            basename_without_ext = os.path.splitext(os.path.basename(values['inputFilePath']))[0] # PDFファイル名を抜き出す
            filename = basename_without_ext + "_"  + str(index+1) +".csv"
            df.to_csv(filename, index=None)
            print("csvファイルに保存しました:", filename)

        print("すべてのcsvファイル保存が完了しました")

window.close()