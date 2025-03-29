import os
import subprocess

import pandas as pd
import streamlit as st

def main():
    # Streamlit app interface
    st.title(
        "DeepCoSI: a Structure-based Deep Graph Learning Network Method for Covalent Binding Site Identification"
    )
    
    # Add links to the GitHub repository and journal article
    st.markdown(
        """
        [GitHub Repository](https://github.com/Brian-hongyan/DeepCoSI)  
        [Journal Article: Covalent Binding Site Identification](https://spj.science.org/doi/10.34133/2022/9873564)
        """
    )
    
    # Step 1: Upload PDB file
    st.header("Step 1: Upload a PDB File")
    uploaded_file = st.file_uploader("Choose a PDB file", type="pdb")
    
    # Step 2: Specify job name
    st.header("Step 2: Enter a Job Name")
    job_name = st.text_input("Job Name", "my_job")
    
    # Optional: Number of processors
    n_processors = os.cpu_count()
    
    # Step 3: Run the script
    if st.button("Run DeepCoSI Script"):
        if uploaded_file is not None and job_name:
            # Save the uploaded file temporarily
            pdb_file_path = f"/mnt/data2/GitHub/DeepCoSI/{uploaded_file.name}"
            os.makedirs(os.path.dirname(pdb_file_path), exist_ok=True)
            with open(pdb_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File {uploaded_file.name} uploaded successfully!")
    
            # Construct the command to run the script with the arguments
            command = [
                "/mnt/data2/GitHub/DeepCoSI/codes/DeepCoSI_prediction.py",
                uploaded_file.name,
                job_name,
                "--n",
                str(n_processors),
            ]
    
            st.write("Running DeepCoSI script with the following command:")
            st.code(" ".join(command))
    
            # Execute the command
            result = subprocess.run(command, capture_output=True, text=True)
    
            # Display the result
            if result.returncode == 0:
                st.success("Job completed successfully!")
    
                # Display results (for example, the generated result CSV)
                result_csv_path = f"/mnt/data2/GitHub/DeepCoSI/build/{job_name}_result.csv"
                if os.path.exists(result_csv_path):
                    st.write("Results:")
                    df = pd.read_csv(result_csv_path, index_col=0)
                    st.dataframe(df)
    
                    # Allow downloading of the result CSV
                    with open(result_csv_path, "rb") as f:
                        st.download_button(
                            label="Download Results CSV",
                            data=f,
                            file_name=f"{job_name}_result.csv",
                            mime="text/csv",
                        )
                else:
                    st.error("Result file not found.")
            else:
                st.error(f"Error running the script: {result.stderr}")
        else:
            st.error("Please upload a PDB file and specify a job name.")

if __name__ == "__main__":
    main()
