import streamlit as st
import google.generativeai as genai

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
        print(response.text)
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
    else:
        st.write("Please enter a query to generate SQL.")

            
main()