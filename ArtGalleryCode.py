from typing import Any
from pymongo import MongoClient
from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.floatlayout import FloatLayout 
from kivy.uix.label import Label 
from kivy.lang import Builder 
from kivy.core.window import Window 
from kivy.uix.button import Button 
from kivy.uix.textinput import TextInput 
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.scrollview import ScrollView 
from datetime import datetime
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp 
from kivy.uix.image import Image 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup 

# Load the kv file
Builder.load_file('RoundedButton.kv')

# Define the RoundedButton class
class RoundedButton(Button):
    pass

# Set the background color
Window.clearcolor = (0.75, 0.75, 0.75, 1)  # RGB values of light gray

# Establish a connection to the MongoDB database
client = MongoClient('localhost', 27017)
db = client['ArtGallery']

##########################################################################################

# Function to retrieve all documents from Artwork Table
def get_all_artworks():
    artworks = db['Artwork'].find({})
    return list(artworks)

# Function to retrieve artworks by criteria
def search_artworks_by_medium(text_input):
    criteria = {
        "$or": []  
    }

    # Iterate over all fields and create individual criteria for each field
    for field in db['Artwork'].find_one().keys():
        if field == "_id" or field == "Image":  # Skip the _id and image field
            continue
        field_criteria = {field: {"$regex": text_input, "$options": "i"}}  # Case-insensitive regex search
        criteria["$or"].append(field_criteria)

    artworks = db['Artwork'].find(criteria)
    return list(artworks)

def get_artwork_by_id(artwork_id):
    # Access the "Artwork" collection
    artworks_collection = db['Artwork']
    # Retrieve the artwork based on the artwork ID
    artwork = artworks_collection.find_one({'ID': artwork_id})
    return artwork

# Function to retrieve all documents from the exhibitions table
def get_all_exhibitions():
    exhibitions = db['Exhibition'].find({})
    return list(exhibitions)

# Function to retrieve all documents from the transactions table
def get_all_transactions():
    transactions = db['Transaction'].find({})
    return list(transactions)

def donothing():
    pass
#-----------------------------------------------------------------------------------------------------#
#---------------------------------------Artwork Collection Start--------------------------------------#
#-----------------------------------------------------------------------------------------------------#

# Code to insert a new artwork
def add_artwork_form(screen_instance):
    screen_instance.clear_widgets()  # Clear the widgets before adding new ones
    screen_instance.background = Image(source='bgimage1.jpg', allow_stretch=True, keep_ratio=False)
    screen_instance.add_widget(screen_instance.background)
    fields = ['Title', 'Artist', 'Medium', 'Dimensions', 'Description', 'Acquisition Date', 'Price', 'Status', 'Tags/Keywords', 'Image']
    for i, field in enumerate(fields):
        label = Label(text=field, color=(0, 0, 0, 1), size_hint=(None, None), size=(200, 30), font_size='25sp', pos_hint={'x': 0.1, 'top': .9 - i * 0.07})
        text_input = TextInput(multiline=False, size_hint=(None, None), size=(900, 30), pos_hint={'x': 0.3, 'top': .9 - i * 0.07})
        screen_instance.add_widget(label)
        screen_instance.add_widget(text_input)
        screen_instance.text_inputs[field] = text_input  # Store the TextInput widget in the dictionary

    submit_btn = RoundedButton(text='Submit', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.15})
    submit_btn.bind(on_release=submit_artwork)
    screen_instance.add_widget(submit_btn)

    back_btn = RoundedButton(text='Back', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.08})
    back_btn.bind(on_release=screen_instance.go_back)
    screen_instance.add_widget(back_btn)

def submit_artwork(instance):
    screen_instance = instance.parent  # Assuming the parent of the button is the screen instance
    artwork = {field: screen_instance.text_inputs[field].text for field in screen_instance.text_inputs}  # Get the text from the TextInput widgets
    db.Artwork.insert_one(artwork)  # Insert the artwork into the MongoDB database
    screen_instance.add_widget(Label(text='Success!', color=(0, 1, 0, 1), size_hint=(None, None), size=(100, 30), font_size='25sp', pos_hint={'x': 0.475, 'top': 0.2}))

# Code to display items in Artwork collection
def display_artworks(screen_instance):
    # Add search by criteria functionality
    medium_input = TextInput(hint_text='Search', size_hint=(1, .1), pos_hint={'top': 1})
    search_btn = RoundedButton(text='Search', size_hint=(1, .1), pos_hint={'top': .9})
    search_btn.bind(on_press=lambda instance: display_artworks_by_criteria(screen_instance, medium_input.text))
    screen_instance.background = Image(source='bgimage1.jpg', allow_stretch=True, keep_ratio=False)
    screen_instance.add_widget(screen_instance.background)

    # Position the search widgets at the top
    screen_instance.add_widget(medium_input)
    screen_instance.add_widget(search_btn)
    # Retrieve data from the mongodb
    artworks = get_all_artworks()

    # Create GridLayout to hold artwork information
    grid_layout = GridLayout(cols=4, spacing=20, padding=[50, 50, 50, 50],size_hint_y=None)
    grid_layout.bind(minimum_height=grid_layout.setter('height'))
    scroll_view = ScrollView(size_hint=(1, None), pos_hint={'top': 0.85}, height=screen_instance.height * 0.75)
    scroll_view.add_widget(grid_layout)
    screen_instance.add_widget(scroll_view)

    # Add artworks to the GridLayout in required format
    for i in range(0, len(artworks), 2):
        artwork_1 = artworks[i]
        artwork_2 = artworks[i + 1] if i + 1 < len(artworks) else None

        formatted_text_1 = ""
        formatted_text_2 = ""

        # First artwork
        if 'Title' in artwork_1:
            formatted_text_1 += f"[size=20][b]{artwork_1['Title']}[/b][/size]\n"
        else:
            formatted_text_1 += "Title: N/A\n"

        if 'Artist' in artwork_1:
            formatted_text_1 += f"[i]{artwork_1['Artist']}[/i]\n"
        else:
            formatted_text_1 += "[i]Artist: N/A[/i]\n"

        if 'Tags' in artwork_1:
            formatted_text_1 += f"Tags: [i]{', '.join(artwork_1['Tags'])}[/i]\n"
        else:
            formatted_text_1 += "[i]Tags: N/A[/i]\n"

        if 'Price' in artwork_1:
            formatted_text_1 += f"Price: ${artwork_1['Price']}\n"
        else:
            formatted_text_1 += "Price: N/A\n"

        if 'Medium' in artwork_1:
            formatted_text_1 += f"Medium: {artwork_1['Medium']}\n"
        else:
            formatted_text_1 += "Medium: N/A\n"

        artwork_label_1 = Label(
            text=formatted_text_1,
            size_hint_y=None,
            height='150dp',
            color=(0, 0, 0, 1),
            halign='center',
            valign='middle',
            markup=True
        )
        grid_layout.add_widget(artwork_label_1)

        # First artwork image
        if 'Image' in artwork_1:
            image_1 = Image(source=artwork_1['Image'], size_hint_y=None, height='150dp')
            grid_layout.add_widget(image_1)
        else:
            noimage = Image(source = 'noimage.jpg',size_hint_y=None, height='150dp')
            grid_layout.add_widget(noimage)

        # Second artwork
        if artwork_2:
            if 'Title' in artwork_2:
                formatted_text_2 += f"[size=20][b]{artwork_2['Title']}[/b][/size]\n"
            else:
                formatted_text_2 += "Title: N/A\n"

            if 'Artist' in artwork_2:
                formatted_text_2 += f"[i]{artwork_2['Artist']}[/i]\n"
            else:
                formatted_text_2 += "[i]Artist: N/A[/i]\n"

            if 'Tags' in artwork_2:
                formatted_text_2 += f"Tags: [i]{', '.join(artwork_2['Tags'])}[/i]\n"
            else:
                formatted_text_2 += "[i]Tags: N/A[/i]\n"

            if 'Price' in artwork_2:
                formatted_text_2 += f"Price: ${artwork_2['Price']}\n"
            else:
                formatted_text_2 += "Price: N/A\n"

            if 'Medium' in artwork_2:
                formatted_text_2 += f"Medium: {artwork_2['Medium']}\n"
            else:
                formatted_text_2 += "Medium: N/A\n"

            artwork_label_2 = Label(
                text=formatted_text_2,
                size_hint_y=None,
                height='150dp',
                color=(0, 0, 0, 1),
                halign='center',
                valign='middle',
                markup=True
            )
            grid_layout.add_widget(artwork_label_2)

            # Second artwork image
            if 'Image' in artwork_2:
                image_2 = Image(source=artwork_2['Image'], size_hint_y=None, height='150dp')
                grid_layout.add_widget(image_2)
            else:
                noimage = Image(source = 'noimage.jpg',size_hint_y=None, height='150dp')
                grid_layout.add_widget(noimage)
        else:
            # Add empty labels if there's no second artwork
            grid_layout.add_widget(Label())
            grid_layout.add_widget(Label())
            grid_layout.add_widget(Label())

    # Add Back button
    back_btn = RoundedButton(text='Back', size_hint=(0.1, .1), size=(10, 40), pos_hint={'center_x': 0.5, 'top': 0.1})
    back_btn.bind(on_release=screen_instance.go_back)
    screen_instance.add_widget(back_btn)

def display_artworks_by_criteria(screen_instance, medium):
    screen_instance.clear_widgets()
    screen_instance.background = Image(source='bgimage1.jpg', allow_stretch=True, keep_ratio=False)
    screen_instance.add_widget(screen_instance.background)
    # Display all artworks by medium
    artworks = search_artworks_by_medium(medium)
    grid_layout = GridLayout(cols=4, spacing=20, padding=[30, 30, 30, 30],size_hint=(None, None))
    scroll_view = ScrollView()
    scroll_view.add_widget(grid_layout)
    screen_instance.add_widget(scroll_view)

    for i in range(0, len(artworks), 2):
        artwork = artworks[i]
        formatted_text_1 = ""
        formatted_text_2 = ""

        # First document
        if 'Title' in artwork:
            formatted_text_1 += f"[size=20][b]{artwork['Title']}[/b][/size]\n"
        else:
            formatted_text_1 += "Title: N/A\n"

        if 'Artist' in artwork:
            formatted_text_1 += f"[i]{artwork['Artist']}[/i]\n"
        else:
            formatted_text_1 += "[i]Artist: N/A[/i]\n"

        if 'Tags' in artwork:
            formatted_text_1 += f"Tags: [i]{', '.join(artwork['Tags'])}[/i]\n"
        else:
            formatted_text_1 += "[i]Tags: N/A[/i]\n"

        if 'Price' in artwork:
            formatted_text_1 += f"Price: ${artwork['Price']}\n"
        else:
            formatted_text_1 += "Price: N/A\n"

        if 'Medium' in artwork:
            formatted_text_1 += f"[b]Medium: {artwork['Medium']}[/b]\n"
        else:
            formatted_text_1 += "Medium: N/A\n"

        artwork_label_1 = Label(
            text=formatted_text_1,
            size_hint=(None, None),
            size=('200dp', '100dp'),
            color=(0, 0, 0, 1),
            halign='center',
            valign='middle',
            markup=True
        )
        grid_layout.add_widget(artwork_label_1)

        # First document image
        if 'Image' in artwork:
            image_1 = Image(source=artwork['Image'], size_hint=(None, None), size=('200dp', '100dp'))
            grid_layout.add_widget(image_1)
        else:
            grid_layout.add_widget(Label())

        # Second document
        if i + 1 < len(artworks):
            artwork = artworks[i + 1]
            if 'Title' in artwork:
                formatted_text_2 += f"[size=20][b]{artwork['Title']}[/b][/size]\n"
            else:
                formatted_text_2 += "Title: N/A\n"

            if 'Artist' in artwork:
                formatted_text_2 += f"[i]{artwork['Artist']}[/i]\n"
            else:
                formatted_text_2 += "[i]Artist: N/A[/i]\n"

            if 'Tags' in artwork:
                formatted_text_2 += f"Tags: [i]{', '.join(artwork['Tags'])}[/i]\n"
            else:
                formatted_text_2 += "[i]Tags: N/A[/i]\n"

            if 'Price' in artwork:
                formatted_text_2 += f"Price: ${artwork['Price']}\n"
            else:
                formatted_text_2 += "Price: N/A\n"

            if 'Medium' in artwork:
                formatted_text_2 += f"[b]Medium: {artwork['Medium']}[/b]\n"
            else:
                formatted_text_2 += "Medium: N/A\n"

            artwork_label_2 = Label(
                text=formatted_text_2,
                size_hint=(None, None),
                size=('200dp', '100dp'),
                color=(0, 0, 0, 1),
                halign='center',
                valign='middle',
                markup=True
            )
            grid_layout.add_widget(artwork_label_2)

        else:
            grid_layout.add_widget(Label())

        # Second document image
        if i + 1 < len(artworks) and 'Image' in artworks[i + 1]:
            image_2 = Image(source=artworks[i + 1]['Image'], size_hint=(None, None), size=('200dp', '100dp'))
            grid_layout.add_widget(image_2)
        else:
            grid_layout.add_widget(Label())

    back_btn = RoundedButton(text='Back')
    back_btn.bind(on_release=screen_instance.go_back)  
    screen_instance.add_widget(back_btn)

# Code to update an item in Artwork collection
def update_artwork_form(screen_instance):
    screen_instance.clear_widgets()  # Clear the widgets before adding new ones
    screen_instance.background = Image(source='bgimage1.jpg', allow_stretch=True, keep_ratio=False)
    screen_instance.add_widget(screen_instance.background)
    # Add Title label and TextInput
    screen_instance.add_widget(Label(text='Title', color=(0, 0, 0, 1), size_hint=(None, None), size=(100, 30), font_size='25sp', pos_hint={'x': 0.1, 'top': 0.9}))
    screen_instance.text_inputs['Title'] = TextInput(multiline=False, size_hint=(None, None), size=(900, 30), pos_hint={'x': 0.3, 'top': 0.9})
    screen_instance.add_widget(screen_instance.text_inputs['Title'])

    # Add Submit button
    submit_btn = RoundedButton(text='Submit', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.15})
    submit_btn.bind(on_release=lambda instance: fetch_artwork(screen_instance))
    screen_instance.add_widget(submit_btn)
    # Add Back button
    back_btn = RoundedButton(text='Back', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.08})
    back_btn.bind(on_release=screen_instance.go_back)
    screen_instance.add_widget(back_btn)

def fetch_artwork(screen_instance):
    title = screen_instance.text_inputs['Title'].text  # Get the title from the TextInput widget
    artwork = db.Artwork.find_one({'Title': title})  # Fetch the artwork from the MongoDB database
    if artwork is not None:
        screen_instance.clear_widgets()
        fields = ['Title', 'Artist', 'Medium', 'Dimensions', 'Description', 'Acquisition_Date', 'Price', 'Status', 'Tags']
        for i, field in enumerate(fields):
            label = Label(text=field, color=(0, 0, 0, 1), size_hint=(None, None), size=(100, 30), font_size='25sp', pos_hint={'x': 0.1, 'top': .9 - i * 0.07})
            text_input = TextInput(multiline=False, text=str(artwork.get(field, '')), size_hint=(None, None), size=(900, 30), pos_hint={'x': 0.3, 'top': .9 - i * 0.07})
            screen_instance.add_widget(label)
            screen_instance.add_widget(text_input)
            screen_instance.text_inputs[field] = text_input

        # Add Update button
        update_btn = RoundedButton(text='Update', size_hint=(1, .2), pos_hint={'center_x': 0.5, 'top': 0.15})
        update_btn.bind(on_release=lambda instance: update_artwork(screen_instance))
        screen_instance.add_widget(update_btn)

        # Add Back button
        back_btn = RoundedButton(text='Back', size_hint=(1, .2), pos_hint={'center_x': 0.5, 'top': 0.08})
        back_btn.bind(on_release=screen_instance.go_back)
        screen_instance.add_widget(back_btn)
    else:
        screen_instance.add_widget(Label(text='No artwork found with the given title.', color=(1, 0, 0, 1)))

def update_artwork(screen_instance):
    artwork = {field: screen_instance.text_inputs[field].text for field in screen_instance.text_inputs}  # Get the text from the TextInput widgets
    db.Artwork.update_one({'Title': artwork['Title']}, {'$set': artwork})  # Update the artwork in the MongoDB database
    screen_instance.add_widget(Label(text='Success!', color=(0, 1, 0, 1), size_hint=(None, None), size=(100, 30), font_size='25sp', pos_hint={'x': 0.475, 'top': 0.2}))


# Code to delete an item from the Artwork collection

def delete_artwork_form(screen_instance):
    screen_instance.clear_widgets()  # Clear the widgets before adding new ones
    screen_instance.background = Image(source='bgimage1.jpg', allow_stretch=True, keep_ratio=False)
    screen_instance.add_widget(screen_instance.background)
    # Add Title label and TextInput
    screen_instance.add_widget(Label(text='Title', color=(0, 0, 0, 1), size_hint=(None, None), size=(100, 30), font_size='25sp', pos_hint={'x': 0.1, 'top': 0.9}))
    screen_instance.text_inputs['Title'] = TextInput(multiline=False, size_hint=(None, None), size=(900, 30), pos_hint={'x': 0.3, 'top': 0.9})
    screen_instance.add_widget(screen_instance.text_inputs['Title'])

    # Add Submit button
    submit_btn = RoundedButton(text='Submit', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.15})
    submit_btn.bind(on_release=lambda instance: confirm_delete_artwork(screen_instance))
    screen_instance.add_widget(submit_btn)

    # Add Back button
    back_btn = RoundedButton(text='Back', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.08})
    back_btn.bind(on_release=screen_instance.go_back)
    screen_instance.add_widget(back_btn)
    
def confirm_delete_artwork(screen_instance):
    title = screen_instance.text_inputs['Title'].text  # Get the title from the TextInput widget
    artwork = db.Artwork.find_one({'Title': title})  # Fetch the artwork from the MongoDB database
    if artwork is not None:
        box = BoxLayout(orientation='vertical')          # Create a confirmation popup
        box.add_widget(Label(text=f'Are you sure you want to delete {title}?'))
        btn_yes = Button(text='Yes')
        btn_yes.bind(on_release=lambda instance: delete_and_confirm_artwork(screen_instance, title))
        btn_no = Button(text='No')
        btn_no.bind(on_release=lambda instance: screen_instance.go_back(instance))
        box.add_widget(btn_yes)
        box.add_widget(btn_no)
        popup = Popup(title='Confirmation', content=box, size_hint=(None, None), size=(400, 400))
        popup.open()
    else:
        screen_instance.add_widget(Label(text='No artwork found with the given title.', color=(1, 0, 0, 1)))

def delete_and_confirm_artwork(screen_instance, title):
    delete_artwork(title)
    screen_instance.clear_widgets()
    screen_instance.add_widget(Label(text=f'Artwork {title} has been deleted.', color=(0, 0, 0, 1)))
    back_btn = RoundedButton(text='Back')
    back_btn.bind(on_release=screen_instance.go_back)
    screen_instance.add_widget(back_btn)

def delete_artwork(title):
    # Delete the artwork from the MongoDB database
    db.Artwork.delete_one({'Title': title})



#-----------------------------------------------------------------------------------------------------#
#--------------------------------------Exhibition Collection Start------------------------------------#
#-----------------------------------------------------------------------------------------------------#

# Code to schedule a new exhibition
def add_exhibition_form(screen_instance):
    screen_instance.clear_widgets()
    screen_instance.background = Image(source='bgimage1.jpg', allow_stretch=True, keep_ratio=False)
    screen_instance.add_widget(screen_instance.background)
    fields = ['Name', 'Description', 'Start Date', 'End Date', 'Curator', 'List of Artwork IDs', 'Gallery Space/Room']
    for i, field in enumerate(fields):
        label = Label(text=field, color=(0, 0, 0, 1), size_hint=(None, None), size=(200, 30), font_size='25sp', pos_hint={'x': 0.1, 'top': .9 - i * 0.07})
        text_input = TextInput(multiline=False, size_hint=(None, None), size=(900, 30), pos_hint={'x': 0.3, 'top': .9 - i * 0.07})
        screen_instance.add_widget(label)
        screen_instance.add_widget(text_input)
        screen_instance.text_inputs[field] = text_input  # Store the TextInput widget in the dictionary

    submit_btn = RoundedButton(text='Submit', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.15})
    submit_btn.bind(on_release=lambda instance: submit_exhibition(screen_instance))
    screen_instance.add_widget(submit_btn)

    back_btn = RoundedButton(text='Back', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.08})
    back_btn.bind(on_release=screen_instance.go_back)
    screen_instance.add_widget(back_btn)

def submit_exhibition(screen_instance):
    exhibition = {field: screen_instance.text_inputs[field].text for field in screen_instance.text_inputs}  # Get the text from the TextInput widgets
    db.Exhibition.insert_one(exhibition)  # Update the exhibition in the MongoDB database
    screen_instance.add_widget(Label(text='Success!', color=(0, 1, 0, 1), size_hint=(None, None), size=(100, 30), font_size='25sp', pos_hint={'x': 0.475, 'top': 0.2}))

# Code to display items in Exhibitions collection
def display_exhibitions(screen_instance):
    exhibitions = get_all_exhibitions()
    screen_instance.clear_widgets()  # Clear the widgets before displaying new ones
    screen_instance.background = Image(source='bgimage1.jpg', allow_stretch=True, keep_ratio=False)
    screen_instance.add_widget(screen_instance.background)
    # Add ScrollView and GridLayout
    scroll_view = ScrollView(size_hint=(None, None), size=(Window.width, Window.height))
    grid_layout = GridLayout(cols=1, spacing=20, padding=[50, 50, 50, 50], size_hint_y=None)
    grid_layout.bind(minimum_height=grid_layout.setter('height'))
    scroll_view.add_widget(grid_layout)
    screen_instance.add_widget(scroll_view)

    for exhibition in exhibitions:
        formatted_text_e = ""

        if 'Name' in exhibition:
            formatted_text_e += f"[size=30][b]{exhibition['Name']}[/b][/size]\n"
        else:
            formatted_text_e += "Name: N/A\n"

        if 'Gallery_Space' in exhibition:
            formatted_text_e += f"[i]{exhibition['Gallery_Space']}[/i]\n"
        else:
            formatted_text_e += "Gallery: N/A\n"

        if 'Description' in exhibition:
            formatted_text_e += f"Description: {exhibition['Description']}\n"
        else:
            formatted_text_e += "Description: N/A\n"

        if 'Start_Date' and 'End_Date' in exhibition:
            formatted_text_e += f"Dates:  {exhibition['Start_Date']} to {exhibition['End_Date']}\n"
        else: 
            formatted_text_e += "Dates: N/A\n"

        if 'Curator' in exhibition:
            formatted_text_e += f"[u]Curator:[/u] {exhibition['Curator']}\n"
        else:
            formatted_text_e += "Curator: N/A\n"

        exhibition_label = Label(text=formatted_text_e, size_hint_y=None, height='150dp', color=(0, 0, 0, 1), halign='center', valign='middle', markup=True)
        grid_layout.add_widget(exhibition_label)

    # Add Back button
    back_btn = RoundedButton(text='Back', size_hint=(1, .1), size=(100, 40), pos_hint={'center_x': 0.5, 'top': 0.1})
    back_btn.bind(on_release=screen_instance.go_back)
    screen_instance.add_widget(back_btn)

# Code to delete an item from the Exhibitions collection
def delete_exhibition(name):
    # Delete the exhibition from the MongoDB database
    db.Exhibition.delete_one({'Name': name})

def confirm_delete_exhibition(screen_instance):
    name = screen_instance.text_inputs['Exhibition Name'].text  # Get the name from the TextInput widget
    exhibition = db.Exhibition.find_one({'Name': name})  # Fetch the exhibition from the MongoDB database
    if exhibition is not None:
        # Create a confirmation popup
        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text=f'Are you sure you want to delete {name}?'))
        btn_yes = Button(text='Yes')
        btn_yes.bind(on_release=lambda instance: delete_and_confirm_exhibition(screen_instance, name))
        btn_no = Button(text='No')
        btn_no.bind(on_release=lambda instance: screen_instance.go_back(instance))
        box.add_widget(btn_yes)
        box.add_widget(btn_no)
        popup = Popup(title='Confirmation', content=box, size_hint=(None, None), size=(400, 400))
        popup.open()
    else:
        screen_instance.add_widget(Label(text='No exhibition found with the given name.', color=(1, 0, 0, 1)))

def delete_and_confirm_exhibition(screen_instance, name):
    delete_exhibition(name)
    screen_instance.clear_widgets()
    screen_instance.add_widget(Label(text=f'Exhibition {name} has been deleted.', color=(0, 0, 0, 1)))
    back_btn = RoundedButton(text='Back')
    back_btn.bind(on_release=screen_instance.go_back)
    screen_instance.add_widget(back_btn)

def delete_exhibition_form(screen_instance):
    screen_instance.clear_widgets()  # Clear the widgets before adding new ones
    screen_instance.background = Image(source='bgimage1.jpg', allow_stretch=True, keep_ratio=False)
    screen_instance.add_widget(screen_instance.background)
    # Add Name label and TextInput
    screen_instance.add_widget(Label(text='Exhibition Name', color=(0, 0, 0, 1), size_hint=(None, None), size=(100, 30), font_size='25sp', pos_hint={'x': 0.1, 'top': 0.9}))
    screen_instance.text_inputs['Exhibition Name'] = TextInput(multiline=False, size_hint=(None, None), size=(900, 30), pos_hint={'x': 0.3, 'top': 0.9})
    screen_instance.add_widget(screen_instance.text_inputs['Exhibition Name'])

    # Add Submit button
    submit_btn = RoundedButton(text='Submit', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.15})
    submit_btn.bind(on_release=lambda instance: confirm_delete_exhibition(screen_instance))
    screen_instance.add_widget(submit_btn)

    # Add Back button
    back_btn = RoundedButton(text='Back', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.08})
    back_btn.bind(on_release=screen_instance.go_back)
    screen_instance.add_widget(back_btn)

# Code to update an item in the Exhibition collection
def update_exhibition_form(screen_instance):
    screen_instance.clear_widgets()  # Clear the widgets before adding new ones
    screen_instance.background = Image(source='bgimage1.jpg', allow_stretch=True, keep_ratio=False)
    screen_instance.add_widget(screen_instance.background)

    # Add Name label and TextInput
    screen_instance.add_widget(Label(text='Name', color=(0, 0, 0, 1), size_hint=(None, None), size=(100, 30), font_size='25sp', pos_hint={'x': 0.1, 'top': 0.9}))
    screen_instance.text_inputs['Name'] = TextInput(multiline=False, size_hint=(None, None), size=(900, 30), pos_hint={'x': 0.3, 'top': 0.9})
    screen_instance.add_widget(screen_instance.text_inputs['Name'])

    # Add Submit button
    submit_btn = RoundedButton(text='Submit', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.15})
    submit_btn.bind(on_release=lambda instance: fetch_exhibition(screen_instance))
    screen_instance.add_widget(submit_btn)

    # Add Back button
    back_btn = RoundedButton(text='Back', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.08})
    back_btn.bind(on_release=screen_instance.go_back)
    screen_instance.add_widget(back_btn)

def fetch_exhibition(screen_instance):
    name = screen_instance.text_inputs['Name'].text  # Get the name from the TextInput widget
    exhibition = db.Exhibition.find_one({'Name': name})  # Fetch the exhibition from the MongoDB database
    if exhibition is not None:
        screen_instance.clear_widgets()
        fields = ['Name', 'Start_Date', 'End_Date', 'Description']
        for i, field in enumerate(fields):
            label = Label(text=field, color=(0, 0, 0, 1), size_hint=(None, None), size=(100, 30), font_size='25sp', pos_hint={'x': 0.1, 'top': .9 - i * 0.07})
            text_input = TextInput(multiline=False, text=str(exhibition.get(field, '')), size_hint=(None, None), size=(900, 30), pos_hint={'x': 0.3, 'top': .9 - i * 0.07})
            screen_instance.add_widget(label)
            screen_instance.add_widget(text_input)
            screen_instance.text_inputs[field] = text_input

        # Add Update button
        update_btn = RoundedButton(text='Update', size_hint=(1, .2), pos_hint={'center_x': 0.5, 'top': 0.15})
        update_btn.bind(on_release=lambda instance: update_exhibition(screen_instance))
        screen_instance.add_widget(update_btn)

        # Add Back button
        back_btn = RoundedButton(text='Back', size_hint=(1, .2), pos_hint={'center_x': 0.5, 'top': 0.08})
        back_btn.bind(on_release=screen_instance.go_back)
        screen_instance.add_widget(back_btn)
    else:
        screen_instance.add_widget(Label(text='No exhibition found with the given name.', color=(1, 0, 0, 1)))

def update_exhibition(screen_instance):
    exhibition = {field: screen_instance.text_inputs[field].text for field in screen_instance.text_inputs}  # Get the text from the TextInput widgets
    db.Exhibition.update_one({'Name': exhibition['Name']}, {'$set': exhibition})  # Update the exhibition in the MongoDB database
    screen_instance.add_widget(Label(text='Success!', color=(0, 1, 0, 1), size_hint=(None, None), size=(100, 30), font_size='25sp', pos_hint={'x': 0.475, 'top': 0.2}))

#-----------------------------------------------------------------------------------------------------#
#-------------------------------------Transaction Collection Start------------------------------------#
#-----------------------------------------------------------------------------------------------------#

# Code to display items in the Transactions collection
def display_transactions(self):
    transactions = get_all_transactions()
    self.background = Image(source='bgimage1.jpg', allow_stretch=True, keep_ratio=False)
    self.add_widget(self.background)

    self.grid_layout = GridLayout(cols=2, spacing=20, padding=[30, 30, 30, 30])
    self.scroll_view = ScrollView()
    self.scroll_view.add_widget(self.grid_layout)
    self.add_widget(self.scroll_view)

    for transaction in transactions:
        # Create a label to display transaction details
        formatted_text_t = f"ID: {transaction['Transaction_ID']} \n"
        formatted_text_t += f"Customer: {transaction['Customer_ID']}\n"
        formatted_text_t += f"Artwork: {transaction['Artwork_IDs']}\n"
        # Parse transaction dates into datetime objects
        transaction_date = datetime.strptime(transaction['Transaction_Date'], '%Y-%m-%d')
        formatted_text_t += f"Transaction Date: {transaction_date.strftime('%B %d, %Y')}\n"  # Format transaction date
        formatted_text_t += f"Payment Method: {transaction['Payment_Method']}\n"
        formatted_text_t += f"Total Amount: {transaction['Total_Amount']}\n"
        formatted_text_t += f"Commission: {transaction['Commission_Generated']}\n"

        transaction_label = Label(text=formatted_text_t, size_hint=(None, None), size=('200dp', '200dp'), color=(0, 0, 0, 1))
        self.grid_layout.add_widget(transaction_label)

        # Display artwork images
        artwork_ids = transaction['Artwork_IDs']
        if isinstance(artwork_ids, list):
            for artwork_id in artwork_ids:
                artwork = get_artwork_by_id(artwork_id)
                if artwork:
                    artwork_image = artwork.get('Image', '')  # Assuming 'Image' field contains base64 encoded image data
                    if artwork_image:
                        image_widget = Image(source=artwork_image, size_hint=(None, None), size=('200dp', '200dp'))
                        self.grid_layout.add_widget(image_widget)
                    else:
                        placeholder_image = Image(source='placeholder_image.png', size_hint=(None, None), size=('200dp', '200dp'))
                        self.grid_layout.add_widget(placeholder_image)
                else:
                    placeholder_image = Image(source='placeholder_image.png', size_hint=(None, None), size=('200dp', '200dp'))
                    self.grid_layout.add_widget(placeholder_image)
        else:
            artwork = get_artwork_by_id(artwork_ids)
            if artwork:
                artwork_image = artwork.get('Image', '')  # Assuming 'Image' field contains base64 encoded image data
                if artwork_image:
                    image_widget = Image(source=artwork_image, size_hint=(None, None), size=('200dp', '200dp'))
                    self.grid_layout.add_widget(image_widget)
                else:
                    placeholder_image = Image(source='placeholder_image.png', size_hint=(None, None), size=('200dp', '200dp'))
                    self.grid_layout.add_widget(placeholder_image)
            else:
                placeholder_image = Image(source='placeholder_image.png', size_hint=(None, None), size=('200dp', '200dp'))
                self.grid_layout.add_widget(placeholder_image)

    back_btn = RoundedButton(text='Back')
    back_btn.bind(on_release=self.go_back)
    self.add_widget(back_btn)

#-----------------------------------------------------------------------------------------------------#
#----------------------------------------Loan Collection Start----------------------------------------#
#-----------------------------------------------------------------------------------------------------#

# Code to insert a new item in the Loan collection
def add_loan_form(screen_instance):
    screen_instance.clear_widgets()
    screen_instance.background = Image(source='bgimage1.jpg', allow_stretch=True, keep_ratio=False)
    screen_instance.add_widget(screen_instance.background)
    fields = ['Loan_ID', 'Artwork_ID', 'Borrower_Name_Institution', 'Start_Date', 'End_Date', 'Loan_Agreement_Details']
    for i, field in enumerate(fields):
        label = Label(text=field, color=(0, 0, 0, 1), size_hint=(None, None), size=(200, 30), font_size='25sp', pos_hint={'x': 0.1, 'top': .9 - i * 0.07})
        text_input = TextInput(multiline=False, size_hint=(None, None), size=(900, 30), pos_hint={'x': 0.3, 'top': .9 - i * 0.07})
        screen_instance.add_widget(label)
        screen_instance.add_widget(text_input)
        screen_instance.text_inputs[field] = text_input  # Store the TextInput widget in the dictionary

    submit_btn = RoundedButton(text='Submit', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.15})
    submit_btn.bind(on_release=lambda instance: submit_loan(screen_instance))
    screen_instance.add_widget(submit_btn)

    back_btn = RoundedButton(text='Back', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.08})
    back_btn.bind(on_release=screen_instance.go_back)
    screen_instance.add_widget(back_btn)

def submit_loan(screen_instance):
    loan_data = {field: screen_instance.text_inputs[field].text for field in screen_instance.text_inputs}  # Get the text from the TextInput widgets
    db['Loan'].insert_one(loan_data)  # Insert the loan data into the MongoDB database
    screen_instance.clear_widgets()
    screen_instance.add_widget(Label(text='Loan added successfully.', color=(0, 0, 0, 1)))
    back_btn = RoundedButton(text='Back')
    back_btn.bind(on_release=screen_instance.go_back)
    screen_instance.add_widget(back_btn)

# Code to display items in the Loan collection
def display_loans(self):
    loans = list(db['Loan'].find({}))  # Convert cursor to list

    self.clear_widgets()  # Clear the widgets before displaying new ones
    self.background = Image(source='bgimage1.jpg', allow_stretch=True, keep_ratio=False)
    self.add_widget(self.background)
    # Add ScrollView and GridLayout
    scroll_view = ScrollView(size_hint=(None, None), size=(Window.width, Window.height))
    grid_layout = GridLayout(cols=1, spacing=20, padding=[50, 50, 50, 50], size_hint_y=None)
    grid_layout.bind(minimum_height=grid_layout.setter('height'))
    scroll_view.add_widget(grid_layout)
    self.add_widget(scroll_view)

    if len(loans) == 0:
        no_loan_label = Label(text='No loans available at the moment.', color=(0, 0, 0, 1), halign='center', valign='middle', markup=True)
        grid_layout.add_widget(no_loan_label)
        return

    for loan in loans:
        formatted_text = ""

        if 'Loan_ID' in loan:
            formatted_text += f"[size=30][b]Loan ID:[/b] {loan['Loan_ID']}[/size]\n"
        else:
            formatted_text += "[size=30][b]Loan ID:[/b] N/A[/size]\n"

        if 'Artwork_ID' in loan:
            formatted_text += f"[i]Artwork ID:[/i] {loan['Artwork_ID']}\n"
        else:
            formatted_text += "[i]Artwork ID:[/i] N/A\n"

        if 'Borrower_Name_Institution' in loan:
            formatted_text += f"[i]Borrower Name/Institution:[/i] {loan['Borrower_Name_Institution']}\n"
        else:
            formatted_text += "[i]Borrower Name/Institution:[/i] N/A\n"

        if 'Start_Date' in loan:
            formatted_text += f"[i]Start Date:[/i] {loan['Start_Date']}\n"
        else:
            formatted_text += "[i]Start Date:[/i] N/A\n"

        if 'End_Date' in loan:
            formatted_text += f"[i]End Date:[/i] {loan['End_Date']}\n"
        else:
            formatted_text += "[i]End Date:[/i] N/A\n"

        if 'Loan_Agreement_Details' in loan:
            formatted_text += f"[i]Loan Agreement Details:[/i] {loan['Loan_Agreement_Details']}\n"
        else:
            formatted_text += "[i]Loan Agreement Details:[/i] N/A\n"

        loan_label = Label(text=formatted_text, size_hint_y=None, height='150dp', color=(0, 0, 0, 1), halign='center', valign='middle', markup=True)
        grid_layout.add_widget(loan_label)

    # Add Back button
    back_btn = RoundedButton(text='Back', size_hint=(1, .1), size=(100, 40), pos_hint={'center_x': 0.5, 'top': 0.1})
    back_btn.bind(on_release=self.go_back)
    self.add_widget(back_btn)

# Code to delete items from the Loan collection
def delete_loan(loan_id):
    # Delete the loan from the MongoDB database
    db['Loan'].delete_one({'Loan_ID': loan_id})

def confirm_delete_loan(screen_instance):
    loan_id = screen_instance.text_inputs['Loan ID'].text  # Get the loan ID from the TextInput widget
    loan = db['Loan'].find_one({'Loan_ID': loan_id})  # Fetch the loan from the MongoDB database
    if loan:
        # Create a confirmation popup
        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text=f'Are you sure you want to delete loan {loan_id}?'))
        btn_yes = Button(text='Yes')
        btn_yes.bind(on_release=lambda instance: delete_and_confirm_loan(screen_instance, loan_id))
        btn_no = Button(text='No')
        btn_no.bind(on_release=lambda instance: screen_instance.go_back(instance))
        box.add_widget(btn_yes)
        box.add_widget(btn_no)
        popup = Popup(title='Confirmation', content=box, size_hint=(None, None), size=(400, 400))
        popup.open()
    else:
        screen_instance.add_widget(Label(text='No loan found with the given loan ID.', color=(1, 0, 0, 1)))

def delete_and_confirm_loan(screen_instance, loan_id):
    delete_loan(loan_id)
    screen_instance.clear_widgets()
    screen_instance.add_widget(Label(text=f'Loan {loan_id} has been deleted.', color=(0, 0, 0, 1)))
    back_btn = RoundedButton(text='Back')
    back_btn.bind(on_release=screen_instance.go_back)
    screen_instance.add_widget(back_btn)

def delete_loan_form(screen_instance):
    screen_instance.clear_widgets()  # Clear the widgets before adding new ones
    screen_instance.background = Image(source='bgimage1.jpg', allow_stretch=True, keep_ratio=False)
    screen_instance.add_widget(screen_instance.background)
    # Add Loan ID label and TextInput
    screen_instance.add_widget(Label(text='Loan ID', color=(0, 0, 0, 1), size_hint=(None, None), size=(100, 30), font_size='25sp', pos_hint={'x': 0.1, 'top': 0.9}))
    screen_instance.text_inputs['Loan ID'] = TextInput(multiline=False, size_hint=(None, None), size=(900, 30), pos_hint={'x': 0.3, 'top': 0.9})
    screen_instance.add_widget(screen_instance.text_inputs['Loan ID'])

    # Add Submit button
    submit_btn = RoundedButton(text='Submit', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.15})
    submit_btn.bind(on_release=lambda instance: confirm_delete_loan(screen_instance))
    screen_instance.add_widget(submit_btn)

    # Add Back button
    back_btn = RoundedButton(text='Back', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.08})
    back_btn.bind(on_release=screen_instance.go_back)
    screen_instance.add_widget(back_btn)

# Code to update items in the Loan collection
def update_loan_form(screen_instance):
    screen_instance.clear_widgets()  # Clear the widgets before adding new ones
    screen_instance.background = Image(source='bgimage1.jpg', allow_stretch=True, keep_ratio=False)
    screen_instance.add_widget(screen_instance.background)
    # Add Loan ID label and TextInput
    screen_instance.add_widget(Label(text='Loan ID', color=(0, 0, 0, 1), size_hint=(None, None), size=(100, 30), font_size='25sp', pos_hint={'x': 0.1, 'top': 0.9}))
    screen_instance.text_inputs['Loan ID'] = TextInput(multiline=False, size_hint=(None, None), size=(900, 30), pos_hint={'x': 0.3, 'top': 0.9})
    screen_instance.add_widget(screen_instance.text_inputs['Loan ID'])

    # Add Submit button
    submit_btn = RoundedButton(text='Submit', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.15})
    submit_btn.bind(on_release=lambda instance: fetch_loan_for_update(screen_instance))
    screen_instance.add_widget(submit_btn)

    # Add Back button
    back_btn = RoundedButton(text='Back', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.08})
    back_btn.bind(on_release=screen_instance.go_back)
    screen_instance.add_widget(back_btn)

def fetch_loan_for_update(screen_instance):
    loan_id = screen_instance.text_inputs['Loan ID'].text  # Get the loan ID from the TextInput widget
    loan = db['Loan'].find_one({'Loan_ID': loan_id})  # Fetch the loan from the MongoDB database
    if loan is not None:
        screen_instance.clear_widgets()
        fields = ['Artwork_ID', 'Borrower_Name_Institution', 'Start_Date', 'End_Date', 'Loan_Agreement_Details']
        for i, field in enumerate(fields):
            label = Label(text=field, color=(0, 0, 0, 1), size_hint=(None, None), size=(100, 30), font_size='25sp', pos_hint={'x': 0.1, 'top': .9 - i * 0.07})
            text_input = TextInput(multiline=False, text=str(loan.get(field, '')), size_hint=(None, None), size=(900, 30), pos_hint={'x': 0.3, 'top': .9 - i * 0.07})
            screen_instance.add_widget(label)
            screen_instance.add_widget(text_input)
            screen_instance.text_inputs[field] = text_input

        # Add Update button
        update_btn = RoundedButton(text='Update', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.15})
        update_btn.bind(on_release=lambda instance: update_loan(screen_instance))
        screen_instance.add_widget(update_btn)

        # Add Back button
        back_btn = RoundedButton(text='Back', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.08})
        back_btn.bind(on_release=screen_instance.go_back)
        screen_instance.add_widget(back_btn)
    else:
        screen_instance.add_widget(Label(text='No loan found with the given loan ID.', color=(1, 0, 0, 1)))

def update_loan(screen_instance):
    # Check if 'Loan ID' exists in text_inputs
    if 'Loan ID' in screen_instance.text_inputs:
        loan_id = screen_instance.text_inputs['Loan ID'].text  # Get the loan ID from the TextInput widget
        loan_data = {field: screen_instance.text_inputs[field].text for field in screen_instance.text_inputs}  # Get the text from the TextInput widgets
        db['Loan'].update_one({'Loan_ID': loan_id}, {'$set': loan_data})  # Update the loan in the MongoDB database
    else:
        # If 'Loan ID' key doesn't exist, handle the error gracefully
        print("Error: 'Loan ID' key not found in text_inputs dictionary.")


#-----------------------------------------------------------------------------------------------------#
#--------------------------------Conservation Collection Start----------------------------------------#
#-----------------------------------------------------------------------------------------------------#

# Code to add a new item to the Conservation collection
def add_conservation_form(screen_instance):
    screen_instance.clear_widgets()
    screen_instance.background = Image(source='bgimage1.jpg', allow_stretch=True, keep_ratio=False)
    screen_instance.add_widget(screen_instance.background)
    fields = ['Artwork_ID', 'Conservation_Date', 'Treatment_Description', 'Images_Documents_of_Conservation_Reports']
    for i, field in enumerate(fields):
        label = Label(text=field, color=(0, 0, 0, 1), size_hint=(None, None), size=(200, 30), font_size='25sp', pos_hint={'x': 0.1, 'top': .9 - i * 0.07})
        text_input = TextInput(multiline=False, size_hint=(None, None), size=(900, 30), pos_hint={'x': 0.3, 'top': .9 - i * 0.07})
        screen_instance.add_widget(label)
        screen_instance.add_widget(text_input)
        screen_instance.text_inputs[field] = text_input  # Store the TextInput widget in the dictionary

    submit_btn = RoundedButton(text='Submit', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.15})
    submit_btn.bind(on_release=lambda instance: submit_conservation(screen_instance))
    screen_instance.add_widget(submit_btn)

    back_btn = RoundedButton(text='Back', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.08})
    back_btn.bind(on_release=screen_instance.go_back)
    screen_instance.add_widget(back_btn)

def submit_conservation(screen_instance):
    conservation_data = {field: screen_instance.text_inputs[field].text for field in screen_instance.text_inputs}
    db['Conservation'].insert_one(conservation_data)
    screen_instance.clear_widgets()
    screen_instance.add_widget(Label(text='Conservation record added successfully.', color=(0, 0, 0, 1)))
    back_btn = RoundedButton(text='Back')
    back_btn.bind(on_release=screen_instance.go_back)
    screen_instance.add_widget(back_btn)

# Code to display items in the Conservation collection
def display_conservation_records(screen_instance):
    conservation_records = db['Conservation'].find({})
    screen_instance.background = Image(source='bgimage1.jpg', allow_stretch=True, keep_ratio=False)
    screen_instance.add_widget(screen_instance.background)
    
    # Create ScrollView and GridLayout
    scroll_view = ScrollView(size_hint=(None, None), size=(Window.width, Window.height))
    grid_layout = GridLayout(cols=1, spacing=20, padding=[30, 30, 30, 30], size_hint_y=None)
    grid_layout.bind(minimum_height=grid_layout.setter('height'))
    scroll_view.add_widget(grid_layout)
    screen_instance.add_widget(scroll_view)

    # Iterate through conservation records and add widgets to the grid layout
    for record in conservation_records:
        formatted_text = ""
        formatted_text += f"[size=20][b]Artwork ID:[/b] {record['Artwork_ID']}[/size]\n"
        if 'Conservation_Date' in record:
            formatted_text += f"[i]Conservation Date:[/i] {record['Conservation_Date']}\n"
        else:
            formatted_text += "[i]Conservation Date:[/i] N/A\n"
        formatted_text += f"[i]Treatment Description:[/i] {record['Treatment_Description']}\n"
        formatted_text += "[i]Images/Documents of Conservation Reports:[/i]\n"
        for image_doc in record['Images_Documents_of_Conservation_Reports']:
            formatted_text += f" - {image_doc}\n"

        record_label = Label(
            text=formatted_text,
            size_hint_y=None,
            height='200dp',
            color=(0, 0, 0, 1),
            halign='center',
            valign='middle',
            markup=True
        )
        grid_layout.add_widget(record_label)

    # Add back button
    back_btn = RoundedButton(text='Back', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.07})
    back_btn.bind(on_release=screen_instance.go_back)
    screen_instance.add_widget(back_btn)

# Code to update an item in the Conservation collection
def update_conservation_form(screen_instance):
    screen_instance.clear_widgets()  # Clear the widgets before adding new ones
    screen_instance.background = Image(source='bgimage1.jpg', allow_stretch=True, keep_ratio=False)
    screen_instance.add_widget(screen_instance.background)
    # Add Artwork ID label and TextInput
    screen_instance.add_widget(Label(text='Artwork ID', color=(0, 0, 0, 1), size_hint=(None, None), size=(200, 30), font_size='25sp', pos_hint={'x': 0.1, 'top': 0.9}))
    screen_instance.text_inputs['Artwork ID'] = TextInput(multiline=False, size_hint=(None, None), size=(900, 30), pos_hint={'x': 0.3, 'top': 0.9})
    screen_instance.add_widget(screen_instance.text_inputs['Artwork ID'])

    # Add Submit button
    submit_btn = RoundedButton(text='Submit', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.15})
    submit_btn.bind(on_release=lambda instance: fetch_conservation_for_update(screen_instance))
    screen_instance.add_widget(submit_btn)

    # Add Back button
    back_btn = RoundedButton(text='Back', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.08})
    back_btn.bind(on_release=screen_instance.go_back)
    screen_instance.add_widget(back_btn)

def fetch_conservation_for_update(screen_instance):
    artwork_id = screen_instance.text_inputs['Artwork ID'].text  # Get the artwork ID from the TextInput widget
    conservation_record = db['Conservation'].find_one({'Artwork_ID': artwork_id})  # Fetch the conservation record from the MongoDB database
    if conservation_record:
        screen_instance.clear_widgets()
        fields = ['Conservation_Date', 'Treatment_Description', 'Images_Documents_of_Conservation_Reports']
        for i, field in enumerate(fields):
            label = Label(text=field, color=(0, 0, 0, 1), size_hint=(None, None), size=(200, 30), font_size='25sp', pos_hint={'x': 0.1, 'top': .9 - i * 0.07})
            text_input = TextInput(multiline=False, text=str(conservation_record.get(field, '')), size_hint=(None, None), size=(900, 30), pos_hint={'x': 0.3, 'top': .9 - i * 0.07})
            screen_instance.add_widget(label)
            screen_instance.add_widget(text_input)
            screen_instance.text_inputs[field] = text_input

        # Add Update button
        update_btn = RoundedButton(text='Update', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.15})
        update_btn.bind(on_release=lambda instance: update_conservation(screen_instance))
        screen_instance.add_widget(update_btn)

        # Add Back button
        back_btn = RoundedButton(text='Back', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'top': 0.08})
        back_btn.bind(on_release=screen_instance.go_back)
        screen_instance.add_widget(back_btn)
    else:
        screen_instance.add_widget(Label(text='No conservation record found with the given artwork ID.', color=(1, 0, 0, 1)))

def update_conservation(screen_instance):
    # Check if 'Artwork ID' exists in text_inputs
    if 'Artwork ID' in screen_instance.text_inputs:
        artwork_id = screen_instance.text_inputs['Artwork ID'].text  # Get the artwork ID from the TextInput widget
        conservation_data = {field: screen_instance.text_inputs[field].text for field in screen_instance.text_inputs}  # Get the text from the TextInput widgets
        db['Conservation'].update_one({'Artwork_ID': artwork_id}, {'$set': conservation_data})  # Update the conservation record in the MongoDB database
    else:
        # If 'Artwork ID' key doesn't exist, handle the error gracefully
        print("Error: 'Artwork ID' key not found in text_inputs dictionary.")

#----------------------------------------------------------------------------------------------#
#--------------------------------User Interface screens----------------------------------------#
#----------------------------------------------------------------------------------------------#

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        # Add a background image
        self.background = Image(source='bgimage1.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)
        # Create a new FloatLayout for the buttons and labels
        self.content = FloatLayout(size_hint=(1, None), pos_hint={'top': 1})
        self.add_widget(self.content)
        self.content.add_widget(Label(text='Art Gallery Management', size_hint=(1.01, 1.1), pos_hint={'top': -2}, bold=True, font_size='50sp', color=(0, 0, 0, 1)))
        # Create a GridLayout with two columns
        layout = GridLayout(cols=2, padding=[600,500,600,600], spacing=20,row_force_default=True,row_default_height=40)
        layout.add_widget(Label(text='Username:', size_hint=(None,None), size=(100, 30), font_size="30sp",font_name="Arial.ttf",color = (0,0,0,1)))
        self.username_input = TextInput(hint_text='Username', multiline=False,size=(60, 30), font_size="20sp",font_name="Arial.ttf")
        layout.add_widget(self.username_input)
        layout.add_widget(Label(text='Password:', size_hint=(None,None), size=(100, 30), font_size="30sp",font_name="Arial.ttf",color = (0,0,0,1)))
        self.password_input = TextInput(hint_text='Password', password=True, multiline=False,size=(60,30), font_size="20sp",font_name="Arial.ttf")
        layout.add_widget(self.password_input)

        # Add login button
        self.login_btn = Button(text='Login', size_hint=(None, None), size=(200, 40))
        self.login_btn.bind(on_release=self.check_credentials)
        layout.add_widget(self.login_btn)

        # Add the GridLayout to the screen
        self.add_widget(layout)

    # Code to check if the login credentials are right
    def check_credentials(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        users_collection = db['User']        # Access the user collection within the database
         # Error message label
        self.error_label = Label(text='', color=(1, 0, 0, 1), size_hint=(1, None), height=30, pos_hint={'top': 0.2})
        self.add_widget(self.error_label)
        
        # Check credentials against the User collection in the database
        user = users_collection.find_one({'Username': username, 'Password': password})
        if user:
            self.manager.current = 'main'
        else:
            self.error_label.text = 'Invalid credentials!'

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.background = Image(source='bgimage1.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)
        # Create a new FloatLayout for the buttons and labels
        self.content = FloatLayout(size_hint=(1, None), pos_hint={'top': 1})
        self.add_widget(self.content)

        self.content.add_widget(Label(text='Art Gallery Management', size_hint=(1.01, 1.1), pos_hint={'top': -0.3}, bold=True, font_size='50sp', color=(0, 0, 0, 1)))
        spacer = BoxLayout(size_hint_y=0.5)
        self.add_widget(spacer)
        # Create a horizontal BoxLayout for the boxes
        box_layout = BoxLayout(orientation='horizontal', size_hint=(1, 1), pos_hint={'center_y': -6.5,'center_x':0.5}, spacing = 20)
        box_names = ['Artworks', 'Exhibitions', 'Transactions','Loans','Conservation']
        self.box_to_page = {name: name for name in box_names}
        box_color = (0.2,0.2,0.2,1)
        for name in box_names:
            box = Button(text=f"{name}", markup=True, font_size=35, color=(1,1,1,1), size_hint=(1, 4), pos_hint={'center_y': 0.5,'center_x':0.5})
            box.background_color = box_color
            box.bind(on_release=self.clear_screen)  # Bind the button release event to the corresponding function
            box_layout.add_widget(box)

        self.text_inputs = {}  # Store the TextInput widgets here
        self.content.add_widget(box_layout)
        logout_button = RoundedButton(text='Log Out', size_hint=(1, 1.1))
        logout_button.bind(on_release=self.logout)
        self.content.add_widget(logout_button)

    def logout(self, instance):
        # Access ScreenManager and switch back to the login screen
        self.parent.parent.current = 'login'

    def clear_screen(self, instance):
        self.content.clear_widgets()
        
        self.current_page = self.box_to_page[instance.text]

        self.content.add_widget(Label(text=f"{instance.text} Management", size_hint=(1, 0.1), pos_hint={'top': -1.1}, bold=True, font_size='50sp', color=(0, 0, 0, 1)))
        operations = ['Add', 'Display', 'Update', 'Delete']
        for i, operation in enumerate(operations):
            btn = RoundedButton(text=operation, pos_hint={'top': -3.2 - i * 0.65}, size_hint=(1, 0.3))
            btn.bind(on_release=self.operation_screen)
            self.content.add_widget(btn)
        back_btn = RoundedButton(text='Back', size_hint=(0.5, 0.1),pos_hint = {'center_x':0.5})
        back_btn.bind(on_release=self.go_back)
        self.content.add_widget(back_btn)

    def operation_screen(self, instance):
        self.clear_widgets()  # Clear the widgets before adding new ones
        if self.current_page == 'Artworks':
            if instance.text == 'Add':
                add_artwork_form(self)
            elif instance.text == 'Display':
                display_artworks(self)
            elif instance.text == 'Update':
                update_artwork_form(self)
            elif instance.text == 'Delete':
                delete_artwork_form(self)
        if self.current_page == 'Exhibitions':
            if instance.text == 'Add':
                add_exhibition_form(self)
            elif instance.text == 'Display':
                display_exhibitions(self)
            elif instance.text == 'Update':
                update_exhibition_form(self)
            elif instance.text == 'Delete':
                delete_exhibition_form(self)
        if self.current_page == 'Transactions':
            if instance.text == 'Display':
                display_transactions(self)
        if self.current_page == 'Loans': 
            if instance.text == 'Display':
                display_loans(self)
            elif instance.text == 'Update':
                update_loan_form(self) 
            elif instance.text == 'Add':
                add_loan_form(self)
            elif instance.text == 'Delete':
                delete_loan_form(self)
        if self.current_page == 'Conservation':
            if instance.text == 'Display':
                display_conservation_records(self)
            elif instance.text == 'Add':
                add_conservation_form(self)
            elif instance.text == 'Update':
                update_conservation_form(self)


#-----------------------------------------------------------------------------------------------------#
#------------------------------------Misc-------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------#
    
    def delete_conservation_form(self):
        self.clear_widgets()
        self.add_widget(Label(text='Artwork ID', color=(0, 0, 0, 1)))
        self.text_inputs['Artwork_ID'] = TextInput(multiline=False)
        self.add_widget(self.text_inputs['Artwork_ID'])
        submit_btn = RoundedButton(text='Submit')
        submit_btn.bind(on_release=self.confirm_delete_conservation)
        self.add_widget(submit_btn)
        back_btn = RoundedButton(text='Back')
        back_btn.bind(on_release=self.go_back)
        self.add_widget(back_btn)

    def confirm_delete_conservation(self, instance):
        artwork_id = self.text_inputs['Artwork_ID'].text
        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text=f'Are you sure you want to delete conservation record for Artwork ID: {artwork_id}?'))
        btn_yes = Button(text='Yes')
        btn_yes.bind(on_release=lambda instance: self.delete_conservation(artwork_id)) 
        btn_no = Button(text='No')
        btn_no.bind(on_release=lambda instance: self.go_back(instance))
        box.add_widget(btn_yes)
        box.add_widget(btn_no)
        confirmation_popup = Popup(title=f'Confirmation', content=box, size_hint=(None, None), size=(400, 400))
        confirmation_popup.bind(on_confirm=lambda instance: self.delete_conservation(artwork_id))
        confirmation_popup.open()

    def delete_conservation(self, artwork_id):
        db['Conservation'].delete_one({'Artwork_ID': artwork_id})
        self.clear_widgets()
        self.add_widget(Label(text=f'Conservation record for Artwork ID {artwork_id} deleted successfully.', color=(0, 0, 0, 1)))
        back_btn = RoundedButton(text='Back')
        back_btn.bind(on_release=self.go_back)
        self.add_widget(back_btn)

    def go_back(self, instance):
        self.clear_widgets()
        self.__init__()


#----------------------------------------------------------------------------------------------#
#-------------------------------------App creation---------------------------------------------#
#----------------------------------------------------------------------------------------------#

class ArtGalleryApp(App):
    def build(self):
        sm = ScreenManager()

        # Create instances of LoginScreen and MainScreen
        login_screen = LoginScreen(name='login')

        # Create a Screen instance to hold MainScreen content
        main_screen_container = Screen(name='main')

        # Create an instance of MainScreen
        main_screen = MainScreen()

        # Add the MainScreen instance to the Screen instance
        main_screen_container.add_widget(main_screen)
        
        # Add screens to ScreenManager
        sm.add_widget(login_screen)
        sm.add_widget(main_screen_container)

        return sm

if __name__ == '__main__':
    ArtGalleryApp().run()