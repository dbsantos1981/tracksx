import streamlit as st
import subprocess

st.title("TracksX")
st.write("You can from your music MP3 files generate separate tracks like **_vocals, drums, bass, piano and others_**.")

with st.form("form_upload"):

    uploaded_mp3_file = st.file_uploader("Upload your MP3 file here:",type=['mp3'])

    tracks = st.radio(
        "Choose which tracks you want to rip:", (
        'vocals / accompaniment',
        'vocals / bass / drums / other',
        'vocals / bass / drums / piano / other'
        )
    )

    delete_mp3_file = st.checkbox("Delete uploaded file after process?")

    submitted = st.form_submit_button("Create tracks!")

# on form submit
if submitted:

    # write uploaded file in temp folder and more
    try:
        content = uploaded_mp3_file.getbuffer()
        new_file = 'temp/' + uploaded_mp3_file.name
        with open(new_file, 'wb') as f:
            f.write(content)
        
        # display uploaded file data:
        st.subheader('Original File')
        st.write(
            "**Original file:** ", uploaded_mp3_file.name,
            "**Size:** ", uploaded_mp3_file.size,
            " bytes  **Type:** ", uploaded_mp3_file.type,
            "**ID:** ", uploaded_mp3_file.id
        )

        # uploaded file player
        with open(new_file, 'rb') as f:
            st.audio(f, format="audio/mp3")

        # selection of tracks
        st.subheader('Extracting the tracks')
        if tracks == 'vocals / accompaniment':
            args = 'spleeter separate --codec mp3 "temp\QuemEvoce.mp3" -p spleeter:4stems -o "temp"'
            result = subprocess.run(args, capture_output=True, text=True)
            try:
                result.check_returncode()
                st.info(result.stdout)
                """
                resultado comando acima
                INFO:spleeter:File temp\QuemEvoce/bass.mp3 written succesfully INFO:spleeter:File temp\QuemEvoce/other.mp3 written succesfully INFO:spleeter:File temp\QuemEvoce/vocals.mp3 written succesfully INFO:spleeter:File temp\QuemEvoce/drums.mp3 written succesfully
                """
            except subprocess.CalledProcessError as e:
                st.error(result.stderr)
                raise e
            # with st.spinner:
            # out = subprocess.run('spleeter separate --codec mp3 "temp\QuemEvoce.mp3" -p spleeter:4stems -o "temp"')
            # st.text(type(out), out)
            # if 'returncode=0' in out:
            #     st.success('Tracks extracted successfully!')
            # else:
            #     st.error(f'Error in extraction: {out}')
            #to aqui, é hora de acionar o spleeter
            # from spleeter.separator import Separator
            # separator = Separator('spleeter:4stems')
            # with st.spinner:
            #     separator.separate_to_file(uploaded_mp3_file, '/temp')
            
            # st.success('Done!')
            # import time
            # my_bar = st.progress(0)
            # for percent_complete in range(100):
            #     time.sleep(0.1)
            #     my_bar.progress(percent_complete + 1)
            #             
            
            # spleeter separate --codec mp3 obedecer.mp3 -p spleeter:4stems --verbose -o "c:\Users\Daniel Bezerra\Music"
            # gerou uma pasta com mp3 mas a bateria nao gerou o arquivo. o audio saiu meio zoado
            # spleeter separate --codec mp3 obedecer.mp3 -p spleeter:5stems --verbose -o "c:\Users\Daniel Bezerra\Music"
            # linha final com a maxima qualidade apos alteracao do arquivo json para 1920 no campo F
            # spleeter separate --codec mp3 Lazaro.mp3 -p spleeter:5stems-16kHz --verbose -o "c:\Users\Daniel Bezerra\Music"

            #spleeter separate --codec mp3 "temp\Obedecer.mp3" -p spleeter:5stems-16kHz --verbose -o "temp"

        elif tracks == 'vocals / bass / drums / other':
            pass

        elif tracks == 'vocals / bass / drums / piano / other':
            pass

    except:
        st.error("Upload error or corrupt file. Re-upload file and try again.")