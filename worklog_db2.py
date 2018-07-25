import os
import datetime
import csv
import re

from peewee import *
from add_menu import Add_Menu
from main_menu import Main_Menu
from search_menu import Search_Menu
from models.time_entry import Time_Entry
from models.employee import Employee
from time_entriesdb import *


def main():
    """Executes core program logic.

    User can search existing entries through a variety of search options or can
    add a new entry. The core program logic repeats until user exits program.
    """

    while True:
        choice = run_main_menu_process()
        if choice == "1":
            run_add_entry_process()
        if choice == "2":
            search = Search_Menu()
            search.show()
            search_type = input("Please select a search type: ").strip()
            clear_screen()
            if search_type.lower() == "a":
                run_browse_by_name_process()
            elif search_type.lower() == "b":
                run_search_by_name_process()
            elif search_type.lower() == "c":
                run_exact_date_search_process() 
            elif search_type.lower() == "d":
                run_range_of_dates_search_process()
            elif search_type.lower() == "e":
                run_time_spent_process()
            elif search_type.lower() == "f":
                run_keyword_search_process()
            elif search_type.lower() == "g":
                pass
            else:
                print("The search option you entered is not recognized.")
                print("Please enter a letter corresponding to an availble" +
                      "option, e.g. \"a\"")
                print("")
                dummy = input("Press Enter to return to main menu. ")
        if choice == "3":
            break


def run_main_menu_process():
    """Displays contents of main menu."""

    clear_screen()
    main = Main_Menu()
    main.show()
    main_result = input("Please enter number of choice (e.g. 1): ")
    clear_screen()
    return main_result


def run_add_entry_process():
    """Creates new time entry and saves to database.

    Obtains field information from user, creates new time entry object, and
    then saves the entry's information into the database.
    """

    add = Add_Menu()
    add.show()
    employee_name = get_employee_name()
    clear_screen()
    add.show()
    date = get_date()
    clear_screen()
    add.show()
    title = get_title()
    clear_screen()
    add.show()
    time_spent = get_time_spent()
    clear_screen()
    add.show()
    notes = get_notes()
    Time_Entry.create(employee_name=employee_name,
                      date=date,
                      title=title,
                      time_spent=time_spent,
                      notes=notes)
    clear_screen()
    input("The entry has been added! Press Enter to return to main menu.")
    clear_screen()


def get_employee_name():
    """Gets employee name for purpose of creating time entry.

    Asks user for employee name, determines whether name already exists, 
    returns employee name as a string.
    """

    employee_name = input("Employee Name \n" + 
                          "Please enter employee's name: ").strip()
    try:
        employee = Employee.create(name=employee_name)
    except IntegrityError:
        employee = Employee.get(Employee.name == employee_name)

    return employee_name


def get_date():
    """Gets date for purpose of creating time entry.

    Asks user for date of entry, determines whether the date is properly
    formatted, and returns date as a datetime object. 
    """

    date = input("Enter Date of the Task \n" + 
                 "Please use DD/MM/YYYY format: ").strip()
    date = validate_date(date)
    date = datetime.datetime.strptime(date, '%d/%m/%Y')
    return date


def validate_date(date):
    """Validates date input from user.

    Ensures that user enters a string for the date that follows DD/MM/YYYY
    format. Returns date as a string.
    """

    date.strip()
    while True:
        try:
            datetime.datetime.strptime(date, '%d/%m/%Y')
            break
        except ValueError:
            clear_screen()
            print("The date must be in DD/MM/YYYY fromat.")
            date = input("Please re-enter the date. > ")
            date.strip()
    return date


def get_title():
    """Gets title for purpose of creating time entry.

    Asks user for title and returns it as a string. 
    """

    title = input("Title of Task: ").strip()
    return title


def get_time_spent():
    """Gets time spent for purpose of creating time entry.

    Asks user for time spent, ensures that it is a number, returns the time
    spent as a string.
    """

    time_spent = input("Time spent (rounded in minutes, e.g. 30): ").strip()
    time_spent = validate_time_spent(time_spent)
    return time_spent


def validate_time_spent(time_spent):
    """Validates time spent input from user.

    Ensures that user enters an integer string for time spent amount.
    """

    time_spent.strip()
    while True:
        try:
            int(time_spent)
            break
        except ValueError:
            clear_screen()
            print("The time spent must be an integer (e.g. 30, 60, or 120).")
            time_spent = input("Please re-enter time. > ")
            time_spent.strip()
    return time_spent


def get_notes():
    """Gets notes for purpose of creating time entry.

    Asks user for notes and returns the input as a string.
    """

    notes = input("Notes (Optional, you can leave this empty): ").strip()
    return notes


def run_browse_by_name_process():
    """Executes employee name search on existing entries.

    Presents user with list of employees who have created entries.
    Allows user to view entries created by one of the employees listed.
     """

    list_of_employees = Employee.select()

    if len(list_of_employees) == 0:
        print("There are no time entries in the database.")
        dummy = input("Press Enter to continue.: > ")
        clear_screen()

    else:
        print("The following employees have created time entries:")
        print("")
        for employee in list_of_employees:
            print("\t" + employee.name)

        print("")
        selection = input("Which employee's time " + 
                          "entries would you like to view? > ").strip()

        selection = validate_employee_name(selection)

        matching_entries = (Time_Entry.select()
                                      .join(Employee)
                                      .where(Employee.name == selection))
        clear_screen()

        run_options_loop(matching_entries)


def run_search_by_name_process():
    """Executes name search on existing entries.

    Asks user for a name to search. Informs user if there is none, one, or 
    many matches. Prompts user to continue process.
    """

    name = input("Please enter a name to search. > ").strip()

    matching_names = (Employee.select().where(Employee.name.contains(name)))

    if len(matching_names) == 0:
        print("Sorry there are no employees whose name contains {}"
               .format(name))
        dummy = input("Please press Enter to return to the Main Menu.")
        clear_screen()

    elif len(matching_names) == 1:
        matching_entries = (Time_Entry.select()
                                      .join(Employee)
                                      .where(Employee.name == name))
        print("Your search returned one match.")
        print("")
        dummy = input("Press Enter to view {}'s entries."
                      .format(matching_entries[0].employee_name.name))
        clear_screen()
        run_options_loop(matching_entries)

    elif len(matching_names) > 1:
        print("There is more than one employee " + 
              "whose name contains {}.".format(name))
        print("")
        for employee in matching_names:
            print("\t {}".format(employee.name))
        print("")
        selection = input("Which employee's time " + 
                          "entries would you like to view? > ").strip()
        selection = validate_employee_name(selection)
        matching_entries = (Time_Entry.select()
                                      .join(Employee)
                                      .where(Employee.name == selection))
        run_options_loop(matching_entries)

    else:
        pass 


def validate_employee_name(employee_name):
    """Confirms that employee name has entries associated with it.

    Takes employee name as input and either returns the employee name or 
    informs user that the requested employee is not recognized.
    """

    employee_name.strip()
    while True:
        try:
            employee = Employee.get(Employee.name == employee_name)
            break
        except DoesNotExist:
            clear_screen()
            print("The name you entered is not recognized.")
            employee_name = input("Please re-enter the name of the person " + 
                               "whose entries you would like to view. > ")
            employee_name.strip()
    return employee_name


def run_exact_date_search_process():
    """Executes exact date search on existing entries.

    Asks user for an exact date. Returns a list of matching entries. If there
    are no matches then user is informed of that fact.
    """

    list_of_entries = Time_Entry.select()

    print("Time entries were created on the following dates:")
    print("")
    for entry in list_of_entries:
        print("\t", end="")
        prettyprint_date(entry.date)
    print("")

    print("Enter the Date you would like to view.")
    exact_date = input("Please use DD/MM/YYYY: > ").strip()
    exact_date = validate_date_eds(exact_date, list_of_entries)
    exact_date = datetime.datetime.strptime(exact_date, '%d/%m/%Y')
    matching_entries = (Time_Entry.select()
                                  .where(Time_Entry.date == exact_date))
    clear_screen()

    if len(matching_entries) == 0:
        print("No matching entries found.")
        dummy = input("Press enter to continue. ")
    else:
        run_options_loop(matching_entries)


def run_range_of_dates_search_process():
    """Executes range of dates search on existing entries.

    Asks user for range of dates. Returns a list of matching entries. If there
    are no matches then user is informed of that fact.
    """

    start_date, end_date = get_date_range()

    within_range = ((Time_Entry.date >= start_date) 
                     & (Time_Entry.date <= end_date))

    matching_entries = (Time_Entry.select().where(within_range))

    clear_screen()

    if len(matching_entries) == 0:
        print("No matching entries found.")
        dummy = input("Press enter to continue. ")
    else:
        run_options_loop(matching_entries)


def get_date_range():
    """Gets date range from user.

    Asks user for start and end of date range. Returns both dates formatted as 
    datetime objects.
    """

    print("Enter the Start Date of Range")
    start_date = input("Please use DD/MM/YYYY format: > ")
    start_date = validate_date(start_date)
    start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')

    clear_screen()

    print("Enter the End Date of Rnage")
    end_date = input("Please use DD/MM/YYYY format: > ")
    end_date = validate_date(end_date)
    end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')

    return start_date, end_date


def run_time_spent_process():
    """Executes time spent search on existing entries.

    Asks user for a time amount. Returns a list of matching entries. If there
    are no matches then user is informed of that fact.
    """

    time_spent = get_time_spent()

    matching_entries = (Time_Entry.select()
                                  .where(Time_Entry.time_spent == time_spent))

    clear_screen()

    if len(matching_entries) == 0:
        print("No matching entries found.")
        dummy = input("Press enter to continue. ")
    else:
        run_options_loop(matching_entries)


def run_keyword_search_process():
    """Executes exact string search on existing entries.

    Asks user for an exact string to match against. Returns a list of matching
    entries. If there are no matches then user is informed of that fact.
    """

    print("This will search for matches in the title and notes fields.")
    search_term = input("Enter a search term: ").strip()

    contains_search_term = ((Time_Entry.title.contains(search_term))
                             | (Time_Entry.notes.contains(search_term)))

    matching_entries = Time_Entry.select().where(contains_search_term)

    clear_screen()

    if len(matching_entries) == 0:
        print("No matching entries found.")
        dummy = input("Press enter to continue. ")
    else:
        run_options_loop(matching_entries)


def run_options_loop(matching_entries):
    """Allows user to view and perform operations on matching entries.

    matching_entries and non_matching_entries are lists of time entry objects.
    """

    total_results = len(matching_entries)
    count = 0
    while True:
        display_sr(matching_entries, count, total_results)
        option = input("> ")
        if option.upper() == "N":
            try:
                count += 1
                matching_entries[count]
            except IndexError:
                count -= 1
                clear_screen()
            clear_screen()
        elif option.upper() == "P":
            count -= 1
            if count < 0:
                count += 1
            clear_screen()
        elif option.upper() == "E":
            clear_screen()
            while True:
                print("What field would you like to edit?")
                print("Please type \"date\", \"title\", \"time spent\", or " +
                      "\"notes\".")
                print("")
                edit_selection = input("> ")
                clear_screen()
                edit_selection.lower().strip()
                if edit_selection == "date":
                    print("Enter a new date.")
                    print("Please use DD/MM/YYYY format.")
                    new_date = input("> ").strip()
                    new_date = validate_date(new_date)
                    matching_entries[count].date = new_date
                    matching_entries[count].save()
                    clear_screen()
                    print("New Date Saved!")
                    dummy = input("Press Enter to Continue.")
                    clear_screen()
                    break
                elif edit_selection == "title":
                    new_title = input("Enter a new title. > ").strip()
                    matching_entries[count].title = new_title
                    matching_entries[count].save()
                    clear_screen()
                    print("New Title Saved!")
                    dummy = input("Press Enter to Continue.")
                    clear_screen()
                    break
                elif edit_selection == "time spent":
                    new_time_spent = input("Enter new time spent. > ").strip()
                    new_time_spent = validate_time_spent(new_time_spent)
                    matching_entries[count].time_spent = new_time_spent
                    matching_entries[count].save()
                    clear_screen()
                    print("New Amount of Time Saved!")
                    dummy = input("Press Enter to Continue.")
                    clear_screen()
                    break
                elif edit_selection == "notes":
                    new_notes = input("Enter new notes. > ").strip()
                    matching_entries[count].notes = new_notes
                    matching_entries[count].save()
                    clear_screen()
                    print("New Notes Saved!")
                    dummy = input("Press Enter to Continue.")
                    clear_screen()
                    break
                else:
                    print("The field you entered is not recognized.")
                    dummy = input("Press enter to try again.")
                    clear_screen()
        elif option.upper() == "D":
            clear_screen()
            print("WARNING: This will delete the selected entry.")
            answer = input("Are you sure you want to proceed (Y/N)? > ")
            if answer.strip().lower() == "y":
                name = matching_entries[count].employee_name.name
                matching_entries[count].delete_instance()
                number_of_entries = remaining_entries(name)
                if number_of_entries == 0:
                    employee = Employee.get(Employee.name == name)
                    employee.delete_instance(recursive=True)
                else:
                    pass
                clear_screen()
                print("Entry Deleted.")
                dummy = input("Press Enter to Continue.")
                clear_screen()
                break
            else:
                print()
            pass
        elif option.upper() == "R":
            break
        else:
            clear_screen()
            print("Command not recognized. \n Please enter N, P, E, D, or R.")
            dummy = input("Press enter to continue viewing search results.")
            clear_screen()


def remaining_entries(employee_name):
    """Returns the number of entries that an employee has made."""

    number_of_entries = (Time_Entry.select()
                                   .join(Employee)
                                   .where(Employee.name == employee_name)
                                   .count()) 
    return number_of_entries


def display_sr(matching_entries, count, total_results):
    """Displays matching search results.

    This function controls the display of information for matching time
    entries. It also displays operations the user can perform.
    """

    len_of_list = len(matching_entries)

    if count == 0:
        print("Name: {}".format(matching_entries[count].employee_name.name))
        print("Date: ", end="")
        prettyprint_date(matching_entries[count].date)
        print("Title: {}".format(matching_entries[count].title))
        print("Time Spent: {}".format(matching_entries[count].time_spent))
        print("Notes: {}".format(matching_entries[count].notes))
        print("")
        print("Result {} of {}".format(count + 1, total_results))
        print("")
        if len_of_list == 1:
            print("[E]dit, [D]elete, [R]eturn to search menu")
        else:
            print("[N]ext, [E]dit, [D]elete, [R]eturn to search menu")
    elif count > 0:
        print("Name: {}".format(matching_entries[count].employee_name.name))
        print("Date: ", end="")
        prettyprint_date(matching_entries[count].date)
        print("Title: {}".format(matching_entries[count].title))
        print("Time Spent: {}".format(matching_entries[count].time_spent))
        print("Notes: {}".format(matching_entries[count].notes))
        print("")
        print("Result {} of {}".format(count + 1, total_results))
        print("")
        if count == (len_of_list - 1):
            print("[P]revious, [E]dit, [D]elete, [R]eturn to search menu")
        else:
            print("[P]revious, [N]ext, [E]dit, [D]elete," + 
                  " [R]eturn to search menu")


def prettyprint_date(date_string):
    dt = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    print("{:%d/%m/%Y}".format(dt))


def validate_date(date):
    """Validates date input from user.

    Ensures that user enters a string for the date that follows DD/MM/YYYY
    format.
    """

    date.strip()
    while True:
        try:
            datetime.datetime.strptime(date, '%d/%m/%Y')
            break
        except ValueError:
            clear_screen()
            print("The date must be in DD/MM/YYYY fromat.")
            date = input("Please re-enter the date. > ")
            date.strip()
    return date


def validate_date_eds(date, time_entries):
    """Validates date input from user.

    Ensures that user enters a string for the date that follows DD/MM/YYYY
    format. Separate version for exact date search so that available dates are
    re-displayed.
    """

    date.strip()
    while True:
        try:
            datetime.datetime.strptime(date, '%d/%m/%Y')
            break
        except ValueError:
            clear_screen()
            print("The date must be in DD/MM/YYYY format.")
            print("The available dates are: \n")
            for entry in time_entries:
                print("\t", end="")
                prettyprint_date(entry.date)
            date = input("Please re-enter the date. > ").strip()
    return date


def validate_time_spent(time_spent):
    """Validates time spent input from user.

    Ensures that user enters an integer string for time spent amount.
    """

    time_spent.strip()
    while True:
        try:
            int(time_spent)
            break
        except ValueError:
            clear_screen()
            print("The time spent must be an integer (e.g. 30, 60, or 120).")
            time_spent = input("Please re-enter time. > ")
            time_spent.strip()
    return time_spent


def clear_screen():
    """Clears the screen of all prior input and output."""

    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    initialize()
    main()
