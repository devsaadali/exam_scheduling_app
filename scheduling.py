import pandas as pd

# def convert_to_dataframe(file_contents):
#     if file_contents.endswith('.csv'):
#         return pd.read_csv(file_contents)
#     elif file_contents.endswith('.xlsx'):
#         return pd.read_excel(file_contents)
#     else:
#         return None

# I will pass the file content to this function. I want this function to return a dataframe containing that content.

# def convert_to_dataframe(file_contents):
#     import io
#     import pandas as pd

#     # Try to read as CSV first
#     try:
#         return pd.read_csv(io.BytesIO(file_contents))
#     except pd.errors.EmptyDataError:
#         print("The file is empty.")
#         return None
#     except Exception as e:
#         print(f"Error reading CSV: {str(e)}")
#         # If CSV fails, try Excel
#         try:
#             return pd.read_excel(io.BytesIO(file_contents))
#         except Exception as e:
#             print(f"Error reading Excel: {str(e)}")
#             # If both fail, return None
#             return None
        



def rename_same_courses(dataframe, same_courses):
    renamed_courses = []

    for same in same_courses:
        new_code = same[0] + '_' + same[1]
        # print(new_code)
        renamed_courses.append(new_code)

    print(renamed_courses)

    rename_count = 0

    for same_course in same_courses:
        # replace_same_courses(same_course, renamed_courses[rename_count])
        dataframe.loc[(dataframe["code"] == same_course[0]) | (dataframe["code"] == same_course[1]), "code"] = renamed_courses[rename_count]
        print("Replaced")
        rename_count += 1

    return dataframe

# def replace_same_courses(dataframe, courses_to_be_renamed, replace_with):
#   dataframe.loc[(dataframe["cod"] == courses_to_be_renamed[0]) | (dataframe["cod"] == courses_to_be_renamed[1]), "cod"] = replace_with
#   print("Replaced")
