import re
import PySimpleGUI as sg
import sqlite3
con = sqlite3.connect('item.db')
cursor = con.cursor() #savieno ar datubāzi
def profit():
  layout = [[sg.Text('Choose')],
            [sg.Combo(cursor.execute('Select itemid from Item JOIN Weapons on WeaponsID = WeaponsNR JOIN Skins on SkinsID = SkinsNR JOIN Locations on LocationsID = LocationsNR;').fetchall())], #izvēlas itemid no Item
              [sg.Text('Enter price:'),sg.InputText()],# Jaunās cenas ievade
              [sg.Button('Enter'), sg.Button('Exit')]]
  window = sg.Window('Window_input', layout)
  while True:
    event, values = window.read()
    if event == 'Exit' or event == sg.WIN_CLOSED: # Visās vietās kur ir redzams šāds kods nodrošina logu aizvēršanu pēc atbilstošās darbības veikšanas
      break
    elif event == 'Enter': # visos šajos gadījumos nodrošina, ka pēc pogas nospiešanas tiks palaists nosacītais algoritms
      cost_per_item_was = (cursor.execute("Select cost from item WHERE itemid =?",(values[0])).fetchall())[0][0]#cik tagad ir cena elementam tiek ņemts pēc jau ievadītā
      amount = (cursor.execute('Select amount from Item WHERE itemId=?',(values[0])).fetchall())[0][0]# cik tagad ir skaits(pēc ievadītā iepriekš)
      new_price = values[1]
      if float(new_price)<0:# nodrošina, ka nevar ievadīt negatīvu cenu
        sg.popup('Price cannot be negative')
      total_was = cost_per_item_was * amount# aprēķina kopējo summu
      total_is = int(values[1]) * amount#aprēķina pēc jaunās cenas ievades kopēju summu
      sg.popup(f'Cost per item was {cost_per_item_was} it is now {values[1]} the total was {total_was} it is now {total_is}!')# izdrukas logs ar visu info
    window.close()
      
                  
def edit_window():
  data = cursor.execute('Select skin,weapon,location,cost,amount from Item JOIN Weapons on WeaponsID = WeaponsNR JOIN Skins on SkinsID = SkinsNR JOIN Locations on LocationsID = LocationsNR;').fetchall()# izvēlas visu izņemot ItemId, tiks attēlots tabulā
  headings = ['Skins', 'Weapons', 'Locations', 'Cost', 'Amount']# tabulas galotnes
  layout = [[sg.Text('Editing')],
              [sg.Table(values=data, headings=headings, num_rows=len(data), row_height=25, expand_x=True, expand_y=True, key='table')],#tabula
              [sg.Button('Edit'), sg.Button('Exit')]]

  window = sg.Window('Edit Item', layout)

  while True:
    event, values = window.read()
    if event == 'Exit' or event == sg.WIN_CLOSED:
      break
    elif event == 'Edit':
      selected_row = cursor.execute('SELECT * FROM Item').fetchall()[0][0]#no izvēlēta tabulas rindas nolasa itemid
      skin= int(re.findall('[0-9]+',str(cursor.execute('SELECT SkinsID from Skins WHERE Skin =?',(sg.popup_get_text('Enter skin:'),)).fetchall()))[0])#pēc ievadītā atbilstošā logā atbilstošu ID elementu sameklē atbilstošā datubāzē, šajā gadījumā SkinsID tiek meklēts pēc Skins nosaukuma Skin datubāzē
      weapon= int(re.findall('[0-9]+',str(cursor.execute('SELECT WeaponsID from Weapons WHERE Weapon =?',(sg.popup_get_text('Enter Weapon:'),)).fetchall()))[0])
      location= int(re.findall('[0-9]+',str(cursor.execute('SELECT LocationsID from Locations WHERE Location =?',(sg.popup_get_text('Enter Location:'),)).fetchall()))[0])
      cost= sg.popup_get_text('Enter Cost:')# cenas ievade
      amount= sg.popup_get_text('Enter Amount:')# skaita ievade
      if float(amount) < 0 or float(cost) < 0:
        sg.popup('Cannot be negative.')
      else:
        cursor.execute('UPDATE Item SET WeaponsNR=?,SkinsNR=?,LocationsNR=?,Cost=?,Amount=? WHERE ItemID=?',(skin,weapon,location,cost,amount,selected_row))# jaunievadītos datus ievada datubāzē 
        con.commit()
        sg.popup('Edited Sucessfully!')
    window.close()

def input_window():
  layout = [[sg.Text('Enter Info')],
            [sg.Text('Skin'), sg.Combo(cursor.execute("SELECT skin FROM skins;").fetchall())],# izvēlei tiek padoti nosaukumi no datubāzes
            [sg.Text('Weapon'), sg.Combo(cursor.execute("SELECT weapon FROM weapons;").fetchall())],
            [sg.Text('Location'), sg.Combo(cursor.execute("SELECT location FROM locations;").fetchall())],
            [sg.Text('Cost'), sg.InputText()],
            [sg.Text('Amount'), sg.InputText()],
            [sg.Button('Exit'),sg.Button('Enter')]]
  window = sg.Window('Window_input', layout)
  while True:
    event, values = window.read()
    if event == 'Exit' or event == sg.WIN_CLOSED:
      break
    elif event == 'Enter':
      if float(values[3]) < 0 or float(values[4]) < 0:# nodrošina ka nevar ievadīt negatīvas vērtības
        sg.popup('Entered values can not be negative')
      else:
        skin= int(re.findall('[0-9]+',str(cursor.execute('SELECT SkinsID from Skins WHERE Skin =?',(values[0][0],)).fetchall()))[0])
        weapon= int(re.findall('[0-9]+',str(cursor.execute('SELECT WeaponsID from Weapons WHERE Weapon =?',(values[1][0],)).fetchall()))[0])
        location= int(re.findall('[0-9]+',str(cursor.execute('SELECT LocationsID from Locations WHERE Location =?',(values[2][0],)).fetchall()))[0])
        id = len(cursor.execute('SELECT ItemID from item').fetchall())+1# aprēķina id katram elementam, ko grib pievienot
        cursor.execute('INSERT INTO Item VALUES(?,?,?,?,?,?)',(id,skin,weapon,location,values[3],values[4]))# ievieto elementus datubāzē
        con.commit()
        sg.popup('Item added successfully!')
        window.close()
  window.close()

def delete_window():
  data = cursor.execute('Select skin,weapon,location,cost,amount from Item JOIN Weapons on WeaponsID = WeaponsNR JOIN Skins on SkinsID = SkinsNR JOIN Locations on LocationsID = LocationsNR;').fetchall()
  headings = ['Skins', 'Weapons', 'Locations', 'Cost', 'Amount']
  layout = [[sg.Text('Delete an item')],
              [sg.Table(values=data, headings=headings, num_rows=len(data), row_height=25, expand_x=True, expand_y=True, key='table')],
              [sg.Button('Delete'), sg.Button('Exit')]]

  window = sg.Window('Delete Item', layout)

  while True:
    event, values = window.read()
    if event == 'Exit' or event == sg.WIN_CLOSED:
      break
    elif event == 'Delete':
      selected_row = cursor.execute('SELECT * FROM Item').fetchall()[0][0]
      cursor.execute('DELETE FROM Item WHERE ItemID = ?', (selected_row,))#pēc izvēlēta tiek izdzēsta rinda no datubāzes
      con.commit()
      sg.popup('Item deleted successfully!')
      window.close()
      
    window.close()

def refresh(window): #tabulu atjaunināšana
  data = cursor.execute('Select skin,weapon,location,cost,amount from Item JOIN Weapons on WeaponsID = WeaponsNR JOIN Skins on SkinsID = SkinsNR JOIN Locations on LocationsID = LocationsNR;').fetchall()
  window['table'].update(values=data, num_rows=len(data))#nodrošona tabulu atjauninājumu
  
def main():
  data = cursor.execute('Select skin,weapon,location,cost,amount from Item JOIN Weapons on WeaponsID = WeaponsNR JOIN Skins on SkinsID = SkinsNR JOIN Locations on LocationsID = LocationsNR;').fetchall()
  headings = ['Skin','Weapon','Location','Cost','Amount']
  layout = [[sg.Text('CS:GO item manager')],
            [sg.Table(values=data,headings=headings,key = 'table',num_rows = len(cursor.execute('SELECT ItemID from item').fetchall()),row_height=25,expand_x=True,expand_y=True)],
            [sg.Button('Input Window'),sg.Button('Delete Window'),sg.Button('Edit Window'), sg.Button('Calculate')],
            [sg.Button('Exit'),sg.Button('Logout')]]
  window = sg.Window('Main window', layout)
  while True: 
    event, values = window.read()
    if event == 'Exit' or event == sg.WIN_CLOSED:
      break
    
    elif event == 'Input Window':
      input_window()
      refresh(window)# izsaukta tabulu atjaunošana uz mainīgo window
      con.commit()
    elif event == 'Delete Window':
      delete_window()
      refresh(window)
      con.commit()
    elif event == 'Edit Window':
      edit_window()
      refresh(window)
      con.commit()
    elif event == 'Logout':
      window.close()
      login()
    elif event == 'Calculate':
      profit()
      refresh(window)
      con.commit()
  window.close()

def login(): # nodrošina pierakstīšanos
  layout = [
    [sg.Text('Username'), sg.Input(key='username')],# lietotājvārds
    [sg.Text('Password'), sg.Input(key='password', password_char='*')],# parolem, kuru ievadod parādās * simbols ievadītā simbola vietā
    [sg.Button('Login'),sg.Button('Register'), sg.Button('Exit')]
  ]
  login_window = sg.Window('Login', layout)

  while True:
    event, values = login_window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
      break

    elif event == 'Login':
      username = values['username']# izsaucot mainīgu atslēgu pārliecinās,ka datubāzē ir pastāvoš lietotājvārds
      password = values['password']# izsaucot mainīgu atslēgu pārliecinās,ka datubāzē ir pastāvoša parole
      if not username or not password:# nodrošina to, ka netiks apstiprināta tukša lauka ievada kā pareizi pierakstīšanās dati
        sg.popup('Please enter both username and password.')
        continue
      cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
      result = cursor.fetchone()
      if result:
        sg.popup('Login successful!')
        main()
        login_window.close()
      else:
        sg.popup('Unsuccessful Login')
    elif event == 'Register':   #nodrošina reģistrāciju  
      cursor.execute('CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT)')# izveido ja nav izveidota datubāzi kurā veikt reģistrāciju
      layout = [[sg.Text('Username:'), sg.Input(key='username')],
      [sg.Text('Password:'), sg.Input(key='password', password_char='*')],
      [sg.Button('Register'), sg.Button('Exit')]]
      register_window = sg.Window('Registration', layout)# izveido reģistrācijas logu
      while True:
        event, values = register_window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
          break
        elif event == 'Register':
          username = values['username']
          password = values['password']
          try:
            cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))# ievieto datubāzē piereģistrētās vērtības
            con.commit()
            sg.popup('Registration Successful!')
            register_window.close()# aizvērs register logu
            login_window.un_hide()# atklusēs login logu
          except sqlite3.IntegrityError:# ja jau ir piereģistrētās tādas pašas vērtības
            sg.popup('Username already exists!')
            continue


      register_window.close()
  login_window.close()

login()# izsauc login() funckiju, kas šajā gadījumā ir programmas logu atvēršanas sākums