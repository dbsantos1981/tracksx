import streamlit as st
import subprocess
import os
import base64

def down(bin_file, file_label='File'):
    # how to download files with markdown links
    # https://discuss.streamlit.io/t/how-to-download-mp3-directly-not-open-a-web-play/6824/2
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()

    # as button
    # href = f'<a class="css-1cpxqw2 edgvbvh9" style="text-decoration: none;" href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    
    # as common link
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" style="text-decoration: none;" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    
    return href

# welcome
st.title("TracksX")
st.write("Now you can from your music MP3 files generate separate tracks like **_vocals, drums, bass and others_**.")
st.markdown('***')

# upload file
st.header("🎵 Upload your music file!")
uploaded_mp3_file = st.file_uploader("Upload your MP3 file here:",type=['mp3'])
st.markdown('***')

# get file
if uploaded_mp3_file != None:
    content = uploaded_mp3_file.getbuffer()
    new_file = 'temporary_files/' + uploaded_mp3_file.name
    with open(new_file, 'wb') as f:
        f.write(content)
        
    # display uploaded file data:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.subheader('File Name')
        st.write(uploaded_mp3_file.name)
    with col2:
        st.subheader('File Size')
        st.write(f'{uploaded_mp3_file.size/1024/1024:.2f} MB')
    with col3:
        st.subheader('File Type')
        st.write(uploaded_mp3_file.type)
    with col4:
        st.subheader('File ID') 
        st.write(uploaded_mp3_file.id)

    # uploaded file player
    st.markdown('🎧 Listen uploaded file:')
    with open(new_file, 'rb') as f:
        st.audio(f, format="audio/mp3")
    st.markdown('***')

    # rip file form
    with st.form("rip_form"):
        st.subheader('🎶 Choose separate type')
        tracks = st.radio(
            "Choose which tracks you want to rip:", (
            '🎤 vocals / 🎼 accompaniment',
            '🎤 vocals / 🎸 bass / 🥁 drums / 🎼 other',
            )
        )
        delete_mp3_file = st.checkbox("🗑️ Delete uploaded file after process?")
        submitted = st.form_submit_button("Create tracks!")
    
    # on form submit
    if submitted:
        st.subheader('💽 Extracting the tracks...')
        result_area = st.empty()
        with result_area.container():
            st.caption('Please be patient... As soon as possible we can have the progress of the process here.\
                For now see the movement of the icon in the upper right corner of the screen.\
                    if the program crashes, close and start again.')

        # selection of tracks
        cmd = ''
        if tracks == '🎤 vocals / 🎼 accompaniment':
            cmd = f'spleeter separate --verbose --codec mp3 "temporary_files\\{uploaded_mp3_file.name}" -p spleeter:2stems -o "separate_files"'
            result = subprocess.run(cmd, capture_output=True, text=True)
        elif tracks == '🎤 vocals / 🎸 bass / 🥁 drums / 🎼 other':
            cmd = f'spleeter separate --verbose --codec mp3 "temporary_files\\{uploaded_mp3_file.name}" -p spleeter:4stems -o "separate_files"'
            result = subprocess.run(cmd, capture_output=True, text=True)

        # get spleeter results
        try:
            result.check_returncode()

        except subprocess.CalledProcessError as e:
            raise e

        # results analyze
        result_area.empty()
        if 'written succesfully' in result.stdout:
            with result_area.container():
                # Path Separate Files
                psf = f'{os.getcwd()}\separate_files\{uploaded_mp3_file.name[:-4]}'
                st.success(f"Job completed successfully! Access the new tracks in the '{psf}' folder or below")
                
                st.markdown('Listen to the new files! **(To download click on the link above the corresponding player)**:')

                # vocals
                vocals = f'separate_files/{uploaded_mp3_file.name[:-4]}/vocals.mp3'
                download_link = down(vocals, '')
                st.markdown(f'🎤 Vocals {download_link}', unsafe_allow_html=True)
                with open(vocals, 'rb') as f:
                    st.audio(f, format="audio/mp3")
                # st.markdown('🎤 Vocals')
                # vocals = f'separate_files/{uploaded_mp3_file.name[:-4]}/vocals.mp3'
                # with open(vocals, 'rb') as f:
                #     st.audio(f, format="audio/mp3")
                # st.markdown(down(vocals, 'Vocals'), unsafe_allow_html=True)
                
                if tracks == '🎤 vocals / 🎼 accompaniment':
                    # accompaniment
                    accompaniment = f'separate_files/{uploaded_mp3_file.name[:-4]}/accompaniment.mp3'
                    download_link = down(accompaniment, '')
                    st.markdown(f'🎼 Accompaniment {download_link}', unsafe_allow_html=True)
                    with open(accompaniment, 'rb') as f:
                        st.audio(f, format="audio/mp3")
                    # st.markdown('🎼 Accompaniment')
                    # accompaniment = f'separate_files/{uploaded_mp3_file.name[:-4]}/accompaniment.mp3'
                    # with open(accompaniment, 'rb') as f:
                    #     st.audio(f, format="audio/mp3")
                    # st.markdown(down(accompaniment, 'Accompaniment'), unsafe_allow_html=True)

                else:
                    # bass
                    accompaniment = f'separate_files/{uploaded_mp3_file.name[:-4]}/bass.mp3'
                    download_link = down(accompaniment, '')
                    st.markdown(f'🎸 Bass {download_link}', unsafe_allow_html=True)
                    with open(accompaniment, 'rb') as f:
                        st.audio(f, format="audio/mp3")
                    # st.markdown('🎸 Bass')
                    # accompaniment = f'separate_files/{uploaded_mp3_file.name[:-4]}/bass.mp3'
                    # with open(accompaniment, 'rb') as f:
                    #     st.audio(f, format="audio/mp3")
                    # st.markdown(down(accompaniment, 'Bass'), unsafe_allow_html=True)
                        # btn = st.download_button(label="Download Bass.mp3", data=f, file_name="bass.mp3", mime="audio/mp3")

                    # drums
                    accompaniment = f'separate_files/{uploaded_mp3_file.name[:-4]}/drums.mp3'
                    download_link = down(accompaniment, '')
                    st.markdown(f'🥁 Drums {download_link}', unsafe_allow_html=True)
                    with open(accompaniment, 'rb') as f:
                        st.audio(f, format="audio/mp3")
                    # st.markdown('🥁 Drums')
                    # accompaniment = f'separate_files/{uploaded_mp3_file.name[:-4]}/drums.mp3'
                    # with open(accompaniment, 'rb') as f:
                    #     st.audio(f, format="audio/mp3")
                    #     # btn = st.download_button(label="Download Drum.mp3", data=f, file_name="drum.mp3", mime="audio/mp3")
                    # st.markdown(down(accompaniment, 'Drums'), unsafe_allow_html=True)

                    # other
                    # st.markdown('🎼 Other')
                    # accompaniment = f'separate_files/{uploaded_mp3_file.name[:-4]}/other.mp3'
                    # with open(accompaniment, 'rb') as f:
                    #     st.audio(f, format="audio/mp3")
                    #     # btn = st.download_button(label="Download Other.mp3", data=f, file_name="other.mp3", mime="audio/mp3")
                    # st.markdown(down(accompaniment, 'Other'), unsafe_allow_html=True)
                    
                    # other
                    accompaniment = f'separate_files/{uploaded_mp3_file.name[:-4]}/other.mp3'
                    download_link = down(accompaniment, '')
                    st.markdown(f'🎼 Other {download_link}', unsafe_allow_html=True)
                    with open(accompaniment, 'rb') as f:
                        st.audio(f, format="audio/mp3")

                st.markdown('***')
        else:
            with result_area.container():
                st.error(f"Work finished with errors... {result.stderr}")

        # delete original file?
        if delete_mp3_file:
            if os.path.exists(new_file):
                os.remove(new_file)
                if not os.path.exists(new_file):
                    st.success(f'The temp file {uploaded_mp3_file.name} was successfully deleted.')
                else:
                    st.error(f'Something went wrong when trying to delete file {uploaded_mp3_file}.')
            else:
                st.error(f'Something went wrong when trying to delete file {uploaded_mp3_file}.')
        else:
            st.warning(f"The file {uploaded_mp3_file.name} is still in folder 'temporary_files'. You can manually delete it.")
        

            