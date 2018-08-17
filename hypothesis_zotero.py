import json
import os
from tkinter import *
import h_annot
from pyzotero import zotero

ZOTERO_API_UPDATE_LIMIT = 50

def save_transfer_settings(settings_path):
    """Save the currently entered transfer settings from the application form to 
    settings_path."""
    try:
        with open(settings_path, "w") as outfile:
            settings = {"library_id": libraryid_w.get(),
                        "zot_api_key":zot_api_key_w.get(),
                        "hyp_username":hyp_username_w.get(),
                        "hyp_api_key":hyp_api_key_w.get(),
                        "num2grab":number_to_grab_w.get()}
            json.dump(settings, outfile)
        progress_indicator.set("Transfer settings saved!")
        return True
    except FileNotFoundError:
        try:
            os.mkdir(os.path.split(settings_path)[0])
            save_transfer_settings(settings_path)
        except PermissionError:
            progress_indicator.set("No permission to save to home folder.")
            return False
        
def load_transfer_settings(settings_path):
    """Load the settings used to transfer annotations from Hypothesis into Zotero
    into the application form."""
    try:
        with open(settings_path) as infile:
            settings = json.load(infile)
            libraryid_w.insert(0, settings["library_id"])
            zot_api_key_w.insert(0,settings["zot_api_key"])
            hyp_username_w.insert(0,settings["hyp_username"])
            hyp_api_key_w.insert(0,settings["hyp_api_key"])
            number_to_grab_w.delete(0,END)
            number_to_grab_w.insert(0,settings["num2grab"])
            return True
    except FileNotFoundError:
        return False

    
def format_converted_note(annotation):
    """Format an annotation so that it translates properly into Zotero note markup."""
    annotated_text = extract_exact(annotation)
    annotation_text = annotation["text"]
    return """<p style="color: green; text-align: center;">{}</p>
    <br>
    <p>{}</p>""".format(annotated_text, annotation_text)
    
def extract_exact(annotation):
    try:
        annotation["target"][0]["selector"]
    except KeyError as e:
        print(annotation)
        return "<text not available>"
    for selector in annotation["target"][0]["selector"]:
        try:
            return selector["exact"]
        except KeyError:
            continue
    return None

def extract_note_tags(notes):
    tags = set()
    for note in notes:
        for tag in note['data']['tags']:
            tags.add(tag['tag'])
    return tags

def grab():
    grab_button.config(state=DISABLED)
    progress_indicator.set("In progress...")
    root.update()
    library_id = libraryid_w.get()
    zot_api_key = zot_api_key_w.get()
    hyp_username = hyp_username_w.get()
    hyp_api_key = hyp_api_key_w.get()
    
    zot = zotero.Zotero(library_id, 'user', zot_api_key)

    num2grab = number_to_grab_w.get()
    items = zot.top(limit=num2grab)
    progress_indicator.set("Zotero library downloaded")
    root.update()
    
    for entry_i in enumerate(items):
        progress_indicator.set("Processing notes...({} of {})".format(entry_i[0]+1,len(items)))
        root.update()
        entry = entry_i[1]
        entry_children = zot.children(entry['key'])
        notes = [note for note in entry_children if note['data']['itemType'] == 'note']
        tags = extract_note_tags(notes)
        entry_annotations = json.loads(h_annot.api.search(hyp_api_key,
                                                          url=entry['data']['url'],
                                                          user=hyp_username))["rows"]
        note_imports = []
        for annotation in entry_annotations:
            if annotation["id"] in tags:
                continue
            else:
                template = zot.item_template("note")
                template['tags'] = (annotation['tags'].copy() +
                                    [{"tag": annotation["id"], "type":1}] +
                                    [{"tag": "hyp-annotation", "type":1}])
                template['note'] = format_converted_note(annotation)
                note_imports.append(template)
        #TODO: Fix this so it doesn't break if you have more than 50 annotations on a document
        zot.create_items(note_imports,entry["key"])
    progress_indicator.set("Done!")
    grab_button.config(state=NORMAL)   

root = Tk()
root.title("Zotero Hypothesis Importer")

frame = Frame(root, width=100, height=100)
frame.pack()

# Add widgets to get auth info for API calls
libraryid_label = Label(frame, text="Library ID:")
libraryid_w = Entry(frame, width=25)
zot_api_key_label = Label(frame, text="Zotero API Key:")
zot_api_key_w = Entry(frame, width=25)
hyp_username_label = Label(frame, text="Hypothesis Username:")
hyp_username_w = Entry(frame, width=25)
hyp_api_key_label = Label(frame, text="Hypothesis API Key:")
hyp_api_key_w = Entry(frame, width=25)
number_to_grab_label = Label(frame,text="Grab last N items:")
number_to_grab_w = Entry(frame, width=25)
number_to_grab_w.insert(0,"50")

# Lay out widgets on application window

libraryid_label.grid(row=1)
libraryid_w.grid(row=1,column=1)

zot_api_key_label.grid(row=2)
zot_api_key_w.grid(row=2,column=1)

hyp_username_label.grid(row=3)
hyp_username_w.grid(row=3,column=1)

hyp_api_key_label.grid(row=4)
hyp_api_key_w.grid(row=4,column=1)

number_to_grab_label.grid(row=5)
number_to_grab_w.grid(row=5,column=1)

grab_button = Button(frame, text="Grab", command=grab)
grab_button.grid(row=6)

# Button to save transfer settings
save_button = Button(frame, text="Save Settings",
                     command=lambda: save_transfer_settings(
                         os.path.expanduser("~/.hypzot/transfer_settings.json")
                     ))
save_button.grid(row=6,column=1)

# Add progress indicators
progress_indicator = StringVar()
progress_indicator.set("Waiting...")
grab_zotero_library_label = Label(frame, text="Progress:")
grab_zotero_library_i = Label(frame, textvariable=progress_indicator)

grab_zotero_library_label.grid(row=7)
grab_zotero_library_i.grid(row=7,column=1)

load_transfer_settings(os.path.expanduser("~/.hypzot/transfer_settings.json"))

root.mainloop()
