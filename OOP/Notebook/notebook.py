import datetime 

last_id = 0

class Note:
    """Represent a note in the notebook. Match against a string in searches and store tags for each note."""

    def __init__(self, memo, tags="") -> None:
        "Initialiase a note with memo and optional space-separated tags. Automatically set the note's creation date and a unique id"
        self.memo = memo
        self.tags = tags
        self.creation_date = datetime.date.today()
        global last_id
        last_id +=  1
        self.id = last_id

    def match(self, filter: str) -> bool:
        """
        Determine if this note matches the filter text. Returns True if it matches. False otherwise.
        Search is case sensitivie and matches both text and tags
        """
        return filter in self.memo or filter in self.tags

class Notebook:
    """
    Represents a collection of notes that can be tagged, modified and searched
    """

    def __init__(self) -> None:
        """Initialize a notebook with an empty list"""
        self.notes = []
    
    def new_note(self, memo, tags=""):
        """Create a new note and add it to the list"""
        self.notes.append(Note(memo,tags))
    
    def _find_note(self, note_id):
        """Locate the note with the given id"""
        for note in self.notes:
            if note.id == str(note_id):
                return note
        return None 
    
    def modify_memo(self, note_id, memo):
        """Find the note with given id and change the memo to given value"""
        note = self._find_note(note_id)
        if note:
            note.memo = memo
            return True
        return False
    
    def modify_tags(self, note_id, tags):
        """Find the note with the given id and change its tag to given value"""
        note = self._find_note(note_id)
        if note:
            note.tag = tags
            return True
        return False 

    
    def search(self, filter):
        """Find all notes that match the given filter string"""
        return [note for note in self.notes if note.match(filter)]
