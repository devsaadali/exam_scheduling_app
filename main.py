import streamlit as st
import pandas as pd
import networkx as nx
import PyPDF2
import io
import openpyxl

def read_file(file):
    file_type = file.type
    st.write(f"Detected file type: {file_type}")  # Debug info
    
    if file_type == "text/csv":
        return pd.read_csv(file)
    elif file_type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        # Convert PDF text to DataFrame
        return pd.DataFrame({'text': [text]})
    elif file_type == "text/plain":
        text = file.getvalue().decode("utf-8")
        # Convert plain text to DataFrame
        return pd.DataFrame({'text': [text]})
    elif file_type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        try:
            return pd.read_excel(file)
        except Exception as e:
            st.error(f"Error reading Excel file: {str(e)}")
            return None
    else:
        st.error(f"Unsupported file type: {file_type}")
        return None

def schedule(df):
    # Remove the course SS1018
    # df.drop(df[df['code'] == 'SS1018'].index, inplace=True)

    # Create a graph
    G = nx.Graph()

    # Extract unique subjects from the DataFrame
    courses = set(df['code'])
    G.add_nodes_from(courses)

    # Calculating edge weights based on clashes
    for course1 in courses:
        for course2 in courses:
            if course1 != course2:
                course1_students = set(df[df['code'] == course1]['roll_no'])
                course2_students = set(df[df['code'] == course2]['roll_no'])
                clash = course1_students.intersection(course2_students)
                total_clashes = len(clash)
                if total_clashes > 0:
                    G.add_edge(course1, course2, weight=total_clashes)

    # Calculate scheduling with minimum clash-free slots
    c_num = nx.algorithms.coloring.greedy_color(G, strategy='largest_first')
    max_c = max(c_num.values()) + 1  # Add 1 to account for 0-based indexing

    # Print the final scheduling
    schedule = {i: [] for i in range(max_c)}
    for course, color in c_num.items():
        schedule[color].append(course)

    # print("Final Scheduling:")
    # for slot, courses in schedule.items():
    #     print(f"Slot {slot + 1}: {courses}")  # Add 1 to slot number for 1-based indexing

    # print(schedule)
    # # Print additional information
    # print("Total number of nodes in resultant graph:", len(G.nodes))
    # print("Total number of edges in the graph:", len(G.edges))
    # print("Chromatic Number (Minimum number of slots):", max_c)
    # print(len(schedule))

    return schedule, G


def rename_same_courses(dataframe, same_courses):
    renamed_courses = []

    for same in same_courses:
        new_code = same[0] + '_' + same[1]
        # print(new_code)
        renamed_courses.append(new_code)

    # print(renamed_courses)

    rename_count = 0

    for same_course in same_courses:
        # replace_same_courses(same_course, renamed_courses[rename_count])
        dataframe.loc[(dataframe["code"] == same_course[0]) | (dataframe["code"] == same_course[1]), "code"] = renamed_courses[rename_count]
        # print("Replaced")
        rename_count += 1

    return dataframe

def check_where_course_can_be_moved(slot_list, course_code, G):
    can_be_moved = False
    if course_code not in slot_list:
        for course in slot_list:
            if G.has_edge(course_code, course):
                return False
        return True
    else:
        return False

def get_unique_courses(dataframe):
    return dataframe['code'].unique()

st.title("Datesheet App")
st.subheader("Powered by: Saad & Munazah")



uploaded_file = st.file_uploader("Upload your timetable file", type=["csv", "pdf", "txt", "xlsx"])

if uploaded_file is not None:
    st.write("File uploaded successfully!")
    
    # Read the file
    file_contents = read_file(uploaded_file)
    
    if file_contents is not None:

        same_courses = [['CS4063', 'DS5007'], ['CS4055', 'CS6007'], ['CS5012', 'CS4068'], ['SS1088', 'SS2010'], ['SS1007', 'SS1002']]

        dataframe = rename_same_courses(file_contents, same_courses)

        scheduled_timetable, G = schedule(dataframe)

        st.subheader("Scheduled Timetable:")
        for slot, courses in scheduled_timetable.items():
            st.write(f"Slot {slot + 1}: {courses}")

        available_slots = []
        # Add input for course code
        course_code_input = st.text_input("Enter the course code to check available slots:")

        valid_course_code = True

        if course_code_input:
            unique_courses = get_unique_courses(dataframe)
            if course_code_input in unique_courses:
                for slot, courses in scheduled_timetable.items():  # slot is a tuple (slot, courses)
                    can_be_moved = check_where_course_can_be_moved(courses, course_code_input, G)  # Pass courses instead of slot
                    if can_be_moved:
                        available_slots.append(slot + 1)  # Append the slot number (1-based)
                    # else:
                    #     st.write(f"The course '{course_code_input}' cannot be moved to slot {slot + 1}.")
            else:
                st.error(f"{course_code_input} is not a valid course code.")
                valid_course_code = False
        if course_code_input:
            if available_slots:
                st.write(f"{course_code_input} can be moved to slots: {available_slots}")
            else:
                if valid_course_code:
                    st.warning(f"{course_code_input} cannot be moved to any slot.")
    else:
        st.error("Unable to read the file. Please make sure it's a valid CSV, PDF, TXT, or Excel file.")
else:
    st.info("Please upload a file to begin.")
