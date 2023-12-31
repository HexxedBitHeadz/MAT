from tkinter import scrolledtext, Listbox, Menu, Button, ttk
import tkinter as tk
import tkinter.messagebox
import random, os

# Creating the window
root = tk.Tk()
root.title("Hexxed BitHeadz - Midjourney Assistant Tool")
root.resizable(False, False)
width = 900
height = 800
root.geometry('{}x{}'.format(width, height))

# Set icon
script_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(script_dir, "HeBi.ico")
root.iconbitmap(icon_path)

# Exit function
def exit_1():
    exit()

# About function
def about():
    tkinter.messagebox.showinfo("About", "This tool is developed and maintained by Hexxed BitHeadz, just a few cyber fanatics exploring the digital world in our own creative ways.  Feel free to reach out to us at info@HexxedBitHeadz.com\n\nCheck our blog and our etsy!\n\nhttps://www.hexxdbitheadz.com/\nhttps://www.etsy.com/shop/HexxedBitHeadz")


listSelections = []

# Make a save function that saves all the selected items to a text file
def save_config():
    # Open a file for writing and create it if it doesn't exist
    f = open(script_dir + "/" + "config.txt", "w+")

    # Get all the selections from the listboxes
    for listBox in listBoxes:
        # Get the selected items
        selections = listBox.curselection()

        # Append the text value selected items to the listSelections
        for selection in selections:
            selected_item = listBox.get(selection)
            listSelections.append(selected_item)
        
            f.write(f"{selected_item} from {listBox.listName}\n")

    # Close the file
    f.close()

    # Make a load function that loads all the selected items from a text file
def load_config():
    # Open a file for reading
    f = open(script_dir + "/" + "config.txt", "r")

    # Read all the lines from the file into an array
    lines = f.readlines()

    # Close the file
    f.close()

    # Clear all the listboxes
    for listBox in listBoxes:
        listBox.selection_clear(0, tk.END)

    # Loop through the lines and select the items in the listboxes
    for line in lines:
        # Split the line by the word "from"
        parts = line.split(" from ")

        # Get the item name from the first part
        item_name = parts[0]

        # Get the listbox name from the second part
        listbox_name = parts[1].strip()

        # Loop through the listboxes and select the item
        for listBox in listBoxes:
            if listBox.listName == listbox_name:
                # Get the index of the item
                index = listBox.get(0, tk.END).index(item_name)

                # Select the item
                listBox.selection_set(index)

    # Copy the selections to the clipboard
    copySelection()


# Creating the menu
menu = Menu(root)
root.config(menu=menu)

tab_parent = ttk.Notebook(root)
tab1 = ttk.Frame(tab_parent)
tab_parent.add(tab1, text="MAT")
tab_parent.pack(expand=1, fill='both')

subm_1 = Menu(menu)
menu.add_cascade(label="File", menu=subm_1)
subm_1.add_command(label="Load", command=load_config)
subm_1.add_command(label="Save", command=save_config)
subm_1.add_command(label="About", command=about)
subm_1.add_command(label="Exit", command=exit_1)


arrayTechniques = ["Aquatint print", "Blacklight paint", "Blueprint", "CinStill 50", "Collotype print", "Holography", "Low-poly", "Monotype print", "Screenprint", "Woodblock print"]
arrayGenres = ["Astropunk", "Atompunk", "Baroque", "Cybergoth fashion", "Cyberpunk", "Deconstructivism", "Glitch art", "Gothic art", "Grimdark", "Necropunk", "Solarpunk"]
arrayTitles = ["Akira", "Ergo Proxy", "The Animatrix", "The Matrix"]
arrayPainters = ["Affandi", "Agostino Arrivabene", "Karol Bak", "Zdzislaw Beksinski", "Saturno Butto", "Leonor Fini", "Callie Fink", "Ernst Fuchs", "H.R. Giger", "Alex Grey", "Peter Gric", "Ryan Hewett"]
arrayIllustrators = ["Rafael Albuquerque", "Yoshitaka Amano", "Chris Bachalo", "Ralph Bakshi", "Benedick Bana", "Noma Bar", "Wayne Barlowe", "Gerald Brom", "Harry Clarke", "Becky Cloonan", "Stanley Donwood", "Philippe Druillet", "Didier Graffet", "Mike Grell", "Carne Griffiths", "Jeffrey Catherine Jones", "Michael Kaluta", "Wadmin Kashin", "Abigal Larson", "Bastien Lecouffe-Deharme", "David Mack", "Jim Mahfood", "Alex Maleev", "Leiji Matsumoto", "Todd McFarlane", "Dave McKean", "Mike Mignola", "Russ Mills", "Peter Mohrbacher", "Katsuhiro Otomo", "Andrew Robinson", "Conrad Roset", "Bart Sears", "Bill Sienkiewicz", "Hajime Sorayama", "Austin Osman Spare", "Arthur Suydam", "Sergio Toppi", "Brian M. Viveros", "Patrick Woodroffe"]
arrayPhotographers = ["Alessio Albi", "Roger  Ballen", "Hans Bellmer", "Annie Brigman", "Vanley Burke", "Robby Cavanaug", "Alvin Langdon Coburn", "Brian Duffy", "Tim Flach", "Stefan Gesell", "Misha Gordin", "Erik Madigan Heck", "Steven Klein", "Nick Knight", "Etienne-Jules Marey", "Meret Oppenheim", "Jan Saudek", "Lorna Simpson", "Mario Sorrenti", "Christophe Staelens", "Solve Sundsbo", "Maurice Tbard", "Mario Testino", "Alex Timmermans", "Aruthur Tress", "Deborah Turbeville", "Brett Walker", "Albert Watson", "Liam Wong", "David Yarrow"]
arrayVarious = ["Refik Anadol", "Tom Bagshaw", "Aleksi Briclot", "Santiago Caruso", "Sandra Chevrier", "Oskar Fischinger", "Jordan Grimmer", "Raoul Hausmann", "Dan Hillier", "Ryoji Ikeda", "Bojan Jevtic", "Ryoichi Kurokawa", "H.P. Lovecract", "Antonio Mora", "Mothmeister", "Patrice Murciano", "Yoh Nagao", "Mimmo Rotella", "Dziga Vertov", "Catrin Welz-Stein"]
arraySculptors = ["Louise Bougeois", "Alberto Giacometti", "Antony Gormley", "Theo Jansen", "Ellen Jewett", "Brian Jungen", "Kris Kuksi", "Gaston Lachaise", "Augusta Savage", "Chiharu Shiota", "Stanislaw Szukalski", "teamlab"]
arrayFashionDesigners = ["Ozwald sBoateng", "Alexander McQueen", "Thierry Mugler", "Nigo", "Rick Owens", "Guo Pei", "Riccardo Tisci", "Junya Watanabe", "Yohji Yamamoto", "Iris Van Herpen"]
arrayDesigners = ["Michael Bierut", "Alan Fletcher", "Kaws", "Syd Mead", "Bruno Munari", "Erik Nitsche", "Erik Spiekermann", "Wolfgang Weingart", "Tadanori Yokoo"]
arrayStreetArtists = ["Banksy", "C215", "Tristan Eaton", "Shepard Fairey", "Hopare", "Anthony Lister", "ROA", "Tatiana Suarez"]
arrayPrintmakers = ["Ernst Barlach", "Jonathan Barnbrook", "Alfred Kubin", "Tsukioka Yoshitoshi", "Ravi Zupa"]

selected_items = []

# Function to toggle selection state of an item
def toggle_selection(event):
    listbox = event.widget
    selected_index = listbox.nearest(event.y)
    
    if selected_index in selected_items:
        selected_items.remove(selected_index)
        listbox.selection_clear(selected_index)
    else:
        selected_items.append(selected_index)
        listbox.selection_set(selected_index)

# Place canvas as big as window in black
canvas = tk.Canvas(tab1, width=width, height=height, bg="black")
canvas.place(x=0, y=0)

# Make a scrolledtext
scrolledtext1 = scrolledtext.ScrolledText(tab1, width=67, height=4, wrap=tk.WORD)
scrolledtext1.place(x=10, y=10)

# Place blinking green cursor in scrolledtext1
scrolledtext1.focus()

# Make cursor green
scrolledtext1.config(insertbackground="green")

# Make scrolled text background black, with green text
scrolledtext1.config(bg="black", fg="green")

# Make scrolledtext font Arial 16 and bold
scrolledtext1.config(font=("Arial Bold", 16))

# Make a label that displays the arrayTechniques title
labelTechniques = tk.Label(tab1, text="Techniques", font=("Arial Bold", 12))
labelTechniques.place(x=10, y=120)

# Make the label background black, with green text
labelTechniques.config(bg="black", fg="green")

# Make a listbox that displays the arrayTechniques
listboxTechniques = Listbox(tab1, width=20, height=10, background="white", exportselection=0)
listboxTechniques.place(x=10, y=140)
listboxTechniques.listName = "Techniques"  # Set a custom attribute to store the name

# Make the label background black, with green text
listboxTechniques.config(bg="black", fg="green")

# Fill listbox1 with the arrayTechniques and bind toggle_selection function
for item in arrayTechniques:
    listboxTechniques.insert(tk.END, item)
listboxTechniques.bind("<Button-1>", toggle_selection)

# Make a label that displays the arrayGenres title
labelGenres = tk.Label(tab1, text="Genres", font=("Arial Bold", 12))
labelGenres.place(x=150, y=120)

# Make the label background black, with green text
labelGenres.config(bg="black", fg="green")

# Make a listbox that displays the arrayGenres
listboxGenres = Listbox(tab1, width=20, height=10, background="white", exportselection=0)
listboxGenres.place(x=150, y=140)
listboxGenres.listName = "Genres"  # Set a custom attribute to store the name

# Make the label background black, with green text
listboxGenres.config(bg="black", fg="green")

# Fill listbox2 with the arrayGenres
for item in arrayGenres:
    listboxGenres.insert(tk.END, item)
listboxGenres.bind("<Button-1>", toggle_selection)

# Make a label that displays the arrayTitles title
labelTitles = tk.Label(tab1, text="Titles", font=("Arial Bold", 12))
labelTitles.place(x=290, y=120)

# Make the label background black, with green text
labelTitles.config(bg="black", fg="green")

# Make a listbox that displays the arrayTitles
listboxTitles = Listbox(tab1, width=20, height=10, background="white", exportselection=0)
listboxTitles.place(x=290, y=140)
listboxTitles.listName = "Titles"  # Set a custom attribute to store the name

# Make the label background black, with green text
listboxTitles.config(bg="black", fg="green")

# Fill listbox3 with the arrayTitles
for item in arrayTitles:
    listboxTitles.insert(tk.END, item)
listboxTitles.bind("<Button-1>", toggle_selection)

# Make a label that displays the arrayPainters title
labelPainters = tk.Label(tab1, text="Painters", font=("Arial Bold", 12))
labelPainters.place(x=430, y=120)

# Make the label background black, with green text
labelPainters.config(bg="black", fg="green")

# Make a listbox that displays the arrayPainters
listboxPainters = Listbox(tab1, width=20, height=10, background="white", exportselection=0)
listboxPainters.place(x=430, y=140)
listboxPainters.listName = "Painters"  # Set a custom attribute to store the name

# Make the label background black, with green text
listboxPainters.config(bg="black", fg="green")

# Fill listbox4 with the arrayPainters
for item in arrayPainters:
    listboxPainters.insert(tk.END, item)
listboxPainters.bind("<Button-1>", toggle_selection)

# Make a label that displays the arrayIllustrators title
labelIllustrators = tk.Label(tab1, text="Illustrators", font=("Arial Bold", 12))
labelIllustrators.place(x=570, y=120)

# Make the label background black, with green text
labelIllustrators.config(bg="black", fg="green")

# Make a listbox that displays the arrayIllustrators
listboxIllustrators = Listbox(tab1, width=20, height=10, background="white", exportselection=0)
listboxIllustrators.place(x=570, y=140)
listboxIllustrators.listName = "Illustrators"  # Set a custom attribute to store the name

# Make the label background black, with green text
listboxIllustrators.config(bg="black", fg="green")

# Fill listbox5 with the arrayIllustrators
for item in arrayIllustrators:
    listboxIllustrators.insert(tk.END, item)
listboxIllustrators.bind("<Button-1>", toggle_selection)

# Make a label that displays the arrayPhotographers title
labelPhotographers = tk.Label(tab1, text="Photographers", font=("Arial Bold", 12))
labelPhotographers.place(x=710, y=120)

# Make the label background black, with green text
labelPhotographers.config(bg="black", fg="green")

# Make a listbox that displays the arrayPhotographers
listboxPhotographers = Listbox(tab1, width=20, height=10, background="white", exportselection=0)
listboxPhotographers.place(x=710, y=140)
listboxPhotographers.listName = "Photographers"  # Set a custom attribute to store the name

# Make the label background black, with green text
listboxPhotographers.config(bg="black", fg="green")

# Fill listbox6 with the arrayPhotographers
for item in arrayPhotographers:
    listboxPhotographers.insert(tk.END, item)
listboxPhotographers.bind("<Button-1>", toggle_selection)

# Make a label that displays the arrayVarious title
labelVarious = tk.Label(tab1, text="Various", font=("Arial Bold", 12))
labelVarious.place(x=10, y=320)

# Make the label background black, with green text
labelVarious.config(bg="black", fg="green")

# Make a listbox that displays the arrayVarious
listboxVarious = Listbox(tab1, width=20, height=10, background="white", exportselection=0)
listboxVarious.place(x=10, y=340)
listboxVarious.listName = "Various"  # Set a custom attribute to store the name

# Make the label background black, with green text
listboxVarious.config(bg="black", fg="green")

# Fill listbox7 with the arrayVarious
for item in arrayVarious:
    listboxVarious.insert(tk.END, item)
listboxVarious.bind("<Button-1>", toggle_selection)

# Make a label that displays the arraySculptors title
labelSculptors = tk.Label(tab1, text="Sculptors", font=("Arial Bold", 12))
labelSculptors.place(x=150, y=320)

# Make the label background black, with green text
labelSculptors.config(bg="black", fg="green")

# Make a listbox that displays the arraySculptors
listboxSculptors = Listbox(tab1, width=20, height=10, background="white", exportselection=0)
listboxSculptors.place(x=150, y=340)
listboxSculptors.listName = "Sculptors"  # Set a custom attribute to store the name

# Make the label background black, with green text
listboxSculptors.config(bg="black", fg="green")

# Fill listbox8 with the arraySculptors
for item in arraySculptors:
    listboxSculptors.insert(tk.END, item)
listboxSculptors.bind("<Button-1>", toggle_selection)

# Make a label that displays the arrayFashionDesigners title
labelFashionDesigners = tk.Label(tab1, text="Fashion Designers", font=("Arial Bold", 12))
labelFashionDesigners.place(x=280, y=320)

# Make the label background black, with green text 
labelFashionDesigners.config(bg="black", fg="green")

# Make a listbox that displays the arrayDesigners
listboxFashionDesigners = Listbox(tab1, width=20, height=10, background="white", exportselection=0)
listboxFashionDesigners.place(x=290, y=340)
listboxFashionDesigners.listName = "Fashion Designers"  # Set a custom attribute to store the name

# Make the label background black, with green text
listboxFashionDesigners.config(bg="black", fg="green")

# Fill listbox9 with the arrayFashionDesigners
for item in arrayFashionDesigners:
    listboxFashionDesigners.insert(tk.END, item)
listboxFashionDesigners.bind("<Button-1>", toggle_selection)

# Make a label that displays the arrayDesigners title
labelDesigners = tk.Label(tab1, text="Designers", font=("Arial Bold", 12))
labelDesigners.place(x=430, y=320)

# Make the label background black, with green text
labelDesigners.config(bg="black", fg="green")

# Make a listbox that displays the arrayDesigners
listboxDesigners = Listbox(tab1, width=20, height=10, background="white", exportselection=0)
listboxDesigners.place(x=430, y=340)
listboxDesigners.listName = "Designers"  # Set a custom attribute to store the name

# Make the label background black, with green text
listboxDesigners.config(bg="black", fg="green")

# Fill listbox10 with the arrayDesigners
for item in arrayDesigners:
    listboxDesigners.insert(tk.END, item)
listboxDesigners.bind("<Button-1>", toggle_selection)

# Make a label that displays the arrayStreetArtists title
labelStreetArtists = tk.Label(tab1, text="Street Artists", font=("Arial Bold", 12))
labelStreetArtists.place(x=570, y=320)

# Make the label background black, with green text
labelStreetArtists.config(bg="black", fg="green")

# Make a listbox that displays the arrayStreetArtists
listboxStreetArtists = Listbox(tab1, width=20, height=10, background="white", exportselection=0)
listboxStreetArtists.place(x=570, y=340)
listboxStreetArtists.listName = "Street Artists"  # Set a custom attribute to store the name

# Make the label background black, with green text
listboxStreetArtists.config(bg="black", fg="green")

# Fill listbox11 with the arrayStreetArtists
for item in arrayStreetArtists:
    listboxStreetArtists.insert(tk.END, item)
listboxStreetArtists.bind("<Button-1>", toggle_selection)

# Make a label that displays the arrayPrintmakers title
labelPrintmakers = tk.Label(tab1, text="Printmakers", font=("Arial Bold", 12))
labelPrintmakers.place(x=710, y=320)

# Make the label background black, with green text
labelPrintmakers.config(bg="black", fg="green")

# Make a listbox that displays the arrayPrintmakers
listboxPrintmakers = Listbox(tab1, width=20, height=10, background="white", exportselection=0)
listboxPrintmakers.place(x=710, y=340)
listboxPrintmakers.listName = "Printmakers"  # Set a custom attribute to store the name

# Make the label background black, with green text
listboxPrintmakers.config(bg="black", fg="green")

# Fill listbox12 with the arrayPrintmakers
for item in arrayPrintmakers:
    listboxPrintmakers.insert(tk.END, item)
listboxPrintmakers.bind("<Button-1>", toggle_selection)

# Make a variable "listBoxes" that contains all the listboxes
listBoxes = (listboxTechniques, listboxGenres, listboxTitles, listboxPainters, listboxIllustrators, listboxPhotographers, listboxVarious, listboxSculptors, listboxFashionDesigners, listboxDesigners, listboxStreetArtists, listboxPrintmakers)




###################################################



# Make a checkbox for people option
var1 = tk.IntVar()
check1 = tk.Checkbutton(tab1, text="No people", variable=var1, onvalue=1, offvalue=0)
check1.place(x=10, y=525)

# Make a checkbox for tshirt option
var2 = tk.IntVar()
check2 = tk.Checkbutton(tab1, text="Tshirt vector", variable=var2, onvalue=1, offvalue=0)
check2.place(x=100, y=525)

radioMode = tk.IntVar()

# Make two radio buttons to choose between niji or midjourney
radioNiji = tk.Radiobutton(tab1, text="niji", variable=radioMode, value=1)
radioNiji.place(x=10, y=560)
radioMidjourney = tk.Radiobutton(tab1, text="midjourney", variable=radioMode, value=2)
radioMidjourney.place(x=100, y=560)

# Make a radio button for stylize option
radioStylize = tk.IntVar()

radioStylize1 = tk.Radiobutton(tab1, text="stylize 0", variable=radioStylize, value=1, width=8)
radioStylize1.place(x=10, y=590)
radioStylize2 = tk.Radiobutton(tab1, text="stylize 250", variable=radioStylize, value=2, width=8)
radioStylize2.place(x=100, y=590)
radioStylize3 = tk.Radiobutton(tab1, text="stylize 500", variable=radioStylize, value=3, width=8)
radioStylize3.place(x=190, y=590)
radioStylize4 = tk.Radiobutton(tab1, text="stylize 750", variable=radioStylize, value=4, width=8)
radioStylize4.place(x=280, y=590)


# Make a function that selects a random item from every listbox
def randomPick():
    for listBox in listBoxes:
        # Clear previous selections
        listBox.selection_clear(0, tk.END)
        
        # Select a random item
        random_index = random.randint(0, listBox.size()-1)
      
        listBox.selection_set(random_index)
        
    copySelection()


# Make a button that prints all the selected items
buttonCopy = Button(tab1, text="Copy", width=12, bg="brown", fg="white", command=lambda : copySelection())
buttonCopy.place(x=445, y=525)

# Make a button that selects a random item from every listbox
buttonRandom = Button(tab1, text="Random", width=12, bg="brown", fg="white", command=lambda : randomPick())
buttonRandom.place(x=585, y=525)

# Make a button that clears selections an item from every listbox
buttonClear = Button(tab1, text="Clear", width=12, bg="brown", fg="white", command=lambda : clear())
buttonClear.place(x=725, y=525)

# Make a function that clears all listboxes
def clear():
    for listBox in listBoxes:
        listBox.selection_clear(0, tk.END)

text2Copy = ""

# Print all the selected items
def copySelection():

    global labelCopy

    prefixes = {
        listboxTechniques: " Technique",
        listboxGenres: " Genre",
        listboxTitles: " Titles",
        listboxPainters: " Painting",
        listboxIllustrators: " Illustration",
        listboxPhotographers: " Photograph",
        listboxVarious: " Influence",
        listboxSculptors: " Sculpture",
        listboxFashionDesigners: " Fashion Design",
        listboxDesigners: " Design",
        listboxStreetArtists: " Street Art",
        listboxPrintmakers: " Printmake"
    }

# Make a variable "listSelections" that contains all the selected items
    listSelections = []
    for listBox in listBoxes:
        # Get the selected items
        selections = listBox.curselection()
        
        # Get the prefix for this ListBox
        prefix = prefixes.get(listBox, "")

        # Append selected items with prefix to the listSelections
        for selection in selections:
            item_with_prefix = f"{listBox.get(selection)}{prefix}"
            listSelections.append(item_with_prefix)

    global selected_items
    selected_items = []

####

    # Get the text from scrolledtext1
    text = scrolledtext1.get("1.0", tk.END).strip()

    # Initialize text2Copy with the base text
    text2Copy = text

    # Append selected items with prefix to the listSelections
    for selection in listSelections:
        text2Copy += f", {selection}"

    # Add checkbox options if they are selected
    if var1.get() == 1:
        text2Copy += ", --no people, woman, man"
    if var2.get() == 1:
        text2Copy = "tshirt vector, black background, " + text2Copy

    # Append radio button option

    if radioStylize.get() == 1:
        text2Copy += ", 8k, --ar 7:4 --s 0"
    elif radioStylize.get() == 2:
        text2Copy += ", 8k, --ar 7:4 --s 250"
    elif radioStylize.get() == 3:
        text2Copy += ", 8k, --ar 7:4 --s 500"
    elif radioStylize.get() == 4:
        text2Copy += ", 8k, --ar 7:4 --s 750"

    # Append radio button option
    if radioMode.get() == 1:
        text2Copy += " --niji 5"
    elif radioMode.get() == 2:
        text2Copy += " --v 6"


    try:
        # Destroy labelCopy if it exists
        labelCopy.destroy()
    except:
        pass

    # Make a label that displays the text2Copy
    labelCopy = tk.Label(tab1, text=text2Copy, font=("Arial Bold", 12), wraplength=800)
    labelCopy.place(x=10, y=620)

    # Make the label background black, with green text
    labelCopy.config(bg="black", fg="green")

    # Make a label that says "Text copied to clipboard" and times out after 5 seconds
    labelCopied = tk.Label(tab1, text="Text copied to clipboard!", font=("Arial Bold", 12))
    labelCopied.place(x=680, y=720)

    # Make the label background black, with green text
    labelCopied.config(bg="black", fg="yellow")

    # Destroy labelCopied after 5 seconds
    labelCopied.after(3000, lambda: labelCopied.destroy())

    # Copy text2Copy to clipboard
    root.clipboard_clear()
    root.clipboard_append(text2Copy)



root.mainloop()
