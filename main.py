import random
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
import csv
from PIL import Image, ImageTk
from tkinter import font, filedialog
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap import Style, Toplevel
from ttkbootstrap.dialogs import Querybox
import datetime
from ttkbootstrap.dialogs import Messagebox
import matplotlib.pyplot as plt

try:
    with open("TXT_files/geometry.txt", "r") as file:
        geometry = file.read()
except:
    with open("TXT_files/geometry.txt", "w") as file:
        file.write("600x400")
        geometry = "600x400"

try:
    with open("JSON_files/categories.json", "r") as json_file:
        a = json.load(json_file)
except:
    with open("JSON_files/categories.json", "w") as json_file:
        json.dump([], json_file)

try:
    with open("JSON_files/spending.json", "r") as json_file:
        a = json.load(json_file)
except:
    with open("JSON_files/spending.json", "w") as json_file:
        json.dump([], json_file)

root = ttk.Window(themename="darkly", title="Expanse Tracker", minsize=(900, 700), iconphoto="images/appIcon.png")
root.geometry(geometry)

notebook = ttk.Notebook()
notebook.pack(expand=True, fill=BOTH)

mainPage = ttk.Frame(notebook)
addPage = ttk.Frame(notebook)
categoriesPage = ttk.Frame(notebook)

mainPage.pack(fill=BOTH, expand=True)
addPage.pack(fill=BOTH, expand=True)
categoriesPage.pack(fill=BOTH, expand=True)

notebook.add(mainPage, text="Расходы")
notebook.add(addPage, text="Добавление расходов")
notebook.add(categoriesPage, text="Категории")

addObj = {
    "price": 0,
    "category": "",
    "date": datetime.date.today(),
    "comment": ""
}


def submit():
    if int(addPrice.get()) == 0 or addPrice.get() == "":
        alertText.configure(background="#F8D7DA", font=(font, 15), width=28, foreground="#721C30")
        alertText["text"] = "Неверно указанная стоимость"

        alertBox.pack(anchor=SE, padx=7, expand=1, pady=15)
        alertText.pack(ipady=15)

        root.after(3000, hideAlerts)

        lineUnderEntry.configure(bootstyle=DANGER)

        return 0

    if addObj["category"] == "":
        alertText.configure(background="#F8D7DA", font=(font, 15), width=28, foreground="#721C30")
        alertText["text"] = "Выберите категорию"

        alertBox.pack(anchor=SE, padx=7, expand=1, pady=15)
        alertText.pack(ipady=15)

        root.after(3000, hideAlerts)

        return 0

    addObj["date"] = str(addObj["date"])
    addObj["price"] = int(addPrice.get())
    addObj["comment"] = commentEntry.get(1.0, "end").replace("\n", "")

    try:
        with open("JSON_files/spending.json", "r") as json_file:
            if json_file.read() == "":
                with open("JSON_files/spending.json", "w") as json_file:
                    json_file.write("[]")
    except:
        with open("JSON_files/spending.json", "w") as json_file:
            json_file.write("[]")

    with open("JSON_files/spending.json", "r") as json_file:
        spending = json.load(json_file)

    spending.append(addObj)

    with open("JSON_files/spending.json", "w") as json_file:
        json.dump(spending, json_file)

    alertText.configure(background="#D4EDDA", font=(font, 15), width=28, foreground="#155724")
    alertText["text"] = "Трата успешно сохранена"

    alertBox.pack(anchor=SE, padx=7, expand=1, pady=15)
    alertText.pack(ipady=15)

    root.after(3000, hideAlerts)

    addObj["category"] = ""
    addObj["date"] = datetime.date.today()
    addObj["price"] = 0
    addObj["comment"] = ""

    commentEntry.delete(1.0, END)
    addPrice.delete(0, "end")
    entryNotFocused("")
    for i in categoryButtonsAddPage:
        i.configure(bootstyle=[LIGHT, OUTLINE])
    dateButtonToday.configure(style="My.TFrame")
    dateLabelToday.configure(style="My.TLabel", foreground="#ffffff")
    textDateLabelToday.configure(style="My.TLabel", foreground="#dddddd")
    onDateNotHover(dateButtonYesterday, textDateLabelYesterday, dateLabelYesterday)
    onDateNotHover(dateButtonSelect, textDateLabelSelect, dateLabelSelect)

    datePick("", "week", False)


def categoriesButtonAlignForAddPage(event):
    categoriesButtonAlignForCategoryPage()

    width = int(root.geometry().split("x")[0]) - 30
    maxCol = (width // 150)
    maxColConst = maxCol
    row = 0
    col = 0
    newStr = False
    for i, button in enumerate(categoryButtonsAddPage):
        if i < maxCol:
            if i == 0:
                button.grid(row=row, column=col, pady=10, padx=3, ipady=10)
            else:
                col += 1
                button.grid(row=row, column=col, pady=10, padx=3, ipady=10)

            newStr = False

        else:
            row += 1
            col = 0
            maxCol += maxColConst
            button.grid(row=row, column=col, pady=10, padx=3, ipady=10)

            newStr = True

    if newStr:
        addCategoriesButton.grid(pady=10, padx=3, row=row, column=col + 1, ipady=10, ipadx=10, sticky=NW)
    elif not newStr and col + 1 == maxColConst:
        addCategoriesButton.grid(pady=10, padx=3, row=row + 1, column=0, ipady=10, ipadx=10, sticky=NW)
    else:
        addCategoriesButton.grid(pady=10, padx=3, row=row, column=col + 1, ipady=10, ipadx=10, sticky=NW)

    with open("TXT_files/geometry.txt", "w") as file:
        file.write(root.geometry())


def categoriesButtonAlignForCategoryPage():
    width = int(root.geometry().split("x")[0]) - 30
    maxCol = (width // 150)
    maxColConst = maxCol
    row = 0
    col = 0
    for i, button in enumerate(categoryButtonsCategoryPage):
        if i < maxCol:
            if i == 0:
                button.grid(row=row, column=col, pady=10, padx=3, ipady=10)
            else:
                col += 1
                button.grid(row=row, column=col, pady=10, padx=3, ipady=10)
        else:
            row += 1
            col = 0
            maxCol += maxColConst
            button.grid(row=row, column=col, pady=10, padx=3, ipady=10)


def onEntryClick(event):
    if addPrice.get() == "0":
        addPrice.delete(0, 'end')
        lineUnderEntry.configure(bootstyle=LIGHT)


def entryNotFocused(event):
    if addPrice.get() == "":
        addPrice.insert(0, "0")


def categoriesButton(category):
    for i in categoryButtonsAddPage:
        i.configure(bootstyle=[LIGHT, OUTLINE])
    categoryButtonsAddPage[category].configure(bootstyle=LIGHT)
    addObj["category"] = categoryButtonsAddPage[category]["text"]

    root.focus()


def onDateHover(box, mainText, minorText):
    if not str(addObj["date"]) == minorText["text"]:
        box.configure(style="My.TFrame")
        mainText.configure(style="My.TLabel", foreground="#ffffff")
        minorText.configure(style="My.TLabel", foreground="#dddddd")


def onDateNotHover(box, mainText, minorText):
    if not str(addObj["date"]) == minorText["text"]:
        box.configure(style='')
        mainText.configure(style='', foreground="#ADB5BD")
        minorText.configure(style='', foreground="#444444")


def dateSelect(date, box, mainText, minorText):
    addObj["date"] = date
    box.configure(style="My.TFrame")
    mainText.configure(style="My.TLabel", foreground="#ffffff")
    minorText.configure(style="My.TLabel", foreground="#dddddd")

    onDateNotHover(dateButtonYesterday, textDateLabelYesterday, dateLabelYesterday)
    onDateNotHover(dateButtonToday, textDateLabelToday, dateLabelToday)
    onDateNotHover(dateButtonSelect, textDateLabelSelect, dateLabelSelect)


def calendar(event):
    date = Querybox.get_date(title="", firstweekday=0)
    if date <= datetime.date.today():
        addObj["date"] = date
        if str(date) == dateLabelToday["text"]:
            dateSelect(date, dateButtonToday, textDateLabelToday, dateLabelToday)
        elif str(date) == dateLabelYesterday["text"]:
            dateSelect(date, dateButtonYesterday, textDateLabelYesterday, dateLabelYesterday)
        else:
            textDateLabelSelect["text"] = "Выбранная"
            dateLabelSelect["text"] = str(date)
            dateButtonSelect.configure(style="My.TFrame")
            dateLabelSelect.configure(style="My.TLabel", foreground="#dddddd")
            textDateLabelSelect.configure(style="My.TLabel", width=10, foreground="#ffffff")
    else:
        alertText.configure(background="#F8D7DA", font=(font, 15), width=28, foreground="#721C30")
        alertText["text"] = "Будущее заблокировано"

        alertBox.pack(anchor=SE, padx=7, expand=1, pady=15)
        alertText.pack(ipady=15)

        root.after(3000, hideAlerts)

    onDateNotHover(dateButtonYesterday, textDateLabelYesterday, dateLabelYesterday)
    onDateNotHover(dateButtonToday, textDateLabelToday, dateLabelToday)
    onDateNotHover(dateButtonSelect, textDateLabelSelect, dateLabelSelect)


def hideAlerts():
    alertText.pack_forget()
    alertBox.pack_forget()


def entryValid(key):
    if key.isdigit() or key == "":
        return True
    else:
        return False


def onButtonClick(symbol, result):
    try:
        with open("TXT_files/calculator.txt", "r") as file:
            isAnswer = file.read()

        if (result["text"] == "0" or result["text"] == "ошибка" or
            (isAnswer == "True" and not symbol in "+*-/")) and (not symbol in "CE="):
            result["text"] = symbol

            with open("TXT_files/calculator.txt", "w") as file:
                file.write("False")
        elif symbol == "=":
            result["text"] = str(eval(result["text"]))

            with open("TXT_files/calculator.txt", "w") as file:
                file.write("True")
        elif symbol == "C":
            result["text"] = "0"
        elif symbol == "CE":
            if result["text"] != "0" and result["text"] != "ошибка":
                result["text"] = result["text"][:len(result["text"]) - 1]
        elif symbol in "+*-/" and result["text"][len(result["text"]) - 1] in "+*-/":
            result["text"] = result["text"][:len(result["text"]) - 1] + symbol
        else:
            result["text"] += symbol

            with open("TXT_files/calculator.txt", "w") as file:
                file.write("False")

        if (result["width"] == 25 or result["width"] == 50) and symbol != "=":
            result.configure(font=(font, 10), width=50)
        elif len(result["text"]) + 1 == result["width"]:
            result["width"] += 1
            result.configure(font=(font, int(str(result["font"]).split(" ")[1]) - 2))
        elif len(result["text"]) + 1 < 10:
            result.configure(font=(font, 40), width=10)
        elif len(result["text"]) + 1 < result["width"]:
            result["width"] -= 1
            result.configure(font=(font, int(str(result["font"]).split(" ")[1]) + 2))

    except:
        result["text"] = "ошибка"


def calcOnHover(button):
    if button["text"] in "+*-/()CE.":
        button.configure(background="#595959")
    elif button["text"] == "=":
        button.configure(background="#004d1a")
    else:
        button.configure(background="#333333")


def calcNotHover(button):
    if button["text"] in "+*-/()CE.":
        button.configure(background="#333333")
    elif button["text"] == "=":
        button.configure(background="#006622")
    else:
        button.configure(background="#595959")


def calculator(event):
    calcRoot = Toplevel(title="Calculator")
    calcRoot.minsize(380, 510)
    calcRoot.maxsize(380, 510)
    calcRoot.title("калькулятор")

    resultFrame = ttk.Frame(calcRoot, height=100)
    buttonsFrame = ttk.Frame(calcRoot)

    resultFrame.pack(side=TOP, fill=X, expand=1)
    buttonsFrame.pack(side=TOP)

    result = ttk.Label(resultFrame, text="0", anchor=E, width=10, font=("Roboto", 40), foreground="#aaaaaa")

    result.pack(side=RIGHT)

    buttons = [
        ["(", 0, 0], [")", 0, 1], ["CE", 0, 2], ["C", 0, 3],
        ["7", 1, 0], ["8", 1, 1], ["9", 1, 2], ["+", 1, 3],
        ["4", 2, 0], ["5", 2, 1], ["6", 2, 2], ["-", 2, 3],
        ["1", 3, 0], ["2", 3, 1], ["3", 3, 2], ["*", 3, 3],
        [".", 4, 0], ["0", 4, 1], ["=", 4, 2], ["/", 4, 3]
    ]

    for button, row, column in buttons:
        if button.isdigit():
            calcButton = ttk.Label(buttonsFrame, text=button, foreground="#dddddd", font=("Roboto", 30),
                                   background="#595959", width=3, anchor=CENTER)

            calcButton.bind("<Button-1>", lambda y="", x=button: onButtonClick(x, result))
            calcButton.bind("<Enter>", lambda y="", x=calcButton: calcOnHover(x))
            calcButton.bind("<Leave>", lambda y="", x=calcButton: calcNotHover(x))
            calcButton.grid(row=row, column=column, padx=2, pady=2, ipady=10)
        elif button in "()+*-/.CE":
            calcButton = ttk.Label(buttonsFrame, text=button, foreground="#dddddd", font=("Roboto", 30),
                                   background="#333333", width=3, anchor=CENTER)

            calcButton.bind("<Button-1>", lambda y="", x=button: onButtonClick(x, result))
            calcButton.bind("<Enter>", lambda y="", x=calcButton: calcOnHover(x))
            calcButton.bind("<Leave>", lambda y="", x=calcButton: calcNotHover(x))
            calcButton.grid(row=row, column=column, padx=2, pady=2, ipady=10)
        elif button == "=":
            calcButton = ttk.Label(buttonsFrame, text=button, foreground="#dddddd", font=("Roboto", 30),
                                   background="#006622", width=3, anchor=CENTER)

            calcButton.bind("<Button-1>", lambda y="", x=button: onButtonClick(x, result))
            calcButton.bind("<Enter>", lambda y="", x=calcButton: calcOnHover(x))
            calcButton.bind("<Leave>", lambda y="", x=calcButton: calcNotHover(x))
            calcButton.grid(row=row, column=column, padx=2, pady=2, ipady=10)

    calcRoot.mainloop()


def makeCategoriesButtons_AddPage():
    with open("JSON_files/categories.json", "r") as json_file:
        categories = json.load(json_file)

    for i in range(len(categories)):
        button = ttk.Button(categoriesBox, text=categories[i][0], bootstyle=[LIGHT, OUTLINE],
                            command=lambda x=i: categoriesButton(x), width=15)
        categoryButtonsAddPage.append(button)


def makeCategoriesButtons_CategoriesPage():
    with open("JSON_files/categories.json", "r") as json_file:
        categoriesArray = json.load(json_file)

    for i in range(len(categoriesArray)):
        button = ttk.Button(allCategories, text=categoriesArray[i][0], bootstyle=[LIGHT, OUTLINE], width=15,
                            command=lambda x=categoriesArray[i][0]: deleteCategory(x))
        categoryButtonsCategoryPage.append(button)


def saveCategory():
    with open("JSON_files/categories.json", "r") as json_file:
        categories = json.load(json_file)
    category = addCategoryEntry.get()
    for i in categories:
        if category == i[0]:
            alertText.configure(background="#F8D7DA", font=(font, 15), width=28, foreground="#721C30")
            alertText["text"] = "Категория уже существует"

            alertBox.pack(anchor=SE, padx=7, expand=1, pady=15)
            alertText.pack(ipady=15)

            root.after(3000, hideAlerts)

            lineUnderAddEntry.configure(bootstyle=DANGER)
            return 0
    if category == "-0":
        category = "Темирлан?"
    addCategoryEntry.delete(0, END)
    if len(category) > 12:
        lineUnderAddEntry.configure(bootstyle=DANGER)
        addCategoryEntry.configure(font=(font, 10), width=40)
        addCategoryEntry.delete(0, END)
        addCategoryEntry.insert(0, "Длинна не может превышать 12 символов")

        return 0

    with open("JSON_files/categories.json", "r") as json_file:
        categories = json.load(json_file)

    colorGenerate = "1234567890abcdef"
    color = f"#{colorGenerate[random.randint(0, len(colorGenerate) - 1)]}{colorGenerate[random.randint(0, len(colorGenerate) - 1)]}{colorGenerate[random.randint(0, len(colorGenerate) - 1)]}{colorGenerate[random.randint(0, len(colorGenerate) - 1)]}{colorGenerate[random.randint(0, len(colorGenerate) - 1)]}{colorGenerate[random.randint(0, len(colorGenerate) - 1)]}"

    categories.append([category, color])

    with open("JSON_files/categories.json", "w") as json_file:
        json.dump(categories, json_file)

    button = ttk.Button(allCategories, text=category, bootstyle=[LIGHT, OUTLINE], width=15,
                        command=lambda x=category: deleteCategory(x))
    categoryButtonsCategoryPage.append(button)

    button = ttk.Button(categoriesBox, text=category, bootstyle=[LIGHT, OUTLINE],
                        command=lambda x=len(categoryButtonsCategoryPage) - 1: categoriesButton(x), width=15)
    categoryButtonsAddPage.append(button)

    cancelCategory()


def addCategoryOpen():
    commonCategoriesBox.grid_forget()
    addCategoryBox.grid(row=0, sticky=N)


def cancelCategory():
    addCategoryBox.grid_forget()
    lineUnderAddEntry.configure(bootstyle=LIGHT)
    addCategoryEntry.delete(0, "end")
    commonCategoriesBox.grid(row=0, sticky=N)


def clearEntry(event):
    if addCategoryEntry.get() == "Длинна не может превышать 12 символов":
        addCategoryEntry.delete(0, END)
        addCategoryEntry.configure(font=(font, 13), width=13)
    lineUnderAddEntry.configure(bootstyle=LIGHT)


def deleteCategory(category):
    delete = Messagebox.show_question(message="Удалить категорию", buttons=['Отмена:success', 'Удалить:danger'],
                                      alert=True)

    if delete == "Удалить":
        with open("JSON_files/categories.json", "r") as json_file:
            categories = json.load(json_file)

        if addObj["category"] == category:
            addObj["category"] = ""

        for i, cat in enumerate(categories):
            if cat[0] == category:
                categoryButtonsCategoryPage[i].destroy()
                categoryButtonsCategoryPage.pop(i)

                categoryButtonsAddPage[i].destroy()
                categoryButtonsAddPage.pop(i)

                categories.pop(i)
                break

        with open("JSON_files/categories.json", "w") as json_file:
            json.dump(categories, json_file)

        with open("JSON_files/spending.json", "r") as json_file:
            spendings = json.load(json_file)

        deleted = False
        while not deleted:
            deleted = True
            for i, spending in enumerate(spendings):
                if spending["category"] == category:
                    spendings.pop(i)
                    deleted = False
                    break

        with open("JSON_files/spending.json", "w") as json_file:
            json.dump(spendings, json_file)

        datePick("", "week", False)


header = ttk.Frame(addPage)
header.pack(fill=X)
mainBody = ttk.Frame(addPage, padding=10)
mainBody.pack(pady=10)
footer = ttk.Frame(addPage, padding=10)
footer.pack(fill=X)

## -------------------------------------------------
## ADDPAGE
## -------------------------------------------------


font = font.Font(family="Roboto", weight="normal")
priceFrame = ttk.Frame(header)
priceFrame.pack(side=TOP)

style = Style()
style.configure("TEntry", fieldbackground='dark')
addPrice = ttk.Entry(priceFrame, justify=CENTER, font=(font, 13), foreground="#ADB5BD", width=13, validate="key",
                     validatecommand=(root.register(entryValid), "%P"))
addPrice.insert(0, "0")
addPrice.bind("<Button-1>", onEntryClick)
addPrice.bind('<FocusOut>', entryNotFocused)
addPrice.grid(pady=(15, 0), row=0, column=0, sticky=S)

ToolTip(addPrice, text="Впишите цену", bootstyle=[SECONDARY, INVERSE])

lineUnderEntry = ttk.Frame(priceFrame, bootstyle=LIGHT, width=150)
lineUnderEntry.grid(column=0, row=1)

currency = ttk.Label(priceFrame, text="KZT", bootstyle=LIGHT, font=(font, 14))
currency.grid(row=0, column=2, sticky=SE)

img = Image.open("images/calculatorIcon.png")
img = img.resize((40, 40))

image = ImageTk.PhotoImage(img)

calculatorButton = ttk.Label(priceFrame, image=image, cursor="hand2")
calculatorButton.bind("<Button-1>", calculator)
calculatorButton.grid(sticky=SW, padx=5, row=0, column=3)

commonCategoriesBox = ttk.Frame(mainBody)
commonCategoriesBox.grid(row=0, sticky=N)

addCategoryBox = ttk.Frame(mainBody)

addCategoryEntry = ttk.Entry(addCategoryBox, justify=CENTER, font=(font, 13), foreground="#ADB5BD", width=13)
addCategoryEntry.bind("<Button-1>", clearEntry)
addCategoryEntry.grid(sticky=S, row=0)

lineUnderAddEntry = ttk.Frame(addCategoryBox, bootstyle=LIGHT, width=150)
lineUnderAddEntry.grid(sticky=N, row=1, pady=(0, 15))

buttonsBox = ttk.Frame(addCategoryBox)
buttonsBox.grid(row=3, sticky=N)

saveCategoryButton = ttk.Button(buttonsBox, text="Сохранить", bootstyle=[SUCCESS, OUTLINE], command=saveCategory)
saveCategoryButton.grid(sticky=N, row=0, column=1, padx=(10, 0))

cancelCategoryButton = ttk.Button(buttonsBox, text="Отмена", bootstyle=[DANGER, OUTLINE], command=cancelCategory)
cancelCategoryButton.grid(sticky=N, row=0, column=0)

categoriesLabelBox = ttk.Frame(commonCategoriesBox)
categoriesLabelBox.pack(anchor=NW)
categoriesLabel = ttk.Label(categoriesLabelBox, text="Категория", bootstyle=[LIGHT], font=(font, 11))
categoriesLabel.grid()

categoryButtonsAddPage = []
categoryButtonsCategoryPage = []

categoriesBox = ttk.Frame(commonCategoriesBox)
categoriesBox.pack()

makeCategoriesButtons_AddPage()

addCategoriesButton = ttk.Button(categoriesBox, text="+", bootstyle=[LIGHT, OUTLINE], command=addCategoryOpen)

root.bind("<Configure>", categoriesButtonAlignForAddPage)

dateBox = ttk.Frame(mainBody)
dateBox.grid(row=1, pady=(30, 0), sticky=W)

styleFrame = Style()
styleFrame.configure("My.TFrame", background="#00BC8C")

styleLabel = Style()
styleLabel.configure("My.TLabel", background="#00BC8C")

dateButtonToday = ttk.Frame(dateBox, style="My.TFrame", cursor="hand2")

textDateLabelToday = ttk.Label(dateButtonToday, text="Сегодня", foreground="#ffffff",
                               style="My.TLabel", font=(font, 11), width=9, anchor=CENTER)
dateLabelToday = ttk.Label(dateButtonToday, text=str(addObj["date"]), font=(font, 9), foreground="#dddddd",
                           anchor=CENTER, style="My.TLabel", width=12)

dateButtonYesterday = ttk.Frame(dateBox, cursor="hand2")

textDateLabelYesterday = ttk.Label(dateButtonYesterday, text="Вчера", bootstyle=[LIGHT], font=(font, 11), width=9,
                                   anchor=CENTER)
dateLabelYesterday = ttk.Label(dateButtonYesterday, text=str(addObj["date"] - datetime.timedelta(1)), font=(font, 9),
                               foreground="#444444",
                               anchor=CENTER, width=12)
dateButtonSelect = ttk.Frame(dateBox, cursor="hand2")

textDateLabelSelect = ttk.Label(dateButtonSelect, text="Позавчера", bootstyle=[LIGHT], font=(font, 11), width=9,
                                anchor=CENTER)
dateLabelSelect = ttk.Label(dateButtonSelect, text=str(addObj["date"] - datetime.timedelta(2)), font=(font, 9),
                            foreground="#444444",
                            anchor=CENTER, width=12)

dateButtonToday.bind("<Button-1>", lambda x="": dateSelect(datetime.date.today(), dateButtonToday, textDateLabelToday,
                                                           dateLabelToday))
dateButtonYesterday.bind("<Button-1>",
                         lambda x="": dateSelect(datetime.date.today() - datetime.timedelta(1), dateButtonYesterday,
                                                 textDateLabelYesterday, dateLabelYesterday))
dateButtonSelect.bind("<Button-1>",
                      lambda x="": dateSelect(dateLabelSelect["text"], dateButtonSelect,
                                              textDateLabelSelect, dateLabelSelect))
dateLabelToday.bind("<Button-1>", lambda x="": dateSelect(datetime.date.today(), dateButtonToday, textDateLabelToday,
                                                          dateLabelToday))
dateLabelYesterday.bind("<Button-1>",
                        lambda x="": dateSelect(datetime.date.today() - datetime.timedelta(1), dateButtonYesterday,
                                                textDateLabelYesterday, dateLabelYesterday))
dateLabelSelect.bind("<Button-1>",
                     lambda x="": dateSelect(dateLabelSelect["text"], dateButtonSelect,
                                             textDateLabelSelect, dateLabelSelect))
textDateLabelToday.bind("<Button-1>",
                        lambda x="": dateSelect(datetime.date.today(), dateButtonToday, textDateLabelToday,
                                                dateLabelToday))
textDateLabelYesterday.bind("<Button-1>",
                            lambda x="": dateSelect(datetime.date.today() - datetime.timedelta(1), dateButtonYesterday,
                                                    textDateLabelYesterday, dateLabelYesterday))
textDateLabelSelect.bind("<Button-1>",
                         lambda x="": dateSelect(dateLabelSelect["text"], dateButtonSelect,
                                                 textDateLabelSelect, dateLabelSelect))

dateButtonToday.bind("<Enter>",
                     lambda x="": onDateHover(dateButtonToday, textDateLabelToday, dateLabelToday))
dateButtonYesterday.bind("<Enter>",
                         lambda x="": onDateHover(dateButtonYesterday, textDateLabelYesterday, dateLabelYesterday))
dateButtonSelect.bind("<Enter>",
                      lambda x="": onDateHover(dateButtonSelect, textDateLabelSelect, dateLabelSelect))

dateButtonToday.bind("<Leave>",
                     lambda x="": onDateNotHover(dateButtonToday, textDateLabelToday, dateLabelToday))
dateButtonYesterday.bind("<Leave>",
                         lambda x="": onDateNotHover(dateButtonYesterday, textDateLabelYesterday, dateLabelYesterday))
dateButtonSelect.bind("<Leave>",
                      lambda x="": onDateNotHover(dateButtonSelect, textDateLabelSelect, dateLabelSelect))

calendarFrame = ttk.Frame(dateBox)

img = ImageTk.PhotoImage(Image.open('images/calendarIcon.png').resize((30, 30)))
calendarButton = ttk.Label(calendarFrame, image=img, cursor="hand2")

calendarButton.bind("<Button-1>", calendar)

dateButtonToday.grid(column=0, row=0)
textDateLabelToday.pack()
dateLabelToday.pack()
dateButtonYesterday.grid(column=1, row=0, padx=15)
textDateLabelYesterday.pack()
dateLabelYesterday.pack()
dateButtonSelect.grid(column=2, row=0)
textDateLabelSelect.pack()
dateLabelSelect.pack()
calendarFrame.grid(column=3, row=0, padx=(10, 0), sticky=SE)
calendarButton.pack()

commentFrame = ttk.Labelframe(mainBody, text="комментарий", borderwidth=0, bootstyle=LIGHT)
commentFrame.grid(row=3, pady=(30, 20), sticky=NW)

commentEntry = tk.Text(commentFrame, font=(font, 13), width=50, height=1)
scrollbar = ttk.Scrollbar(commentFrame, command=commentEntry.yview(), orient="vertical")
commentEntry.bind("<FocusIn>", lambda x="": commentEntry.configure(height=5))
commentEntry.bind("<FocusOut>", lambda x="": commentEntry.configure(height=1))
commentEntry.configure(yscrollcommand=scrollbar.set)
commentEntry.configure(background="#222222", border=0, highlightthickness=0, foreground="#ababab")
commentEntry.grid(row=0, sticky=NW)

underCommentLine = ttk.Frame(commentFrame, borderwidth=1, relief=SUNKEN, width=605)
underCommentLine.grid(row=1, sticky=NW)

alertBox = ttk.Frame(addPage)
alertText = ttk.Label(alertBox, text="Трата успешно добавлена", bootstyle="success-inverse", font=(font, 15), width=28,
                      anchor=CENTER, foreground="#dddddd")

submitButton = ttk.Button(footer, text="ДОБАВИТЬ", bootstyle=[SUCCESS, OUTLINE],
                          command=submit)
submitButton.pack(ipady=10, ipadx=10, side=TOP)

## -------------------------------------------------
## ADDPAGE
## -------------------------------------------------


## -------------------------------------------------
## CATEGORIES PAGE
## -------------------------------------------------
allCategories = ttk.Frame(categoriesPage)
allCategories.pack()

makeCategoriesButtons_CategoriesPage()


## -------------------------------------------------
## CATEGORIES PAGE
## -------------------------------------------------


## -------------------------------------------------
## Main PAGE
## -------------------------------------------------

def datePick(event, date, changePeriod):
    for widget in expansesInCategoryFrame.winfo_children():
        widget.destroy()

    goBackButton.pack_forget()
    previousPageButton.configure(command=lambda x="": previousPage_Categories(date))
    expansesInCategoryFrame.pack_forget()
    expansesFrame.pack(side=BOTTOM)

    def expansePlaceOnPage(dateArea):
        uniqueCategories = []
        uniqueCategoriesForIf = []

        for i in spendingsInDate:
            if not i["category"] in uniqueCategoriesForIf:
                color = ""
                for cat in categories_mainPage:
                    if cat[0] == i["category"]:
                        color = cat[1]
                uniqueCategories.append({"category": i["category"], "sum": 0, "color": f"{color}"})
                uniqueCategoriesForIf.append(i["category"])

        for i in spendingsInDate:
            for j in uniqueCategories:
                if i["category"] == j["category"]:
                    j["sum"] += i["price"]

        cat = []
        sum = []
        colors = []
        allSpendingSum = 0

        for i in uniqueCategories:
            cat.append(i["category"])
            sum.append(i["sum"])
            colors.append(i["color"])
            allSpendingSum += i["sum"]

        if uniqueCategories == []:
            diagramEmpty = ImageTk.PhotoImage(Image.open("images/diagramEmpty.png"))
            diagramLabel.configure(image=diagramEmpty)
            diagramLabel.image = diagramEmpty
            return 0

        sort = False
        while not sort:
            sort = True
            for i in range(len(uniqueCategories) - 1):
                if uniqueCategories[i]["sum"] < uniqueCategories[i + 1]["sum"]:
                    uniqueCategories[i], uniqueCategories[i + 1] = uniqueCategories[i + 1], uniqueCategories[i]
                    sort = False

        nextPageButton.configure(command=lambda x="": nextPage_Categories(date, len(uniqueCategories) // 3 + 1))
        if len(uniqueCategories) // 3 == 0 or (len(uniqueCategories) // 3 == 1 and len(uniqueCategories) % 3 == 0):
            nextPageButton.configure(state=DISABLED)
        else:
            nextPageButton.configure(state=NORMAL)

        fig, diagram = plt.subplots()
        diagram.axis("equal")
        diagram.pie(sum, labels=None, startangle=90, wedgeprops=dict(width=0.4), colors=colors)
        diagram.set_title(f"{allSpendingSum} KZT", fontsize=20, color="#bababa", pad=0)

        plt.savefig("images/diagram.png", transparent=True)

        diagramPNG = ImageTk.PhotoImage(Image.open("images/diagram.png"))

        diagramLabel.configure(image=diagramPNG)
        diagramLabel.image = diagramPNG
        plt.close(fig)
        expanseCreate(uniqueCategories, allSpendingSum, len(str(max(sum))), date, dateArea, currentPage["text"])

    spendingsInDate = []
    with open("JSON_files/spending.json", "r") as json_file:
        spendings = json.load(json_file)
    with open("JSON_files/categories.json", "r") as json_file:
        categories_mainPage = json.load(json_file)

    for widget in expansesFrame.winfo_children():
        widget.destroy()

    months = ["янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"]
    monthsFull = ["Январь", "Февраль", "Мар", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь",
                  "Ноябрь", "Декабрь"]

    match date:
        case "day":
            dayLabel.config(bootstyle=SUCCESS)
            dayLine.grid(row=1, column=0, sticky=N, padx=10)

            weekLabel.config(bootstyle=LIGHT)
            weekLine.grid_forget()
            monthLabel.config(bootstyle=LIGHT)
            monthLine.grid_forget()
            yearLabel.config(bootstyle=LIGHT)
            yearLine.grid_forget()
            periodLabel.config(bootstyle=LIGHT)
            periodLine.grid_forget()

            dateArea = datetime.date.today()

            currentDateLabel["text"] = f"{datetime.date.today().day} {months[datetime.date.today().month - 1]}"

            for spending in spendings:
                if spending["date"] == str(datetime.date.today()):
                    spendingsInDate.append(spending)
            expansePlaceOnPage(dateArea)
        case "week":
            weekLabel.config(bootstyle=SUCCESS)
            weekLine.grid(row=1, column=1, sticky=N, padx=10)

            dayLabel.config(bootstyle=LIGHT)
            dayLine.grid_forget()
            monthLabel.config(bootstyle=LIGHT)
            monthLine.grid_forget()
            yearLabel.config(bootstyle=LIGHT)
            yearLine.grid_forget()
            periodLabel.config(bootstyle=LIGHT)
            periodLine.grid_forget()

            weekStart = datetime.date.today() - datetime.timedelta(datetime.date.today().weekday())
            weekEnd = datetime.date.today() + datetime.timedelta((6 - datetime.date.today().weekday()))
            dateArea = [weekStart, weekEnd]

            currentDateLabel["text"] = \
                f"{weekStart.day} {months[weekStart.month - 1]} - {weekEnd.day} {months[weekEnd.month - 1]}"

            for spending in spendings:
                if ((datetime.datetime.today() - datetime.timedelta(
                        datetime.datetime.now().weekday())) <=
                        datetime.datetime.strptime(spending["date"] + " 23:59:00", "%Y-%m-%d %H:%M:%f")):
                    spendingsInDate.append(spending)
            expansePlaceOnPage(dateArea)
        case "month":
            monthLabel.config(bootstyle=SUCCESS)
            monthLine.grid(row=1, column=2, sticky=N, padx=10)

            dayLabel.config(bootstyle=LIGHT)
            dayLine.grid_forget()
            weekLabel.config(bootstyle=LIGHT)
            weekLine.grid_forget()
            yearLabel.config(bootstyle=LIGHT)
            yearLine.grid_forget()
            periodLabel.config(bootstyle=LIGHT)
            periodLine.grid_forget()

            dateArea = datetime.date.today()

            currentDateLabel["text"] = f"{monthsFull[datetime.date.today().month - 1]} {datetime.date.today().year} год"

            for spending in spendings:
                if spending["date"][5:7] == str(datetime.date.today())[5:7]:
                    spendingsInDate.append(spending)
            expansePlaceOnPage(dateArea)
        case "year":
            yearLabel.config(bootstyle=SUCCESS)
            yearLine.grid(row=1, column=3, sticky=N, padx=10)

            dayLabel.config(bootstyle=LIGHT)
            dayLine.grid_forget()
            weekLabel.config(bootstyle=LIGHT)
            weekLine.grid_forget()
            monthLabel.config(bootstyle=LIGHT)
            monthLine.grid_forget()
            periodLabel.config(bootstyle=LIGHT)
            periodLine.grid_forget()

            dateArea = datetime.date.today()

            currentDateLabel["text"] = f"{datetime.date.today().year} год"

            for spending in spendings:
                if spending["date"][:4] == str(datetime.date.today())[:4]:
                    spendingsInDate.append(spending)
            expansePlaceOnPage(dateArea)
        case "period":
            if not changePeriod:
                startDate = datetime.datetime.strptime(currentDateLabel["text"].split(" - ")[0], "%d %b %Y")
                endDate = datetime.datetime.strptime(currentDateLabel["text"].split(" - ")[1], "%d %b %Y")
                dateArea = [startDate, endDate]
                for spending in spendings:
                    if startDate <= datetime.datetime.strptime(spending["date"], "%Y-%m-%d") <= endDate:
                        spendingsInDate.append(spending)
                currentDateLabel["text"] = (f"{startDate.day} {months[startDate.month - 1]} {startDate.year} - "
                                            f"{endDate.day} {months[endDate.month - 1]} {endDate.year}")
                currentDateLabel.pack(side=BOTTOM, pady=(15, 0))
                datePickerFrame.pack(side=TOP)
                expansePlaceOnPage(dateArea)
                return 0
            datePickerFrame.pack_forget()
            currentDateLabel.pack_forget()
            toolsFrame.pack_forget()

            def getStartDate():
                startDate = Querybox.get_date(title="", firstweekday=0)
                if startDate > datetime.date.today():
                    return 0
                startDateButton["text"] = str(startDate)

            def getEndDate():
                endDate = Querybox.get_date(title="", firstweekday=0)
                if endDate > datetime.date.today() + datetime.timedelta(6 - datetime.date.today().weekday()):
                    return 0
                endDateButton["text"] = str(endDate)

            def cancelPeriodDate():
                datePickerFrame.pack(side=TOP)
                toolsFrame.pack(side=TOP, fill=X)
                periodFrame.destroy()
                datePick("", "week", True)

            def acceptPeriodDate():
                if startDateButton["text"] == "Начало" or endDateButton["text"] == "Конец":
                    return 0

                startDate = datetime.datetime.strptime(startDateButton["text"], "%Y-%m-%d")
                endDate = datetime.datetime.strptime(endDateButton["text"], "%Y-%m-%d")

                dateArea = [startDate, endDate]

                if endDate < startDate:
                    endDateButton["text"] = "Конец"
                    return 0
                elif endDate == datetime.datetime.strptime(str(datetime.date.today()),
                                                           "%Y-%m-%d") and startDate == endDate:
                    datePick("", "day", False)
                    datePickerFrame.pack(side=TOP)
                    periodFrame.destroy()
                    return 0
                elif endDate == datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d") + datetime.timedelta(
                        (
                                6 - datetime.date.today().weekday())) and startDate == datetime.datetime.strptime(
                    (str(datetime.date.today() - datetime.timedelta(
                        datetime.date.today().weekday()))), "%Y-%m-%d"):

                    datePick("", "week", False)
                    datePickerFrame.pack(side=TOP)
                    periodFrame.destroy()
                    return 0

                for spending in spendings:
                    if startDate <= datetime.datetime.strptime(spending["date"], "%Y-%m-%d") <= endDate:
                        spendingsInDate.append(spending)
                currentDateLabel["text"] = (f"{startDate.day} {months[startDate.month - 1]} {startDate.year} - "
                                            f"{endDate.day} {months[endDate.month - 1]} {endDate.year}")
                currentDateLabel.pack(side=BOTTOM, pady=(15, 0))
                datePickerFrame.pack(side=TOP)
                periodFrame.destroy()
                toolsFrame.pack(side=TOP, fill=X)
                expansePlaceOnPage(dateArea)

            periodFrame = ttk.Frame(mainBlock)
            periodFrame.pack(side=TOP)
            startDateButton = ttk.Button(periodFrame, text="Начало", bootstyle=INFO, command=getStartDate)
            startDateButton.grid(row=0, column=0)

            dashButton = ttk.Label(periodFrame, text="-", bootstyle=LIGHT, font=(font, 20))
            dashButton.grid(row=0, column=1, padx=20, sticky=E)

            endDateButton = ttk.Button(periodFrame, text="Конец", bootstyle=INFO, command=getEndDate)
            endDateButton.grid(row=0, column=2, sticky=W)

            cancelDateButton = ttk.Button(periodFrame, text="Отмена", bootstyle=DANGER, command=cancelPeriodDate)
            cancelDateButton.grid(row=1, column=0, pady=(15, 0))

            submitDateButton = ttk.Button(periodFrame, text="Применить", bootstyle=SUCCESS, command=acceptPeriodDate)
            submitDateButton.grid(row=1, column=2, pady=(15, 0))

            periodLabel.config(bootstyle=SUCCESS)
            periodLine.grid(row=1, column=4, sticky=N, padx=10)

            dayLabel.config(bootstyle=LIGHT)
            dayLine.grid_forget()
            weekLabel.config(bootstyle=LIGHT)
            weekLine.grid_forget()
            monthLabel.config(bootstyle=LIGHT)
            monthLine.grid_forget()
            yearLabel.config(bootstyle=LIGHT)
            yearLine.grid_forget()


def showComment(event, expanse):
    expanseRoot = Toplevel(title="expanse", minsize=(300, 450), maxsize=(300, 450))

    months = ["янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"]

    expanseInfoFrame = ttk.Frame(expanseRoot)
    expanseInfoFrame.pack(side=TOP, pady=(15, 25), fill=X)

    expanseCategoryFrame = ttk.LabelFrame(expanseInfoFrame, text="Категория", borderwidth=0)
    expanseCategoryFrame.pack(anchor=NW, pady=(0, 20))
    expanseCategory = ttk.Label(expanseCategoryFrame, text=expanse["category"], font=(font, 13),
                                width=len(expanse["category"]) + 1, bootstyle=LIGHT)
    expanseCategory.pack(anchor=NW, padx=(10, 0))

    expansePriceFrame = ttk.LabelFrame(expanseInfoFrame, text="Сумма", borderwidth=0)
    expansePriceFrame.pack(anchor=NW, pady=(0, 20))
    expansePrice = ttk.Label(expansePriceFrame, text=f"{expanse["price"]} KZT", font=(font, 12),
                             width=len(str(expanse["price"])) + 5, bootstyle=LIGHT)
    expansePrice.pack(anchor=NW, padx=(10, 0))

    expanseDateFrame = ttk.LabelFrame(expanseInfoFrame, text="Дата", borderwidth=0)
    expanseDateFrame.pack(anchor=NW, pady=(0, 20))
    expanseDate = ttk.Label(expanseDateFrame,
                            text=f"{expanse["date"][8:]} {months[int(expanse["date"][5:7]) - 1]} {expanse["date"][:4]}",
                            font=(font, 13), width=11, bootstyle=LIGHT)
    expanseDate.pack(anchor=NW, padx=(10, 0))

    expanseCommentFrame = ttk.LabelFrame(expanseRoot, text="Комментарий", borderwidth=0)
    expanseCommentFrame.pack(anchor=NW)
    expanseComment = tk.Text(expanseCommentFrame, width=22, font=(font, 13), height=7)
    scroll = ttk.Scrollbar(expanseCommentFrame, orient="vertical", command=expanseComment.yview())
    expanseComment.insert(1.0, expanse["comment"])
    expanseComment.configure(background="#222222", foreground="#ADB5BD", highlightthickness=0, state=DISABLED)
    expanseComment.pack(anchor=NW, padx=(9, 0))


def expanseExpand(event, expanseCategory, unit, date, firstPage):
    for widget in expansesInCategoryFrame.winfo_children():
        widget.destroy()
    if firstPage:
        currentPage["text"] = "1"
        previousPageButton.configure(state=DISABLED)
    expansesFrame.pack_forget()
    expansesInCategoryFrame.pack(side=TOP)

    goBackButton.configure(command=lambda x=unit: datePick("", x, False))
    goBackButton.pack(anchor=NE, side=LEFT)
    previousPageButton.configure(command=lambda x="": previousPage_Expanses(unit, expanseCategory, date))

    with open("JSON_files/spending.json", "r") as json_file:
        expanses = []
        for expanse in json.load(json_file):
            if unit == "day" and str(date) == expanse["date"]:
                expanses.append(expanse)
            elif unit == "week" and datetime.datetime.strptime(str(date[0]), "%Y-%m-%d") <= datetime.datetime.strptime(
                    expanse["date"], "%Y-%m-%d") <= datetime.datetime.strptime(str(date[1]), "%Y-%m-%d"):
                expanses.append(expanse)
            elif unit == "month" and date.month == datetime.datetime.strptime(expanse["date"],
                                                                              "%Y-%m-%d").month and date.year == datetime.datetime.strptime(
                expanse["date"], "%Y-%m-%d").year:
                expanses.append(expanse)
            elif unit == "year" and date.year == datetime.datetime.strptime(expanse["date"], "%Y-%m-%d").year:
                expanses.append(expanse)
            elif unit == "period" and date[0] <= datetime.datetime.strptime(expanse["date"], "%Y-%m-%d") <= date[1]:
                expanses.append(expanse)

    sort = False
    maxPriceLen = 0
    while not sort:
        sort = True
        for i in range(len(expanses) - 1):
            if datetime.datetime.strptime(expanses[i]["date"], "%Y-%m-%d") < datetime.datetime.strptime(
                    expanses[i + 1]["date"],
                    "%Y-%m-%d"):
                expanses[i], expanses[i + 1] = expanses[i + 1], expanses[i]
                sort = False

    for i in expanses:
        if maxPriceLen < i["price"]:
            maxPriceLen = i["price"]

    months = ["янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"]

    countOfExpanseInCategory = 0
    for i, expanse in enumerate(expanses):
        if expanse["category"] == expanseCategory:
            countOfExpanseInCategory += 1
            if not (int(currentPage["text"]) - 1) * 3 <= countOfExpanseInCategory - 1 < int(currentPage["text"]) * 3:
                continue
            style = Style()
            style.configure("ExpanseFrame.TFrame", background="#343A40")
            expanseFrame = ttk.Frame(expansesInCategoryFrame, style="ExpanseFrame.TFrame")
            expanseFrame.pack(pady=(0, 10))

            style = Style()
            style.configure("ExpanseLabel.TLabel", background="#343A40")
            if expanse["comment"] != "":
                expanseLabel = ttk.Label(expanseFrame, text=expanseCategory, font=(font, 12),
                                         style="ExpanseLabel.TLabel",
                                         width=15, foreground="#cacaca")
                expanseLabel.grid(row=0, column=0, ipady=10, padx=(10, 0))

                expanseCommentLabel = ttk.Label(expanseFrame, text=expanse["comment"][0:3] + "...", font=(font, 12),
                                                style="ExpanseLabel.TLabel",
                                                width=7, foreground="#aaaaaa", cursor="hand2")
                expanseCommentLabel.bind("<Button-1>", lambda x="", y=expanse: showComment(x, y))
                expanseCommentLabel.grid(row=0, column=1, ipady=10, padx=(0, 10))
            else:
                expanseLabel = ttk.Label(expanseFrame, text=expanseCategory, font=(font, 12),
                                         style="ExpanseLabel.TLabel",
                                         width=22, foreground="#cacaca")
                expanseLabel.grid(row=0, column=0, ipady=10, padx=(10, 15))

            expanseDate = ttk.Label(expanseFrame, text=f"{expanse["date"][8:]} {months[int(expanse["date"][5:7]) - 1]}",
                                    font=(font, 10), style="ExpanseLabel.TLabel", width=6, foreground="#aaaaaa")
            expanseDate.grid(row=0, column=2, ipady=10, padx=(0, 15))

            expansePrice = ttk.Label(expanseFrame, text=f"{expanse["price"]} KZT",
                                     font=(font, 12), style="ExpanseLabel.TLabel", width=len(str(maxPriceLen)) + 4,
                                     foreground="#cacaca")
            expansePrice.grid(row=0, column=3, ipady=10)

            trash = ImageTk.PhotoImage(Image.open("images/trash.png").resize((20, 20)))
            trashIcon = ttk.Label(expanseFrame, style="ExpanseLabel.TLabel", width=5, image=trash, cursor="hand2")
            trashIcon.image = trash
            trashIcon.bind("<Button-1>", lambda x="", y=expanse, z=expanseFrame: deleteExpense(x, y, z))
            trashIcon.grid(row=0, column=4, ipady=10, padx=10)
    nextPageButton.configure(
        command=lambda x="": nextPage_Expanses(unit, expanseCategory, date, countOfExpanseInCategory // 3 + 1))
    if countOfExpanseInCategory // 3 == 0 or (countOfExpanseInCategory // 3 == 1 and countOfExpanseInCategory % 3 == 0):
        nextPageButton.configure(state=DISABLED)
    else:
        nextPageButton.configure(state=NORMAL)


def deleteExpense(event, exp, el):
    with open("JSON_files/spending.json", "r") as json_file:
        expanses = json.load(json_file)

    expanses.pop(expanses.index(exp))

    with open("JSON_files/spending.json", "w") as json_file:
        json.dump(expanses, json_file)

    el.destroy()


def expanseCreate(expansesCategory, allMoneySum, maxSumLen, unit, date, page):
    for i, expanse in enumerate(expansesCategory):
        if not (int(page) - 1) * 3 <= i < int(page) * 3:
            continue
        style = Style()
        style.configure("ExpanseFrame.TFrame", background="#343A40")
        expanseFrame = ttk.Frame(expansesFrame, style="ExpanseFrame.TFrame", cursor="hand2")
        expanseFrame.bind("<Button-1>",
                          lambda x="", y=expanse["category"], z=unit, w=date, v=True: expanseExpand(x, y, z, w, v))
        expanseFrame.pack(pady=(0, 10))

        expanseColorBox = ttk.Label(expanseFrame, background=expanse["color"], font=12, width=2, cursor="hand2")
        expanseColorBox.bind("<Button-1>",
                             lambda x="", y=expanse["category"], z=unit, w=date, v=True: expanseExpand(x, y, z, w, v))
        expanseColorBox.grid(column=0, row=0, padx=(10, 0), sticky=S)

        style = Style()
        style.configure("ExpanseLabel.TLabel", background="#343A40")
        expanseLabel = ttk.Label(expanseFrame, text=expanse["category"], font=(font, 12), width=15,
                                 foreground="#cacaca",
                                 cursor="hand2", style="ExpanseLabel.TLabel")
        expanseLabel.bind("<Button-1>",
                          lambda x="", y=expanse["category"], z=unit, w=date, v=True: expanseExpand(x, y, z, w, v))
        expanseLabel.grid(row=0, column=1, padx=15, ipady=10, sticky=W, rowspan=2)

        expansePercentLabel = ttk.Label(expanseFrame, text=f"{round((expanse["sum"] / allMoneySum) * 100, 1)}%",
                                        style="ExpanseLabel.TLabel", foreground="#aaaaaa", font=(font, 10), width=7)
        expansePercentLabel.bind("<Button-1>",
                                 lambda x="", y=expanse["category"], z=unit, w=date, v=True: expanseExpand(x, y, z, w,
                                                                                                           v))
        expansePercentLabel.grid(row=0, column=2, sticky=S)

        expanseMoneyLabel = ttk.Label(expanseFrame, text=f"{expanse["sum"]} KZT",
                                      style="ExpanseLabel.TLabel", foreground="#cacaca", font=(font, 13),
                                      width=maxSumLen + 5, anchor=S)
        expanseMoneyLabel.bind("<Button-1>",
                               lambda x="", y=expanse["category"], z=unit, w=date, v=True: expanseExpand(x, y, z, w, v))
        expanseMoneyLabel.grid(row=0, column=3, sticky=S, padx=(10, 0))


def previousPage_Categories(date):
    nextPageButton.configure(state=NORMAL)
    currentPage["text"] = str(int(currentPage["text"]) - 1)
    datePick("", date, False)
    if currentPage["text"] == "1":
        previousPageButton.configure(state=DISABLED)


def nextPage_Categories(date, maxPage):
    previousPageButton.config(state=NORMAL)
    currentPage["text"] = str(int(currentPage["text"]) + 1)
    datePick("", date, False)
    if currentPage["text"] == str(maxPage):
        nextPageButton.configure(state=DISABLED)


def previousPage_Expanses(unit, expanseCategory, date):
    nextPageButton.configure(state=NORMAL)
    currentPage["text"] = str(int(currentPage["text"]) - 1)
    expanseExpand("", expanseCategory, unit, date, False)
    if currentPage["text"] == "1":
        previousPageButton.configure(state=DISABLED)


def nextPage_Expanses(unit, expanseCategory, date, maxPage):
    previousPageButton.config(state=NORMAL)
    currentPage["text"] = str(int(currentPage["text"]) + 1)
    expanseExpand("", expanseCategory, unit, date, False)
    if currentPage["text"] == str(maxPage):
        nextPageButton.configure(state=DISABLED)


uniqueCategories = []

mainBlock = ttk.Frame(mainPage, height=300, width=500)
mainBlock.pack(pady=20)

datePickerFrame = ttk.Frame(mainBlock, height=50, width=400)
datePickerFrame.pack(expand=1, side=TOP)

dayLabel = ttk.Label(datePickerFrame, text="День", bootstyle=LIGHT, font=(font, 11), cursor="hand2")
dayLabel.bind("<Button-1>", lambda x="": datePick(x, "day", False))
dayLabel.grid(row=0, column=0, padx=10)
dayLine = ttk.Frame(datePickerFrame, bootstyle=SUCCESS, width=45, height=3)

weekLabel = ttk.Label(datePickerFrame, text="Неделя", bootstyle=LIGHT, font=(font, 11), cursor="hand2")
weekLabel.bind("<Button-1>", lambda x="": datePick(x, "week", False))
weekLabel.grid(row=0, column=1, padx=10)
weekLine = ttk.Frame(datePickerFrame, bootstyle=SUCCESS, width=65, height=3)

monthLabel = ttk.Label(datePickerFrame, text="Месяц", bootstyle=LIGHT, font=(font, 11), cursor="hand2")
monthLabel.bind("<Button-1>", lambda x="": datePick(x, "month", False))
monthLabel.grid(row=0, column=2, padx=10)
monthLine = ttk.Frame(datePickerFrame, bootstyle=SUCCESS, width=55, height=3)

yearLabel = ttk.Label(datePickerFrame, text="Год", bootstyle=LIGHT, font=(font, 11), cursor="hand2")
yearLabel.bind("<Button-1>", lambda x="": datePick(x, "year", False))
yearLabel.grid(row=0, column=3, padx=10)
yearLine = ttk.Frame(datePickerFrame, bootstyle=SUCCESS, width=35, height=3)

periodLabel = ttk.Label(datePickerFrame, text="Период", bootstyle=LIGHT, font=(font, 11), cursor="hand2")
periodLabel.bind("<Button-1>", lambda x="": datePick(x, "period", True))
periodLabel.grid(row=0, column=4, padx=10)
periodLine = ttk.Frame(datePickerFrame, bootstyle=SUCCESS, width=65, height=3)

currentDateLabel = ttk.Label(mainBlock, text="", font=(font, 12), foreground="#aaaaaa")
currentDateLabel.pack(side=TOP, pady=(15, 0))

diagramFrame = ttk.Frame(mainBlock)
diagramFrame.pack(side=BOTTOM)

diagramLabel = ttk.Label(diagramFrame)
diagramLabel.pack()

subBlock = ttk.Frame(mainPage)
subBlock.pack(side=TOP)

toolsFrame = ttk.Frame(subBlock)
toolsFrame.pack(side=TOP, fill=X)

navigationFrame = ttk.Frame(toolsFrame)
navigationFrame.pack(anchor=NW, side=RIGHT)
goBackButton = ttk.Button(toolsFrame, text="Назад", bootstyle=[DANGER])

previousPageButton = ttk.Button(navigationFrame, text="<", bootstyle=[LIGHT, OUTLINE], state=DISABLED,
                                command=lambda x="": previousPage_Categories("week"))
previousPageButton.grid(row=0, column=1, sticky=NE, padx=(0, 15), pady=(0, 15))

currentPage = ttk.Label(navigationFrame, text="1", font=(font, 15), bootstyle=LIGHT)
currentPage.grid(row=0, column=2, sticky=NE)

nextPageButton = ttk.Button(navigationFrame, text=">", bootstyle=[LIGHT, OUTLINE],
                            command=lambda x="": nextPage_Categories("week", 1), state=DISABLED)
nextPageButton.grid(row=0, column=3, sticky=NE, padx=(15, 0))

expansesFrame = ttk.Frame(subBlock)
expansesFrame.pack(side=BOTTOM)

expansesInCategoryFrame = ttk.Frame(subBlock)
datePick("", "week", False)


def downloadAsCSV():
    path = filedialog.asksaveasfilename(initialfile="expanses.csv", defaultextension=".csv")
    if path == "":
        return 0
    with open("JSON_files/spending.json", "r") as json_file:
        allExpanses = json.load(json_file)
    with open(path, "w", newline='') as csv_file:
        data = [["Категория", "Стоимость", "Дата", "Комментарий"]]
        date2 = [["Категория", "Сумма"]]
        uniqueCategories_CSV = []
        for expanse in allExpanses:
            data.append([expanse["category"], expanse["price"], expanse["date"], expanse["comment"]])

            if not expanse["category"] in uniqueCategories_CSV:
                uniqueCategories_CSV.append(expanse["category"])
        for i in range(len(uniqueCategories_CSV)):
            uniqueCategories_CSV[i] = [uniqueCategories_CSV[i], 0]
        for category in uniqueCategories_CSV:
            for expanse in allExpanses:
                if expanse["category"] == category[0]:
                    category[1] += expanse["price"]
        for category in uniqueCategories_CSV:
            date2.append(category)
        write = csv.writer(csv_file)
        write.writerows(data)
        write.writerow("")
        write.writerows(date2)


downloadButton = ttk.Button(mainPage, text="Скачать в CSV", bootstyle=[SECONDARY, OUTLINE], command=downloadAsCSV)
downloadButton.place(x=10, y=10)

## -------------------------------------------------
## Main PAGE
## -------------------------------------------------

root.mainloop()
