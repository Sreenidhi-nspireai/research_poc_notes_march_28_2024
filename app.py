import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Load your data
from cryptography.fernet import Fernet
import pickle


# Function to decrypt data with a key provided by the user
def decrypt_data(encrypted_data_path, key):
    try:
        # Initialize the Fernet class with the key
        cipher_suite = Fernet(key)

        # Load the encrypted data
        with open(encrypted_data_path, 'rb') as file_encrypted:
            encrypted_data = file_encrypted.read()

        # Decrypt the data and load it into a DataFrame
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        df = pickle.loads(decrypted_data)
        return df, None
    except Exception as e:
        return None, e



# Sidebar for key input
st.sidebar.header("Security")
key_input = st.sidebar.text_area("Paste the encryption key here:", value="", max_chars=None, height=None, help="Paste the Fernet encryption key to access the data.")
structured_commenting_persons_df = None

# Button to load the data
if st.sidebar.button('Load Data'):
    if key_input:
        # Path to your encrypted data
        encrypted_data_path = 'encrypted_data.pkl'

        # Decrypt and load the data
        structured_commenting_persons_df, error = decrypt_data(encrypted_data_path, key_input.encode())

        if structured_commenting_persons_df is not None:
            # st.write(df.head())  # Example of displaying the data
            st.sidebar.success("Data loaded successfully.")
        else:
            st.error(f"Failed to decrypt data: {error}")
    else:
        st.sidebar.error("Please paste the encryption key to load the data.")


# output_excel_path = 'structured_note_quality_data.xlsx'
# structured_commenting_persons_df = pd.read_excel(output_excel_path, sheet_name='Structured Commenting Persons')

# App title
st.title('Data Analysis on Note Quality and Insights')

if structured_commenting_persons_df is not None:
        
    # Using tabs to organize different sections
    tab1, tab2, tab3, tab4 = st.tabs(["Introduction", "Category Analysis", "Data Extraction Insights", "Note Data Quality Analysis"])

    with tab1:
        # Context Introduction
        st.header('Context Introduction')
        st.write('''
                - Here you will find an analysis of the quality of notes taken and other data attributes extracted during the recruitment process. 
                - This analysis helps in understanding the depth and relevance of the information captured 
                about candidates, which in turn aids in making informed hiring decisions.
                ''')
        
    with tab2:
        st.header('Categories Table and Rationale')
        st.write('''
        - In our analysis, we initially extracted all job orders placed from the start of 2023, as recorded in Bullhorn, amounting to over 335 job orders across various categories. 

        - To enhance our understanding and derive more insightful data distribution, we consolidated similar categories. 
                
        - This process reduced the total of 70 categories to 23 distinct categories, streamlining our analysis focus and ensuring a robust examination of the data.

        - Below is an illustration showing the consolidation results, highlighting the categories and the count of job orders within each. 
        ''')


        # Data from OCR transcription
        data = {
            'Major Category': [
                'Salesforce CRM & Sales Systems', 'Development', 'Data Science & Analytics',
                'Network & Systems Engineering', 'ERP & Enterprise Solutions', 'Product & Project Management',
                'Crypto/Blockchain', 'Finance & Fintech', 'Cybersecurity', 'Other',
                'Marketing & Sales', 'Human Resources', 'Support & Help Desk', 'Business & Data Analysis',
                'Cloud & Infrastructure', 'Leadership & Management', 'Administrative', 'Quality Assurance',
                'Architecture & System Design', 'Consulting & Strategy', 'Technical Consultancy', 
                'Design & User Experience', 'Technical Support'
            ],
            'Sub-Categories': [
                'Salesforce', '.NET, Android, App Dev Manager, C++, DevOps, Developer, Front End Dev, Java, Mobile, Mulesoft, PHP, Python, Rust, ServiceNow, Software Engineer',
                'Data', 'Network Engineer, Network/systems', 'Dynamics, ERP, NetSuite, Oracle, SAP, Workday',
                'Product Manager, Program Manager, Project Manager', 'Blockchain, Crypto', 'Accounting/Finance, Fintech, Portfolio Manager, Quant, Trader',
                'Security', 'Contractor, Customer Activity Repository, Functional, HGT, Opportunistic, Order Management Systems, Other',
                'Account Manager, Marketing, Sales', 'Human Resources, Recruiter, Recruiter - Client, Recruiter - Internal, Sourcer',
                'Desktop Support, Support', 'Business Analyst', 'Cloud, Cloud Architect',
                'Management, ScrumMaster / Coach, Solutions Manager', 'Admin, Administrator', 'QA/Tester, SDET',
                'Architect, Enterprise Architect, Solution Architect', 'Consultant', 'Technical', 'UI/UX',
                'Audio Video Engineer'
            ],
            'Count': [
                191, 188, 112, 111, 104, 104, 70, 60, 58, 44, 44, 34, 28, 24, 19, 19, 16, 13, 10, 9, 9, 7, 1
            ]
        }

        # Create the DataFrame
        categories_df = pd.DataFrame(data)
        categories_df.index = categories_df.index + 1

        # Streamlit code to display the DataFrame as a table
        st.header('Job Order Categories and Counts')
        with st.expander("Job Order Categories and Counts Table"):
            st.table(categories_df)

        st.header('Rationale for Category Selection')

        st.write('''
        - For a detailed exploration of notes data, we specifically focused on 10 categories based on expertise we possess. 
        - This targeted approach allows us to dive deeper into the data, ensuring a thorough analysis.

        Selected categories for detailed analysis include:
        - **Development**
        - **Data Science and Analytics**
        - **Networks and Systems Engineering**
        - **Program and Project Management**
        - **Blockchain and Cryptocurrency**
        - **Finance and Fintech**
        - **Security**
        - **Marketing and Sales**
        - **Support**
        - **Leadership and Management**
        - **UI/UX Design**
        ''')


    with tab3:
        st.header('Data Extraction from Notes')

        st.write("""
                A thorough data extraction process has been undertaken for 128 candidates, yielding both direct and indirect insights which contribute to a holistic understanding of each profile.


                """)

        # Define the attributes for each column
        direct_data_extraction = [
            "Candidate Placement Reasons",
            "Interview Summary",
            "Recruiter Comments",
            "Client Comments",
            "Relocation Information",
            "Salary Expectations",
            "Remote Work Preference"
        ]

        indirect_data_extraction = [
            "Role Fit",
            "Recruiter Sentiment",
            "Client Sentiment",
            "Behavioral Assessment",
            "Technical Skills",
            "Communication Skills",
            "Candidate Attitude",
            "Personal Traits",
            "Soft Skills",
            "Cultural Fit",
            "Team Fit",
            "Engagement Level"
        ]

        data_quality_attributes = [
            "Note Quality",
            "Comment Presence",
            "Comment Length",
            "Relevance of Comments",
            "Specificity of Comments",
            "Improvement Suggestions"
        ]

        # Find the max length of the lists to standardize the DataFrame shape
        max_length = max(len(direct_data_extraction), len(indirect_data_extraction), len(data_quality_attributes))

        # Standardize the lengths of all lists
        direct_data_extraction += [''] * (max_length - len(direct_data_extraction))
        indirect_data_extraction += [''] * (max_length - len(indirect_data_extraction))
        data_quality_attributes += [''] * (max_length - len(data_quality_attributes))

        # Create a DataFrame
        data_extraction_df = pd.DataFrame({
            "Direct Data Extraction Attributes": direct_data_extraction,
            "Indirect/Inferred Data Extraction Attributes": indirect_data_extraction,
            "Data Quality Attributes": data_quality_attributes
        })

        data_extraction_df.index = data_extraction_df.index + 1

        # Display the DataFrame as a table in Streamlit
        # st.header('Data Extraction from Notes')
        st.table(data_extraction_df)



    with tab4:
        
        # First plot: Distribution of Quality Ratings for Commenting Persons
        st.header('1. Note level - Distribution of Quality of notes')
        
        with st.expander("1. Note level - Distribution of Quality of notes"):


            quality_counts = structured_commenting_persons_df['quality'].value_counts().reset_index()
            quality_counts.columns = ['quality', 'count']

            # Create the pie chart using Plotly
            fig = px.pie(quality_counts, values='count', names='quality', ) #title='Distribution of Quality Ratings'
            fig.update_layout(
                        width=800,  # Width of the chart
                        height=600,  # Height of the chart
                        margin=dict(l=20, r=20, t=20, b=20),  # Optional: Adjust margins to fit layout
                            legend=dict(
                                x=0.85,  # Horizontally move the legend closer to the chart
                                y=0.7,  # Vertically align the legend at the middle
                                font=dict(size=20)  # Increase the font size
                            )
                    )
            # Display the pie chart in Streamlit
            st.plotly_chart(fig, use_container_width=True, theme="streamlit")
            # Assuming 'fig' is your Plotly figure object
            # fig.write_html('chart1.html')






        
        st.header('2. Quality of notes Across Action Stages')
        with st.expander('2. Quality of notes Across Action Stages'):

            # Preparing data for Quality Across Action Stages visualization
            action_stages = structured_commenting_persons_df['action stages'].dropna().apply(eval)
            quality_ratings = structured_commenting_persons_df.loc[action_stages.index, 'quality']
            flattened_actions = [(action, quality) for actions, quality in zip(action_stages, quality_ratings) for action in actions]
            action_df = pd.DataFrame(flattened_actions, columns=['Action Stage', 'Quality'])


            # Correct mapping of all unique stages to the 7 categories
            correct_consolidated_categories = {
                'Submitted': [
                    'Submitted', 'Account Manager Feedback', 'Account Manager Rejected',
                    'Candidate Availability', 'Candidate Feedback', 'Candidate Not Interested',
                    'Contacted', 'Conversation',
                    'Note from Recruiter', 'Note from Sourcer', 'Prospect Touch', 'Qualifying Call', 'Sales Call'
                ],
                'Client Submission': ['Client Submission', 'Client Availability', 'Client Feedback', 'Client Interview Request', 'Client Rejected / Passed',],
                'Initial Screen Scheduled': ['Initial Screen Scheduled'],
                'Interview Scheduled': ['Interview Scheduled'],
                'Offer Extended': ['Offer Extended'],
                'Offer Accepted': ['Offer Accepted'],
                'Placed': ['Placed']
            }

            # Invert the mapping dictionary
            stage_to_consolidated_category = {stage: consolidated 
                                            for consolidated, stages in correct_consolidated_categories.items() 
                                            for stage in stages}

            # Map the action stages to the consolidated categories
            structured_commenting_persons_df['Consolidated Action Stages'] = structured_commenting_persons_df['action stages'].apply(
                lambda stages: [stage_to_consolidated_category.get(stage, 'Other') for stage in eval(stages)]
            )

            # We need to flatten the list and remove duplicates
            flattened_consolidated_actions = [
                (action, quality) 
                for actions, quality in zip(structured_commenting_persons_df['Consolidated Action Stages'], structured_commenting_persons_df['quality']) 
                for action in set(actions)  # Use set to remove duplicates
            ]

            # Create a DataFrame from the flattened list
            consolidated_action_df = pd.DataFrame(flattened_consolidated_actions, columns=['Consolidated Action Stage', 'Quality'])

            # Ensure the order of quality categories for plotting
            quality_order = ['good', 'ok', 'bad']
            
                # Define the desired order of the stages
            stage_order = [
                'Submitted', 'Client Submission', 'Initial Screen Scheduled',
                'Interview Scheduled', 'Offer Extended', 'Offer Accepted', 'Placed'
            ]

            # Count the occurrences for each 'Consolidated Action Stage' and 'Quality' combination
            action_counts = consolidated_action_df.groupby(['Consolidated Action Stage', 'Quality']).size().reset_index(name='count')

            # Create the bar plot using Plotly Express
            fig2 = px.bar(action_counts, x='Consolidated Action Stage', y='count', color='Quality',
                        category_orders={'Consolidated Action Stage': stage_order, 'Quality': quality_order},
                        labels={'count':'Count', 'Consolidated Action Stage':'Action Stage', 'Quality':'Quality'})

            # Update the layout to make the plot similar to the Seaborn plot
            fig2.update_layout(
                xaxis_title='Action Stage',
                yaxis_title='Count',
                legend_title='Quality',
                xaxis_tickangle=-45,
                legend=dict(
                    yanchor="top",
                    # y=0.99,
                    xanchor="left",
                    x=0.85,  # Horizontally move the legend closer to the chart
                    y=0.7,  # Vertically align the legend at the middle
                ),
                legend_font_size=20,
                font=dict(size=20, color="RebeccaPurple"),
                width=800,
                height=800
            )

            # Display the plot in Streamlit
            st.plotly_chart(fig2, use_container_width=True, theme="streamlit")
            # Assuming 'fig' is your Plotly figure object
            # fig2.write_html('chart2.html')


    

        st.header('3. Individual Recriter Note Quality Levels')
        with st.expander('3. Individual Recriter Note Quality Levels'):
            # For the commenter names, we anonymize them by showing only the first name and the initial of the last name
            structured_commenting_persons_df['Anonymized Recruiter'] = structured_commenting_persons_df['Commenter'].apply(
                lambda name: name.split()[0] + ' ' + name.split()[-1][0] + '.' if len(name.split()) > 1 else name
            )

                    # Create a new DataFrame for plotting that counts the occurrences
            plot_df = structured_commenting_persons_df.groupby(['Anonymized Recruiter', 'quality']).size().reset_index(name='Count')

            # Create the bar plot using Plotly Express
            fig = px.bar(plot_df, x='Anonymized Recruiter', y='Count', color='quality',
                        category_orders={'quality': quality_order},
                        # color_discrete_map=quality_colors,
                        ) # title='Per Person Quality Levels'

            # Update the layout to make the plot similar to the Seaborn plot
            fig.update_layout(
                xaxis_title='Recruiter',
                yaxis_title='Count',
                legend_title='Quality',
                xaxis_tickangle=-45,
                legend=dict(
                    yanchor="top",
                    # y=0.99,
                    xanchor="left",
                                x=0.85,  # Horizontally move the legend closer to the chart
                                y=0.7,  # Vertically align the legend at the middle
                ),
                # Optionally adjust font size and legend size
                legend_font_size=20,
                font=dict(size=20, color="RebeccaPurple"),
                # Set the width and height if needed
                width=800,
                height=800
            )

            # Display the plot in Streamlit
            st.plotly_chart(fig, use_container_width=True, theme="streamlit")
            # Assuming 'fig' is your Plotly figure object
            # fig.write_html('chart3.html')


