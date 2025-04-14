# importing modules
import streamlit as st
from sympy.codegen.ast import continue_

from llm import parse
import pandas as pd
import re
from io import StringIO

from scrapper import scrape_web, split_dom_cont

st.title("Web Scraper")
st.text("~By Adesh Shrivastav")
url = st.text_input("Enter Website URL")



# Add Input area Which define how many pages we need to scrape
col1, col2 = st.columns(2)
with col1:
    max_pages = st.number_input("Maximum Pages to Scrape", min_value=1, value=10)
with col2:
    max_depth = st.number_input("Maximum Depth you want to scrape in a page", min_value=1, value=3)

# Scrape content
if st.button("Scrape Web Data"):
    if "https://" not in url or "http://" not in url:
        st.error("Please make sure you have Entered a URL else it will not work")


    st.write("Scraping...")
    results = scrape_web(url, max_pages=max_pages, max_depth=max_depth)

    # Store all scraped content in session state
    st.session_state.dom_cont = "\n\n===PAGE BREAK===\n\n".join(
        f"URL: {result['url']}\nTitle: {result['title']}\nContent:\n{result['content']}"
        for result in results
    )

    # Display summary
    st.write(f"Successfully Got data of {len(results)} pages")

    # Display results in tabs instead of nested expanders
    tabs = st.tabs([f"Page {i+1}" for i in range(len(results))])
    for i, (tab, result) in enumerate(zip(tabs, results)):
        with tab:
            st.markdown(f"**URL:** {result['url']}")
            st.markdown(f"**Title:** {result['title']}")
            st.text_area(
                "Content",
                result['content'],
                height=200,
                key=f"content_{i}"
            )

# Parse content if it's available in session state
if "dom_cont" in st.session_state:
    description = st.text_area("Describe what you want to Parse from Scraped data?")

    if st.button("Parse Content") and description:
        st.write("Parsing...")

        chunks = split_dom_cont(st.session_state.dom_cont)  # Split content into chunks
        result = parse(chunks, description)  # Parse the content with the user's description

        st.write(result)
        try:
            # Convert the markdown response to a list of DataFrames
            def markdown_to_dataframe(markdown):
                # Split the markdown into separate tables based on the horizontal separator `| --- | --- | ---`
                tables = re.split(r'\| --- \| --- \| ---', markdown)

                dfs = []  # List to store DataFrames for each table

                for table in tables:
                    table = table.strip()
                    if table:
                        # Read the table into a DataFrame, treating `|` as the delimiter
                        df = pd.read_csv(StringIO(table), sep="|", engine='python', header=0)
                        df.columns = df.columns.str.strip()  # Strip extra spaces from columns
                        dfs.append(df)  # Add the dataframe to the list

                return dfs

            # Convert markdown result into DataFrames
            dataframes = markdown_to_dataframe(result)

            # Display the DataFrames
            for i, df in enumerate(dataframes, start=1):
                st.write(f"Table {i}:")
                st.write(df)

                # Convert DataFrame to CSV for download
                csv_data = df.to_csv(index=False).encode('utf-8')

                # Download button to download CSV of the DataFrame
                st.download_button(
                    label=f"Download Table {i} as CSV",
                    data=csv_data,
                    file_name=f"table_{i}.csv",
                    mime="text/csv"
                )
        except Exception as e:
            st.write("Facing the error converting output to Data Frame Please Try again")

