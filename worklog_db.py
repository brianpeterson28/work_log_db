import os
import datetime
import csv
import re

from peewee import *
from time_entry import Time_Entry
from employee import Employee
from main_menu import Main_Menu
from add_menu import Add_Menu
from search_menu import Search_Menu


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
            search_type = input("Please select a search type: ")
            clear_screen()
            if search_type.lower() == "a":
                run_employee_name_search_process()
            elif search_type.lower() == "b":
                run_exact_date_search_process() # model off of exact_date_search()
            elif search_type.lower() == "c":
                run_range_of_dates_search_process()
            elif search_type.lower() == "d":
                run_time_spent_process()
            elif search_type.lower() == "e":
                run_exact_search_process()
            elif search_type.lower() == "f":
                pass
            else:
                print("The search option you entered is not recognized.")
                print("Please enter a letter corresponding to an availble" +
                      "option, e.g. \"a\"")
                print("")
                dummy = input("Press enter to return to main menu. ")
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
    """Creates new time entry and saves to csv file.

    Obtains field information from user, creates new time entry object, and
    then saves the entry's information into the csv file.
    """

    add = Add_Menu()
    add.show()
    print("Employee Name")
    employee_name = input("Please enter employee's name: ").strip()
    clear_screen()

    try:
        employee = Employee.create(name=employee_name)
    except IntegrityError:
        employee = Employee.get(Employee.name == employee_name)

    print("Date of the Task")
    date = input("Please use DD/MM/YYYY format: ").strip()
    date = validate_date(date)
    clear_screen()
    add.show()

    title = input("Title of Task: ").strip()
    clear_screen()
    add.show()

    time_spent = input("Time spent (rounded in minutes, e.g. 30): ").strip()
    time_spent = validate_time_spent(time_spent)
    clear_screen()
    add.show()

    notes = input("Notes (Optional, you can leave this empty): ").strip()

    Time_Entry.create(employee_name=employee,
                      date=date,
                      title=title,
                      time_spent=time_spent,
                      notes=notes)
    clear_screen()
    
    input("The entry has been added! Press enter to return to main menu.")
    clear_screen()


def run_employee_name_search_process():
    """Executes employee name search on existing entries.

    Presents user with list of employees who have created entries.
    Allows user to view entries created by one of the employees listed.
     """
     print("The following employees have created time entries.:")

     list_of_employees = Employee.select()
     for employee in list_of_employees:
        print("\t" + employee.name)

    selection = input("Which employee's time " + 
                      "entries would you like to view? > ").strip()

    selection = validate_employee_name(selection)

    matching_entries = (Time_Entry
                        .select()
                        .join(Employee)
                        .where(Employee.name == selection)

    run_options_loop(matching_entries)



def validate_employee_name(employee_name):
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
    no matches then user is informed of that fact.
    """
    time_entries = recall_time_entries()
    print("The available dates are: \n")
    for entry in time_entries:
        print("\t" + entry.date)
    print("")
    print("Enter the Date you would like to view.")
    exact_date = input("Please use DD/MM/YYYY: ")
    exact_date = validate_date_eds(exact_date, time_entries)
    matching_entries = []
    non_matching_entries = []
    for entry in time_entries:
        if re.match(r'' + exact_date, entry.date):
            matching_entries.append(entry)
        else:
            non_matching_entries.append(entry)
    clear_screen()
    if len(matching_entries) == 0:
        print("No matching entries found.")
        dummy = input("Press enter to continue. ")
    else:
        run_options_loop(matching_entries, non_matching_entries)


def run_range_of_dates_search_process():
    """Executes range of date search on existing entries.

    Asks user for range of dates. Returns a list of matching entries. If there
    are no matches then user is informed of that fact.
    """

    print("Enter the Start Date of Range")
    start_date = input("Please use DD/MM/YYYY format: ")
    start_date = validate_date(start_date)
    clear_screen()
    print("Enter the End Date of Rnage")
    end_date = input("Please use DD/MM/YYYY format: ")
    end_date = validate_date(end_date)
    start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')
    end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')
    time_entries = recall_time_entries()
    matching_entries = []
    non_matching_entries = []
    for entry in time_entries:
        entry_date = datetime.datetime.strptime(entry.date, '%d/%m/%Y')
        if entry_date > start_date and entry_date < end_date:
            matching_entries.append(entry)
        else:
            non_matching_entries.append(entry)
    clear_screen()
    if len(matching_entries) == 0:
        print("No matching entries found.")
        dummy = input("Press enter to continue. ")
    else:
        run_options_loop(matching_entries, non_matching_entries)


def run_time_spent_process():
    """Executes time spent search on existing entries.

    Asks user for a time amount. Returns a list of matching entries. If there
    are no matches then user is informed of that fact.
    """

    print("Enter the amount of time spent")
    time_spent = input("Please use the number of minutes (e.g. 60): ")
    time_spent = validate_time_spent(time_spent)
    time_entries = recall_time_entries()
    matching_entries = []
    non_matching_entries = []
    for entry in time_entries:
        if int(entry.time_spent) == int(time_spent):
            matching_entries.append(entry)
        else:
            non_matching_entries.append(entry)
    clear_screen()
    if len(matching_entries) == 0:
        print("No matching entries found.")
        dummy = input("Press enter to continue. ")
    else:
        run_options_loop(matching_entries, non_matching_entries)


def run_exact_search_process():
    """Executes exact string search on existing entries.

    Asks user for an exact string to match against. Returns a list of matching
    entries. If there are no matches then user is informed of that fact.
    """

    print("This will search for matches in the title and notes fields.")
    search_term = input("Enter a search term: ")
    time_entries = recall_time_entries()
    matching_entries = []
    non_matching_entries = []
    for entry in time_entries:
        if re.search(r'' + search_term, entry.title + entry.notes):
            matching_entries.append(entry)
        else:
            non_matching_entries.append(entry)
    clear_screen()
    if len(matching_entries) == 0:
        print("No matching entries found.")
        dummy = input("Press enter to continue. ")
    else:
        run_options_loop(matching_entries, non_matching_entries)


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
                    new_date = input("> ")
                    new_date = validate_date(new_date)
                    matching_entries[count].date = new_date
                    matching_entries[count].save()
                    clear_screen()
                    print("New Date Saved!")
                    dummy = input("Press Enter to Continue.")
                    clear_screen()
                    break
                elif edit_selection == "title":
                    new_title = input("Enter a new title. > ")
                    matching_entries[count].title = new_title
                    matching_entries[count].save()
                    clear_screen()
                    print("New Title Saved!")
                    dummy = input("Press Enter to Continue.")
                    clear_screen()
                    break
                elif edit_selection == "time spent":
                    new_time_spent = input("Enter new time spent. > ")
                    new_time_spent = validate_time_spent(new_time_spent)
                    matching_entries[count].time_spent = new_time_spent
                    matching_entries[count].save()
                    clear_screen()
                    print("New Amount of Time Saved!")
                    dummy = input("Press Enter to Continue.")
                    clear_screen()
                    break
                elif edit_selection == "notes":
                    new_notes = input("Enter new notes. > ")
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
                del matching_entries[count]
                save_edited_entry(matching_entries, non_matching_entries)
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
            print("Command not recognized.")
            print("Please enter N, P, E, D, or R.")
            dummy = input("Press enter to continue viewing search results.")
            clear_screen()


def save_edited_entry(matching_entries, non_matching_entries):
    """Saves edited entries to csv file."""

    edited_entries = matching_entries + non_matching_entries
    first = create_iterable_entry(edited_entries.pop(0))

    with open(TIME_ENTRY_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(first)

    with open(TIME_ENTRY_FILE, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for entry in edited_entries:
            entry = create_iterable_entry(entry)
            writer.writerow(entry)


def create_iterable_entry(entry):
    """Makes entry object an iterable list.

    This is a helper function that converts a time entry object into a list
    containing the entry's fields. This is done so csv.writer can handle it.
    """

    iterable_entry = []
    iterable_entry.append(entry.date)
    iterable_entry.append(entry.title)
    iterable_entry.append(entry.time_spent)
    iterable_entry.append(entry.notes)
    return iterable_entry


def display_sr(matching_entries, count, total_results):
    """Displays matching search results.

    This function controls the display of information for matching time
    entries. It also displays operations the user can perform.
    """

    if count == 0:
        print("Name: {}".format(matching_entries[count].employee_name.name))
        print("Date: {}".format(matching_entries[count].date))
        print("Title: {}".format(matching_entries[count].title))
        print("Time Spent: {}".format(matching_entries[count].time_spent))
        print("Notes: {}".format(matching_entries[count].notes))
        print("")
        print("Result {} of {}".format(count + 1, total_results))
        print("")
        print("[N]ext, [E]dit, [D]elete, [R]eturn to search menu")
    elif count > 0:
        print("Name: {}".format(matching_entries[count].employee_name.name))
        print("Date: {}".format(matching_entries[count].date))
        print("Title: {}".format(matching_entries[count].title))
        print("Time Spent: {}".format(matching_entries[count].time_spent))
        print("Notes: {}".format(matching_entries[count].notes))
        print("")
        print("Result {} of {}".format(count + 1, total_results))
        print("")
        print("[P]revious, [N]ext, [E]dit, [D]elete, [R]eturn to search menu")


def recall_time_entries():
    """Reads previously saved entries into program.

    Opens the designated csv file, reads its contents, and loads all of them
    into a list that can be used by program.
    """

    time_entries = []
    with open(TIME_ENTRY_FILE, newline="") as csvfile:
        time_entry_file = csv.reader(csvfile)
        for row in time_entry_file:
            entry = Time_Entry()
            entry.set_date(row[0])
            entry.set_title(row[1])
            entry.set_time_spent(row[2])
            entry.set_notes(row[3])
            time_entries.append(entry)
    return time_entries


def validate_date(date):
    """Validates date input from user.

    Ensures that user enters a string for the date that follows DD/MM/YYYY
    format.
    """

    date.strip()
    while True:
        try:
            datetime.datetime.strptime(date, '%d/%m/%Y') #may need to switch to '%Y-%m-%d'
            break
        except ValueError:
            clear_screen()
            print("The date must be in DD/MM/YYYY fromat.") #may need to switch to 'YYYY/MM/DD'
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
                print("\t" + entry.date)
            date = input("Please re-enter the date. > ")
            date.strip()
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
    main()
