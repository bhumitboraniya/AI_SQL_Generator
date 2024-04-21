import streamlit as st
import google.generativeai as genai
import sqlite3
import tkinter as tk
from tkinter import messagebox
import easygui

google_api_key = "AIzaSyByqwQqm-zdgUgek-VFsWVKasMsXL0TvN8"

genai.configure(api_key=google_api_key)
model = genai.GenerativeModel('gemini-pro')

def main():
    st.set_page_config(page_title="SQL Query Generator")
    st.markdown(
        """
                <div style="text-align: center;"> 
                    <h1> SQL Query Generator </h1>
                    <h3> I can generate SQL queries for you! </h3>
                </div>

        """,
        unsafe_allow_html=True,
    )
    text_input= st.text_input("enter your query in english")

    if text_input:  # Check if text_input is not empty
        response = model.generate_content(text_input)
        
        submit = st.button("Go")
        if submit:
            with st.spinner("generating SQL Query"):
                template= """
                    create a SQL query snippet using the below text:
                    '''
                        {text_input}
                    '''
                    I just want a SQL Query.
                        
                    """
                formatted_template = template.format(text_input = text_input)
                st.write(formatted_template)
                response = model.generate_content(formatted_template)
                sql_query = response.text
                st.write(sql_query)

                excepted_output= """
                    what would be the expected response of this SQL query snippet:
                        '''
                        {sql_query}
                        '''
                    provide sample tabular Response with no exploration:
                
                """

                excepted_output_formatted = excepted_output.format(sql_query= sql_query)
                eoutput = model.generate_content(excepted_output_formatted)
                eoutput=  eoutput.text
                st.write(eoutput)


                explanation = """
                    explain this sql query: 
                                '''
                                {sql_query}
                                '''
                    please provide with simplest of explanation:
                """
                explanation_formmated = explanation.format(sql_query= sql_query )
                explanation = model.generate_content(explanation_formmated)
                explanation = explanation.text
                st.write(explanation)
                
                
                sql_query_cleaned = sql_query.replace("`", "").replace("sql", "").strip()
                print("==================")
                print(sql_query_cleaned)
                print("==================")
                
                def execute_query_with_confirmation(sql_query_cleaned):
                    # Prompt for confirmation
                    confirmation = easygui.ccbox("Are you sure you want to execute this query?", "Confirmation")
                    if confirmation:
                        # Connect to the database and execute the query
                        conn = sqlite3.connect('new_database.db')
                        cursor = conn.cursor()
                        cursor.execute(sql_query_cleaned)
                        conn.commit()
                        conn.close()
                        easygui.msgbox("Query executed successfully!", "Success")
                    else:
                        easygui.msgbox("Query execution cancelled.", "Cancelled")

            # Example SQL query
            # sql_query = "INSERT INTO your_table (name, age) VALUES ('John', 30);"

            # Execute the query with confirmation
            execute_query_with_confirmation(sql_query_cleaned)
                    
                    
                    # conn = sqlite3.connect('new_database.db')
                    # cursor = conn.cursor()
                    # cursor.execute(sql_query_cleaned)
                    # conn.commit()
                    # conn.close()
    else:
        st.write("Please enter a query to generate SQL.")

            
main()
