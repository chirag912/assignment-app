import requests
import pandas as pd
import streamlit as st
import openai  # Assuming you have the openai library installed

# Set your OpenAI API key
openai.api_key = "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"




def generate_assignment(topic, domain):
    prompt = f"Generate an assignment on {topic} in the domain of {domain}.\n\n" \
             "Problem Statement:\n" \
             "Description and Details of the Assignment:\n" \
             "Learning Outcomes from the Assignment:\n" \
             "Steps to Solve the Assignment or Method to Solve:\n" \
             "Links to Datasets for the Assignment:\n" \
             "Please provide a step-by-step breakdown of how a student should approach and solve the assignment:\n"


    response = openai.Completion.create(
        engine="text-davinci-003",  # Choose the appropriate engine
        prompt=prompt,
        max_tokens=2000  # Adjust the max tokens as needed
    )
    return response.choices[0].text


def solve_errors(errors_input):
    prompt = f"Solve the following errors related to the dataset:\n{errors_input}"

    response = openai.Completion.create(
        engine="text-davinci-003",  # Choose the appropriate engine
        prompt=prompt,
        max_tokens=100  # Adjust the max tokens as needed
    )
    return response.choices[0].text

def generate_eda_suggestions(dataset_info):
    prompt = f"Tell what Exploratory Data Analysis we can do based on the dataset:\n{dataset_info}" \
             f"How can the student apply the assignment based on the topic and dataset?\n"

    response = openai.Completion.create(
        engine="text-davinci-003",  # Choose the appropriate engine
        prompt=prompt,
        max_tokens=2000  # Adjust the max tokens as needed
    )
    return response.choices[0].text


def display_csv_upload():
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file:
        dataframe = pd.read_csv(uploaded_file)
        first_10_rows = dataframe.head(20)
        eda_suggestions = generate_eda_suggestions(first_10_rows)
        st.subheader("Exploratory Data Analysis Suggestions:")
        st.write(eda_suggestions)


def main():
    st.title("Student Assignment Generator")

    name = st.text_input("Name")
    topic = st.text_input("Topic you learned in lecture")
    domain = st.text_input("Domain for the assignment")

    if st.button("Generate Assignment"):
        if topic and domain:
            assignment = generate_assignment(topic, domain)

            st.subheader("Generated Assignment:")
            st.write(assignment)

            st.subheader("Additional Details:")
            # ... (other details)

            st.subheader("Errors Faced:")
            errors = st.text_area("Details of Errors")

            if errors and st.button("Solve Errors"):
                solution = solve_errors(errors)
                st.subheader("Solution for Errors:")
                st.write(solution)

    # Call the CSV upload function here
    display_csv_upload()


if __name__ == "__main__":
    main()
