import pandas as pd
import networkx as nx


def schedule(df):
    # Read the data
    # df = pd.read_excel('Saad data.xlsx')

    # # Define same courses pairs
    # same_courses = [['CS4063', 'DS5007'], ['CS4055', 'CS6007'], ['CS5012', 'CS4068'], ['SS1088', 'SS2010'], ['SS1007', 'SS1002']]

    # # Rename same courses pairs
    # renamed_courses = []
    # for same in same_courses:
    #     new_code = same[0] + '_' + same[1]
    #     renamed_courses.append(new_code)

    # # Function to rename same courses
    # def rename_same_courses(courses_to_be_renamed, replace_with):
    #     df.loc[(df["code"] == courses_to_be_renamed[0]) | (df["code"] == courses_to_be_renamed[1]), "code"] = replace_with

    # # Apply renaming
    # for i, same_course in enumerate(same_courses):
    #     rename_same_courses(same_course, renamed_courses[i])

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

    print("Final Scheduling:")
    for slot, courses in schedule.items():
        print(f"Slot {slot + 1}: {courses}")  # Add 1 to slot number for 1-based indexing

    # Print additional information
    print("Total number of nodes in resultant graph:", len(G.nodes))
    print("Total number of edges in the graph:", len(G.edges))
    print("Chromatic Number (Minimum number of slots):", max_c)
