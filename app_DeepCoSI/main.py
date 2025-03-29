import os
import subprocess

import streamlit as st


def main():
    st.title(
        "DeepCoSI: a Structure-based Deep Graph Learning Network Method for Covalent Binding Site Identification"
    )

    st.markdown(
        """
        [GitHub Repository](https://github.com/Brian-hongyan/DeepCoSI)  
        [Journal Article: Covalent Binding Site Identification](https://spj.science.org/doi/10.34133/2022/9873564)
        """
    )

    # Step 1: Upload PDB file
    st.header("Step 1: Upload a PDB File")
    uploaded_file = st.file_uploader("Choose a PDB file", type="pdb")

    # Optional: Number of processors
    n_processors = os.cpu_count()

    # Step 2: Run the script (job name derived automatically)
    if st.button("Run DeepCoSI Script"):
        if uploaded_file is not None:
            # Derive job name from the uploaded file name (strip any path and .pdb extension)
            job_name = os.path.splitext(os.path.basename(uploaded_file.name))[
                0
            ]
            st.write(f"Job name derived from uploaded file: **{job_name}**")

            # Save the uploaded file temporarily
            pdb_file_path = (
                f"app_DeepCoSI/uploads/{os.path.basename(uploaded_file.name)}"
            )
            os.makedirs(os.path.dirname(pdb_file_path), exist_ok=True)
            with open(pdb_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File {uploaded_file.name} uploaded successfully!")

            # Construct the command to run the script with the arguments
            command = [
                "app_DeepCoSI/DeepCoSI/codes/DeepCoSI_prediction.py",
                os.path.basename(uploaded_file.name),
            ]

            st.write("Running DeepCoSI script with the following command:")
            st.code(" ".join(command))

            # Execute the command
            result = subprocess.run(command, capture_output=True, text=True)

            # Display the result
            if result.returncode == 0:
                st.success("Job completed successfully!")

                # Look for the generated zip file instead of CSV.
                result_zip_path = f"app_DeepCoSI/outputs/{job_name}_output.zip"
                if os.path.exists(result_zip_path):
                    st.write("Results:")
                    with open(result_zip_path, "rb") as f:
                        st.download_button(
                            label="Download Results ZIP",
                            data=f,
                            file_name=f"{job_name}_output.zip",
                            mime="application/zip",
                        )
                else:
                    st.error("Result file not found.")
            else:
                st.error(f"Error running the script: {result.stderr}")
        else:
            st.error("Please upload a PDB file.")


if __name__ == "__main__":
    main()
