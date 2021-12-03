"""
Programming 1

Project 5: GUI, Address book

This program executes an address book. User can enter data into the address book and
then search through it, edit it or see the entire address book.

Program comes in a ZIP file containing two txt-files:
address_book.txt:           a txt-file to which the contacts are added. This file is also
                            loaded at the beginning of the program and rows are saved to it
                            to make sure user can always access their address book.
                            The file comes with some example addresses, however tester can
                            edit, delete or save more into the address book as they please.

zipcodes_and_cities.txt:    a txt-file which contains almost all zipcodes in Finland. The most
                            recent and best data I was able to find was an Excel at:
                            https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=
                            2ahUKEwjExZ-Y37ftAhW7AhAIHby2CD0QFjABegQIBBAC&url=https%3A%2F%2Fwww.
                            stat.fi%2Fstatic%2Fmedia%2Fuploads%2Ftup%2Fpaavo%2Falueryhmittely_
                            posnro_2015.xlsx&usg=AOvVaw1FNpXgC_wP4EguBDNIIA-c
                            I edited the Excel, formatted it and got a consistent txt-file.
                            This file of course narrowed down the program to only work with
                            addresses in Finland, however to expand the program one would only
                            need to add another txt-file with the same formatting.

Name: Sophie Tötterström
Student ID: 050102822
Email: sophie.totterstrom@tuni.fi
"""

from tkinter import *
import time


class ContactCard:
    """
    This class creates a contact card object,
    which contains data for an individual's contact information.
    """

    def __init__(self, first_name, last_name, address, zip_code, city):
        """
        Define the object's (a person in the address book) parameters:
        :param first_name: person's first name, str
        :param last_name: person's last name, str
        :param address: person's full address, str
        :param zip_code: address zipcode, str
        :param city: the city related to a specific zip code, str

        Class attributes are public on purpose to make them easy to access in the code.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.zip_code = zip_code
        self.city = city


class GUI:
    """
    This class is the implementation of a simple user interface.
    The GUI
    """

    def __init__(self):
        """
        Here we define a lot of elements of the GUI.
        This is full of elements which will be further explained and configured in class methods.
        """

        self.__main_window = Tk()

        # Set window title
        self.__main_window.title("Address Book")

        # Define global attributes for the GUI.
        self.title_font = ("default", 20, 'bold')
        self.content_height = 350
        self.content_width = 450
        self.sidebar_width = 100

        # Initialize the address book itself to be a dict.
        # This dict is the basis of the GUI's data.
        self.__address_book = {}

        # Create a dict of zip codes for city lookup feature of the GUI.
        self.__dict_of_zipcodes_and_cities = {}
        self.read_zip_code_city_file()

        # The GUI is comprised of three pieces. The sidebar, the title, and the content frame.
        self.__sidebar = Frame(self.__main_window)
        self.__title_frame = Frame(self.__main_window)
        self.__content_frame = Frame(self.__main_window)

        # sticky=NSEW makes the frame extend to every edge (N=north, S=South,.. etc).
        self.__sidebar.grid(row=0, column=0, rowspan=2, sticky=NSEW)
        self.__title_frame.grid(row=0, column=1, sticky=NSEW)
        self.__content_frame.grid(row=1, column=1, sticky=NSEW)

        # Define row and column constraints for the pieces.

        # Rows and columns do not resize by default. To allow them to resize,
        # the rowconfigure or columnconfigure weight= needs to be set to 1.
        # The minimum window size is defined using minsize=.
        self.__main_window.rowconfigure(1, weight=1, minsize=self.content_height)
        self.__main_window.columnconfigure(1, weight=1, minsize=self.content_width)

        # Here, all of the buttons in the sidebar are allowed to stretch vertically, but not horizontally.
        self.__sidebar.rowconfigure(0, weight=1)
        self.__sidebar.rowconfigure(1, weight=1)
        self.__sidebar.rowconfigure(2, weight=1)
        self.__sidebar.rowconfigure(3, weight=1)
        self.__sidebar.columnconfigure(0, minsize=self.sidebar_width)

        # The content frame has stretching enabled vertically and horizontally.
        self.__content_frame.rowconfigure(0, weight=1)
        self.__content_frame.columnconfigure(0, weight=1)

        # **************************
        # *  Initializing Objects  *
        # **************************

        # ** TITLE FRAME OBJECTS **

        # Label object for title is initialized here in the title_frame. The font is set using font=.
        self.__title_label = Label(self.__title_frame, font=self.title_font)
        # Since the label is the only object in title_frame, no layout needs to be specified besides .pack().
        self.__title_label.pack()

        # ** SIDEBAR FRAME OBJECTS **

        # Button objects can be defined with a text label, a height, and connected to a command.
        # The commands refresh the content_frame thus user is switching through "pages".
        self.__add_to_address_book_page_button = Button(self.__sidebar,
                                                        text="Add Contact Here",
                                                        height=4,
                                                        command=self.add_to_address_book_page)

        self.__print_address_book_button = Button(self.__sidebar,
                                                  text="Show Address Book",
                                                  height=4,
                                                  command=self.address_book_page)

        self.__search_button = Button(self.__sidebar,
                                      text="Search Address Book",
                                      height=4,
                                      command=self.search_page)

        self.__quit_button = Button(self.__sidebar,
                                    text="Quit",
                                    height=4,
                                    command=self.stop)

        # Sidebar buttons are in column=0 with sticky used to stretch the button to the edges of the grid.
        # Row= is used to set the vertical layout.
        self.__add_to_address_book_page_button.grid(row=0, column=0, sticky=NSEW)
        self.__print_address_book_button.grid(row=1, column=0, sticky=NSEW)
        self.__search_button.grid(row=2, column=0, sticky=NSEW)
        self.__quit_button.grid(row=3, column=0, sticky=NSEW)

        # ** ADD ADDRESS PAGE OBJECTS **

        # Initialize the content frame.
        self.__add_address_frame = Frame(self.__content_frame)

        # User's input data labels and entry-fields.
        self.__add_address_first_name_label = Label(self.__add_address_frame, text="First Name:")
        self.__add_address_first_name_data = Entry(self.__add_address_frame)

        self.__add_address_last_name_label = Label(self.__add_address_frame, text="Last Name:")
        self.__add_address_last_name_data = Entry(self.__add_address_frame)

        self.__add_address_street_address_label = Label(self.__add_address_frame, text="Street Address:"
                                                                                       "\n(and address details)")
        self.__add_address_street_address_data = Entry(self.__add_address_frame)

        self.__add_address_zip_code_label = Label(self.__add_address_frame, text="Zip Code:")
        self.__add_address_zip_code_data = Entry(self.__add_address_frame)

        # The error message label is used for communicating with the user. The text
        # is first set to an empty string and will be configured to have specific messages.
        self.__add_address_error_message_label = Label(self.__add_address_frame, text="")

        # Action buttons are set in a separate frame to help the interface to stay consistent
        # if the user resizes the main window.
        self.__button_frame = Frame(self.__add_address_frame)

        self.__add_address_add_button = Button(self.__button_frame,
                                               text="Add Contact",
                                               command=self.add_to_address_book,
                                               height=3,
                                               width=15
                                               )
        self.__add_address_clear_button = Button(self.__button_frame,
                                                 text="Clear",
                                                 command=self.add_address_reset_fields,
                                                 height=3,
                                                 width=15
                                                 )

        # ** ADDRESS BOOK PAGE OBJECTS **

        #
        self.number_of_addresses = 0
        self.number_of_pages = 0

        # Initialize the content frame.
        self.__address_book_frame = Frame(self.__content_frame)

        self.__current_page = 1
        self.page_size = 3

        # Address Book Navigation Objects

        self.__contact_frame = Frame()
        self.__name_label = Label(self.__contact_frame)
        self.__address_label = Label(self.__contact_frame)
        self.__zip_and_city_label = Label(self.__contact_frame)

        self.__address_book_button_frame = Frame(self.__address_book_frame)

        self.__address_results_frame = Frame(self.__address_book_frame)

        self.__address_book_back_page_button = Button(self.__address_book_button_frame,
                                                      text="<",
                                                      command=self.back_button,
                                                      height=2,
                                                      width=10
                                                      )
        self.__address_book_front_page_button = Button(self.__address_book_button_frame,
                                                       text=">",
                                                       command=self.front_button,
                                                       height=2,
                                                       width=10
                                                       )
        self.__address_book_page_label = Label(self.__address_book_button_frame)

        self.__address_book_error_message = Label(self.__address_book_frame)

        # **  SEARCH PAGE OBJECTS  **

        # Initialize the content frame.
        self.__search_frame = Frame(self.__content_frame)

        # Search Field Objects
        self.__search_name_label = Label(self.__search_frame, text="Enter Name:\n(First and Last name)")
        self.__search_name_data = Entry(self.__search_frame)
        self.__search_name_button = Button(self.__search_frame,
                                           text="Search",
                                           command=self.search)
        self.__search_error_message = Label(self.__search_frame, text=None)

        # Action Buttons
        self.__search_button_frame = Frame(self.__search_frame)

        self.__search_edit_button = Button(self.__search_button_frame,
                                           text="Edit",
                                           command=self.edit,
                                           height=3,
                                           width=15
                                           )
        self.__search_delete_button = Button(self.__search_button_frame,
                                             text="Delete",
                                             command=self.delete,
                                             height=3,
                                             width=15
                                             )

        # ** EDIT ADDRESS PAGE OBJECTS **
        self.edit_contact_object = None

        # Content Frame
        self.__edit_address_frame = Frame(self.__content_frame)

        # Form Data
        self.__edit_address_first_name_label = Label(self.__edit_address_frame, text="First Name:")
        self.__edit_address_first_name_data = Entry(self.__edit_address_frame)

        self.__edit_address_last_name_label = Label(self.__edit_address_frame, text="Last Name:")
        self.__edit_address_last_name_data = Entry(self.__edit_address_frame)

        self.__edit_address_street_address_label = Label(self.__edit_address_frame, text="Street Address:"
                                                                                         "\n(and address details)")
        self.__edit_address_street_address_data = Entry(self.__edit_address_frame)

        self.__edit_address_zip_code_label = Label(self.__edit_address_frame, text="Zip Code:")
        self.__edit_address_zip_code_data = Entry(self.__edit_address_frame)

        self.__edit_address_error_message_label = Label(self.__edit_address_frame, text="")

        # Action Buttons
        self.__edit_button_frame = Frame(self.__edit_address_frame)

        self.__edit_address_save_button = Button(self.__edit_button_frame,
                                                 text="Save",
                                                 command=self.edit_address,
                                                 height=3,
                                                 width=15
                                                 )
        self.__edit_address_clear_button = Button(self.__edit_button_frame,
                                                  text="Clear",
                                                  command=self.edit_address_reset_fields,
                                                  height=3,
                                                  width=15
                                                  )

        # Start the program on the Add Address Page.
        self.add_to_address_book_page()

    # ********************
    # * ADD ADDRESS PAGE *
    # ********************

    def add_to_address_book_page(self):
        """
        This method opens the page in which a user can add a contact into the address book.
        """

        # reset_page hides the other content frames and sets this content frame in the grid.
        self.reset_page(self.__add_address_frame)

        # Change the title to the corresponding page name.
        self.__title_label.configure(text="Add Contact\n")

        # Only column 1 and row 4 are allowed to stretch.
        # Column 1 contains the Entry fields, row 4 contains the feedback message to the user.
        self.__add_address_frame.columnconfigure(1, weight=1)
        self.__add_address_frame.rowconfigure(4, weight=1)

        # The form fields are arranged vertically, with each row containing a description label and
        # a corresponding entry field.
        self.__add_address_first_name_label.grid(row=0, column=0, sticky=NSEW)
        self.__add_address_first_name_data.grid(row=0, column=1, sticky=NSEW)

        self.__add_address_last_name_label.grid(row=1, column=0, sticky=NSEW)
        self.__add_address_last_name_data.grid(row=1, column=1, sticky=NSEW)

        self.__add_address_street_address_label.grid(row=2, column=0, sticky=NSEW)
        self.__add_address_street_address_data.grid(row=2, column=1, sticky=NSEW)

        self.__add_address_zip_code_label.grid(row=3, column=0, sticky=NSEW)
        self.__add_address_zip_code_data.grid(row=3, column=1, sticky=NSEW)

        self.__add_address_error_message_label.grid(row=4, columnspan=2, sticky=NSEW)

        # We create a separate frame for the two buttons at the bottom of the page
        # to make sure the two buttons in the frame expand in a similar ratio.
        self.__button_frame.grid(row=5, columnspan=2, sticky=NSEW)

        # To make the buttons expand and fill the bottom of the content frame, expand= and fill= are used.
        self.__add_address_clear_button.pack(side='right', expand=True, fill=BOTH)
        self.__add_address_add_button.pack(side='left', expand=True, fill=BOTH)

    def add_to_address_book(self):
        """
        Button action for when the "Add Contact" button is pressed on the "Add Contact Here" page
        """

        # Create dictionary from the form input data to send to the input checker.
        form_input = {"first_name": self.__add_address_first_name_data.get(),
                      "last_name": self.__add_address_last_name_data.get(),
                      "address": self.__add_address_street_address_data.get(),
                      "zip_code": self.__add_address_zip_code_data.get()}

        # Get a contact card object back from the input checker.
        contact_card = self.input_checker(form_input)

        if contact_card is not None:
            # Construct a key from the object. Use lower() for key consistency and user-friendly search.
            key = f"{contact_card.last_name},{contact_card.first_name}".lower()

            if key not in self.__address_book:
                # Add contact card to the address book.
                self.__address_book[key] = contact_card

                # Save addresses to text file.
                self.save_address_book()

                # Display status to user.
                new_label = Label(self.__add_address_frame, text="Contact was added to address book!", fg="green")
                new_label.grid(row=4, columnspan=2)

                # Clear the entry fields.
                self.add_address_reset_fields()

            else:
                # Notify user if a contact already exists in the address book.
                self.__add_address_error_message_label.configure(text="Contact already exists!", fg="red")

    def input_checker(self, form_input):
        """
        This method verifies the entered data is not an empty string and verifies the zip code is valid.
        :return: Returns a contact card object if the input data is valid, otherwise returns None
        """

        # As all the entry fields are compulsory in order for the program to function
        # correctly, it doesn't really matter in what order we check input. Thus we will
        # begin at the first entry field: the first name:

        first_name = form_input["first_name"]
        if first_name == '':
            self.__add_address_error_message_label.configure(text="Invalid first name!", fg="red")
            return None

        last_name = form_input["last_name"]
        if last_name == '':
            self.__add_address_error_message_label.configure(text="Invalid last name!", fg="red")
            return None

        address = form_input["address"]
        if address == '':
            self.__add_address_error_message_label.configure(text="Invalid address!", fg="red")
            return None

        zip_code = form_input["zip_code"]
        # Instead of only checking for empty string, the zip code field is checked for validity.
        if zip_code not in self.__dict_of_zipcodes_and_cities:
            self.__add_address_error_message_label.configure(text="Unknown zipcode!", fg="red")
            return None

        # If the entered fields are valid, the city is looked up
        city = self.__dict_of_zipcodes_and_cities[zip_code]

        # and a contact card object is created and returned
        contact_card = ContactCard(first_name, last_name, address, zip_code, city)
        return contact_card

    def add_address_reset_fields(self):
        """
        Clears the Entry fields on the add_address page and resets the error message label to an empty string
        """
        self.__add_address_first_name_data.delete(0, 'end')
        self.__add_address_last_name_data.delete(0, 'end')
        self.__add_address_street_address_data.delete(0, 'end')
        self.__add_address_zip_code_data.delete(0, 'end')
        self.__add_address_error_message_label.configure(text="")

    # *********************
    # * ADDRESS BOOK PAGE *
    # *********************

    def address_book_page(self):
        """
        This method opens the page in which the address book contents are displayed and places the
        objects on the page in the grid.
        """
        # Clear previous objects that have been placed.
        self.reset_page(self.__address_book_frame)

        # Set corresponding title for page.
        self.__title_label.configure(text="Address Book\n")

        # Allow the content to stretch horizontally and vertically.
        self.__address_book_frame.columnconfigure(0, weight=1)
        self.__address_book_frame.rowconfigure(1, weight=1)

        # Orient the objects in a vertical stack.
        self.__address_results_frame.grid(row=1, sticky=NSEW)
        self.__address_book_error_message.grid(row=2, sticky=NSEW)
        self.__address_book_button_frame.grid(row=3, sticky=NSEW)

        # Place the button objects in a horizontal row.
        self.__address_book_back_page_button.grid(row=0, column=0, sticky=W)
        self.__address_book_page_label.grid(row=0, column=1, sticky=NSEW)
        self.__address_book_front_page_button.grid(row=0, column=2, sticky=E)

        # Allow button frame to stretch in the middle, but keep the buttons the same size.
        self.__address_book_button_frame.columnconfigure(1, weight=1)

        # Label the page number.
        self.__address_book_page_label.configure(text=self.__current_page)

        # Find the number of addresses in the book.
        self.number_of_addresses = len(self.__address_book)

        # Calculate the number of pages.
        last_page = self.number_of_addresses % self.page_size
        self.number_of_pages = self.number_of_addresses // self.page_size

        if last_page != 0:
            self.number_of_pages += 1

        # Reset error message text.
        self.__address_book_error_message.configure(text="")

        # Create a list of the contact card objects.
        contacts_list = []
        for key in sorted(self.__address_book):
            contact = self.__address_book[key]
            contacts_list.append(contact)

        # Add empty contact cards to the end of the list to make a
        # number of contact cards divisible by the page size
        for j in range(self.page_size-last_page):
            contact_card = ContactCard("", "", "", "", "")
            contacts_list.append(contact_card)

        # Display contact cards in frames, handled by print_one_address.
        for i in range(self.page_size):
            # Calculate the index of the list based on the current page, page size, and index.
            index = (self.__current_page - 1) * self.page_size + i
            contact = contacts_list[index]
            self.print_one_address(contact, i, self.__address_results_frame)

    def back_button(self):
        """
        Navigates back one page or displays a message saying the beginning has been reached
        """
        if self.__current_page > 1:
            # Reduce current page to go back thus creating the functionality of the button.
            self.__current_page -= 1
            self.address_book_page()
        else:
            self.__address_book_error_message.configure(text="At beginning of pages")

    def front_button(self):
        """
        Navigates forward one page or displays a message saying the end has been reached
        """
        if self.__current_page < self.number_of_pages:

            self.__current_page += 1
            self.address_book_page()
        else:
            self.__address_book_error_message.configure(text="At end of pages")

    def print_one_address(self, contact, row_number, frame):
        """
        Creates a frame containing the contact information of a single contact,
        and places it at at a specific row in the frame object
        :param contact: ContactCard object to be displayed
        :param row_number: Row to place the created frame
        :param frame: Frame object to contain contact cards
        """

        # Create a frame to contain the address information.
        self.__contact_frame = Frame(frame, width=400, height=100, padx=10, pady=10)
        self.__contact_frame.grid(row=row_number, columnspan=2, sticky=NSEW)
        self.__contact_frame.columnconfigure(0, weight=1)

        # Create strings to place in the frame.
        name = f"{contact.first_name} {contact.last_name}"
        address = contact.address
        zip_and_city = f"{contact.zip_code} {contact.city}"

        # Create label objects for the strings using anchor=W to have the text pushed to the left.
        self.__name_label = Label(self.__contact_frame, text=name, anchor=W)
        self.__address_label = Label(self.__contact_frame, text=address, anchor=W)
        self.__zip_and_city_label = Label(self.__contact_frame, text=zip_and_city, anchor=W)

        # Orient the labels vertically.
        self.__name_label.grid(row=0, column=0, sticky=NSEW)
        self.__address_label.grid(row=1, column=0, sticky=NSEW)
        self.__zip_and_city_label.grid(row=2, column=0, sticky=NSEW)

    # *********************
    # *    SEARCH PAGE    *
    # *********************

    def search_page(self):
        """
        This method opens the search page by placing the objects in the grid.
        """
        # Clear previous objects that have been placed.
        self.reset_page(self.__search_frame)

        # Set the correct title.
        self.__title_label.configure(text="Search Address Book\n")

        # Allow window to stretch horizontally in column 1 and horizontally in row 1.
        self.__search_frame.columnconfigure(1, weight=1)
        self.__search_frame.rowconfigure(1, weight=1)

        # Search bar has a horizontal layout in row 0.
        self.__search_name_label.grid(row=0, column=0)
        self.__search_name_data.grid(row=0, column=1)
        self.__search_name_button.grid(row=0, column=2)

        # Status messages displayed below search bar in row 1.
        self.__search_error_message.grid(row=1, columnspan=3)

        # Button frame for edit and delete buttons in row 2.
        self.__search_button_frame.grid(row=2, columnspan=3, sticky=NSEW)

        # Layout edit and delete buttons in button frame.
        self.__search_edit_button.pack(side='left', expand=True, fill=BOTH)
        self.__search_delete_button.pack(side='right', expand=True, fill=BOTH)

    def search(self):
        """
        This method handles the search feature when the search button is pressed
        """
        try:
            # Reset the error message field in case there is an error message displayed
            self.__search_error_message.configure(text=" ")

            # Construct a key from the search data field
            full_name = self.__search_name_data.get()
            firstname, lastname = full_name.split(" ")
            key = f"{lastname},{firstname}".lower()

            # Print the information for the associated contact if it exists
            if key in self.__address_book:
                self.print_one_address(self.__address_book[key], 1, self.__search_frame)

            # Handle if the contact does not exist
            else:
                self.__search_error_message.configure(text="\nName not in address book!", fg="red")

        # Handles if an incomplete name is entered for search
        except ValueError:
            self.__search_error_message.configure(text="\nSearch with first and last name.")

    # -- EDIT CONTACT FEATURE ON SEARCH PAGE --

    def edit_address_page(self):
        """
        This method opens the edit page by placing the objects in the grid.
        """

        # Clear previous objects that have been placed.
        self.reset_page(self.__edit_address_frame)

        # Change the title accordingly.
        self.__title_label.configure(text="Edit Contact\n")

        # Get contact which is being edited from the edit-method.
        contact = self.edit_contact_object

        # Same layout as in the add contact page.
        self.__edit_address_frame.columnconfigure(1, weight=1)
        self.__edit_address_frame.rowconfigure(4, weight=1)

        self.__edit_address_first_name_label.grid(row=0, column=0, sticky=NSEW)
        self.__edit_address_first_name_data.grid(row=0, column=1, sticky=NSEW)
        # Insert autofills the field using the contact object's data.
        self.__edit_address_first_name_data.insert(0, contact.first_name)

        self.__edit_address_last_name_label.grid(row=1, column=0, sticky=NSEW)
        self.__edit_address_last_name_data.grid(row=1, column=1, sticky=NSEW)
        self.__edit_address_last_name_data.insert(0, contact.last_name)

        self.__edit_address_street_address_label.grid(row=2, column=0, sticky=NSEW)
        self.__edit_address_street_address_data.grid(row=2, column=1, sticky=NSEW)
        self.__edit_address_street_address_data.insert(0, contact.address)

        self.__edit_address_zip_code_label.grid(row=3, column=0, sticky=NSEW)
        self.__edit_address_zip_code_data.grid(row=3, column=1, sticky=NSEW)
        self.__edit_address_zip_code_data.insert(0, contact.zip_code)

        self.__edit_address_error_message_label.grid(row=4, columnspan=2, sticky=NSEW)

        self.__edit_button_frame.grid(row=5, columnspan=2, sticky=NSEW)
        self.__edit_address_save_button.pack(side='left', expand=True, fill=BOTH)
        self.__edit_address_clear_button.pack(side='right', expand=True, fill=BOTH)

    def edit_address(self):

        # Create a dictionary from the contact data. This makes the use of
        # input checker-method easier.
        form_input = {"first_name": self.__edit_address_first_name_data.get(),
                      "last_name": self.__edit_address_last_name_data.get(),
                      "address": self.__edit_address_street_address_data.get(),
                      "zip_code": self.__edit_address_zip_code_data.get()}

        contact_card = self.input_checker(form_input)

        # Input checker returns None if the contact is invalid.
        if contact_card is not None:
            key = f"{contact_card.last_name},{contact_card.first_name}".lower()

            if key not in self.__address_book:
                self.__address_book[key] = contact_card

                # After editing the contact in a similar fashion as in the add contact-method,
                # we save the address book to ensure no data is lost.
                self.save_address_book()

                # Display a message to the interface that the edit was successful.
                new_label = Label(self.__edit_address_frame, text="Contact edited successfully!", fg="green")
                new_label.grid(row=4, columnspan=2)

                self.edit_address_reset_fields()

    def delete(self):
        """
        This method is called on the search page. It deletes a contact from the
        address book.
        """

        try:
            # Make sure error message label doesn't display an old message.
            self.__search_error_message.configure(text=" ")

            # As user input is in one entry-field we separate user input into two variables.
            full_name = self.__search_name_data.get()
            firstname, last_name = full_name.split(" ")
            key = f"{last_name},{firstname}".lower()

            if key in self.__address_book:

                # This deletes the contact object at it's key.
                del self.__address_book[key]

                # Destroy the displayed contact frame and update the address book accordingly.
                self.__contact_frame.destroy()
                self.save_address_book()
                self.__search_error_message.configure(text="\nContact was deleted successfully!", fg="green")

            else:
                # If name is not in the address book, display an error message.
                self.__search_error_message.configure(text="\nName not in address book!", fg="red")

        # This except statement deals with if user presses delete before searching for a contact.
        except ValueError:
            self.__search_error_message.configure(text="\nSearch for valid contact first!", fg="red")

    def edit(self):
        """
        This method is called by the edit-button. It replaces the old contact
        with an edited one. Similar structure to delete.
        """

        try:
            self.__search_error_message.configure(text=" ")
            full_name = self.__search_name_data.get()
            firstname, last_name = full_name.split(" ")
            key = f"{last_name},{firstname}".lower()

            if key in self.__address_book:

                # Assigns an edit contact object according to search entry field data.
                self.edit_contact_object = self.__address_book[key]

                # Deletes the old, unedited contact.
                del self.__address_book[key]

                # Opens the edit-page where user can edit the contact.
                self.edit_address_page()

            else:
                self.__search_error_message.configure(text="\nName not in address book!", fg="red")

        except ValueError:
            self.__search_error_message.configure(text="\nSearch for valid contact first!", fg="red")

    def edit_address_reset_fields(self):
        """
        Same as other reset field methods but for the edit_address_fields- method.
        """
        self.__edit_address_first_name_data.delete(0, 'end')
        self.__edit_address_last_name_data.delete(0, 'end')
        self.__edit_address_street_address_data.delete(0, 'end')
        self.__edit_address_zip_code_data.delete(0, 'end')
        self.__edit_address_error_message_label.configure(text="")

    def stop(self):
        """
        Ends the execution of the program.
        """

        self.__main_window.destroy()

    def start(self):
        """
        Starts the mainloop.
        """
        self.load_address_book()
        self.__main_window.mainloop()

    def save_address_book(self):
        """
        A data persistence method which if called writes the contents of the
        address book dictionary into a txt-file.
        """

        filename = "address_book.txt"

        # Opens the file using the "write" mode. Thus every time this method
        # is called, the whole txt-file is rewritten. This takes care of
        # duplicate contacts in the txt-file itself.
        file = open(filename, mode="w")

        for address in self.__address_book.values():

            # Semicolon is used to separate the data in the txt-file.
            line = f"{address.first_name};{address.last_name};" \
                   f"{address.address};{address.zip_code};{address.city}\n"

            file.write(line)

        file.close()

    def load_address_book(self):
        """
        A data persistence method which is called every time the program runs.
        It takes the data in the txt-file and adds it to the dictionary used
        by the program. Method is called in the start-method.
        """

        filename = "address_book.txt"

        file = open(filename, mode="r")

        for row in file:

            address_variables = row.rstrip().split(";")

            firstname = address_variables[0]
            lastname = address_variables[1]
            address = address_variables[2]
            zipcode = address_variables[3]
            city = address_variables[4]

            # Creates a contact card object according to the data in the txt-file.
            contact_card = ContactCard(firstname, lastname,
                                       address, zipcode, city)

            key = f"{lastname},{firstname}".lower()

            # If person is not yet in the address book, add the contact.
            # This statement takes care of duplicates.
            if key not in self.__address_book:
                self.__address_book[key] = contact_card

    def read_zip_code_city_file(self):
        """
        This method reads the txt.file zipcodes_and_cities.
        It takes the data and reformats it into a dictionary.
        This dictionary is used in the program for input checking
        and as a sort-of autofill feature.
        """

        filename = "zipcodes_and_cities.txt"

        try:

            file = open(filename, mode="r")

            for row in file:
                zip_code, city = row.rstrip().split(";")

                self.__dict_of_zipcodes_and_cities[zip_code] = city

        # As the program needs this file to be in the correct format and exist,
        # if an error occurs, the program shuts down.
        except (ValueError, FileNotFoundError, OSError):

            # Address book page opens automatically when the program is first
            # opened, so we open it and display an error message on it.
            self.add_to_address_book_page()

            self.__add_address_error_message_label.configure(text="Fatal Error: Contact service provider!", fg="red")

            # Here we use the Python "time" library to tell the program to wait 10 seconds
            # before shutting down. This gives the user time to read the error message.
            time.sleep(10)
            self.stop()

    def reset_page(self, frame):
        """
        Resets a the grid layout of all of the page frames, then lays
        out only the specified frame passed to the method.
        :param frame: tkinter frame that contains objects to be displayed
        """

        # grid_forget "forgets" all of the grid layouts of objects on the page, removing them from view.
        self.__add_address_frame.grid_forget()
        self.__address_book_frame.grid_forget()
        self.__search_frame.grid_forget()
        self.__edit_address_frame.grid_forget()

        # Layout the frame passed to the method, which then lets the objects it contains be laid out in the frame.
        frame.grid(sticky=NSEW)


def main():
    ui = GUI()
    ui.start()


if __name__ == "__main__":
    main()
