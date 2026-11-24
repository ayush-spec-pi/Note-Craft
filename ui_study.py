import streamlit as st
from processor import process_multiple_pdfs
from transcriber import transcribe_audio
from llm_engine import generate_study_pack

SAMPLE_TRANSCRIPT = (
    "Pay very close attention here—I am spending 10 minutes repeating the AVL LR double rotation "
    "derivation because this question is a classic SEE 10-marker. When ancestor Z has BF = +2 and "
    "its left child Y has BF = -1, ALWAYS left-rotate Y first, then right-rotate Z. "
    "Mark this rubric warning: write updated balance factors beside every node or evaluators deduct 3 marks. "
    "Also remember for Infix to Postfix: exponent '^' is right-associative, so DO NOT pop an existing '^' on stack."
)


def render_study_tab(profile: dict):
    left, right = st.columns([1, 1.45], gap="large")

    # Left column: lecture and notes input card
    with left:
        with st.container(border=True):
            st.markdown(
                """
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:15px; font-weight:600; color:#111827;">Lecture &amp; Notes Capture</div>
                    <span class="nc-badge">PDF · OCR · Audio</span>
                </div>
                <div style="font-size:12px; color:#6B7280; margin-bottom:14px;">
                    Upload typed or scanned PDFs, provide lecture audio alone, or combine both.
                </div>
                """,
                unsafe_allow_html=True
            )

            mode = st.segmented_control(
                "Source Mode",
                options=["Manual Upload", "Auto-Fetch (Drive DB)"],
                default="Manual Upload",
                label_visibility="collapsed"
            )

            c_sub, c_top = st.columns(2)
            subject = c_sub.text_input("Subject", value="Data Structures & Algorithms")
            topic_keyword = c_top.text_input(
                "Specific Topic (Optional)",
                placeholder="e.g. AVL Rotation"
            )

            uploaded_pdfs = []
            if mode == "Manual Upload":
                uploaded_pdfs = st.file_uploader(
                    "Notes / PYQ PDFs (Typed or Scanned)",
                    type=["pdf"],
                    accept_multiple_files=True
                )
            else:
                st.markdown(
                    f"""
                    <div style="border:1px solid #FDE68A; background:#FFFBEB; color:#92400E; border-radius:10px; padding:12px 14px; font-size:12px; line-height:1.5; margin:6px 0 12px 0;">
                        <strong>Drive DB Scope:</strong> {profile['year']} → {profile['cycle']} → {profile['branch']}<br/>
                        Live <code>drive_catalog.json</code> sync is scheduled for the full build. Use <b>Manual Upload</b> or <b>Audio</b> to test the pipeline right now.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown(
                "<hr style='margin:14px 0; border:none; border-top:1px solid #E5E7EB;'/>",
                unsafe_allow_html=True
            )

            # Audio upload and sample transcript action row
            a_col1, a_col2 = st.columns([2.2, 1], vertical_alignment="center")
            with a_col1:
                st.markdown(
                    "<div style='font-size:13px; font-weight:600; color:#111827;'>Classroom Audio / Transcript</div>",
                    unsafe_allow_html=True
                )
                st.caption("Optional · Powered by Groq Whisper")
            with a_col2:
                if st.button("Load Sample", use_container_width=True):
                    st.session_state["transcript_input"] = SAMPLE_TRANSCRIPT

            audio_file = st.file_uploader(
                "Upload Lecture Audio (.mp3, .wav, .m4a)",
                type=["mp3", "wav", "m4a", "ogg", "webm"],
                label_visibility="collapsed"
            )

            manual_transcript = st.text_area(
                "Or paste lecture transcript / teacher hints",
                key="transcript_input",
                height=115,
                placeholder="Paste raw classroom notes or click 'Load Sample' above to test immediately..."
            )

            generate_btn = st.button(
                "Generate Smart Study Pack →",
                type="primary",
                use_container_width=True
            )

    # Right column: generated study pack workspace card
    with right:
        with st.container(border=True):
            header_status = (
                f"<span class='nc-badge nc-badge-green'><span class='nc-dot'></span>{st.session_state.get('last_model', 'Ready')}</span>"
                if "last_notes" in st.session_state
                else "<span class='nc-badge'>Awaiting Input</span>"
            )
            st.markdown(
                f"""
                <div style="display:flex; justify-content:space-between; align-items:center; padding-bottom:12px; border-bottom:1px solid #E5E7EB; margin-bottom:16px;">
                    <div>
                        <div style="font-size:16px; font-weight:600; color:#111827;">Smart Study Pack</div>
                        <div style="font-size:12px; color:#6B7280;">Exam-grounded notes, teacher emphasis &amp; 60-second recap</div>
                    </div>
                    {header_status}
                </div>
                """,
                unsafe_allow_html=True
            )

            if generate_btn:
                if not uploaded_pdfs and not audio_file and not manual_transcript.strip():
                    st.warning("Please upload at least one PDF, an audio file, or a transcript before generating notes.")
                else:
                    pdf_text = ""
                    final_transcript = manual_transcript.strip()

                    try:
                        if uploaded_pdfs:
                            with st.spinner("Scanning PDFs (Typed + RapidOCR)..."):
                                pdf_text = process_multiple_pdfs(uploaded_pdfs, topic_keyword)

                        if audio_file:
                            with st.spinner("Transcribing classroom audio via Groq Whisper..."):
                                whisper_text = transcribe_audio(audio_file)
                                final_transcript = f"{whisper_text}\n\n{final_transcript}".strip()
                                st.session_state["last_transcript"] = whisper_text

                        with st.spinner("Synthesizing Study Pack via OpenRouter..."):
                            notes_md, used_model = generate_study_pack(
                                pdf_text=pdf_text,
                                transcript=final_transcript,
                                subject=subject,
                                topic=topic_keyword
                            )
                            st.session_state["last_notes"] = notes_md
                            st.session_state["last_model"] = used_model
                            st.rerun()

                    except Exception as e:
                        st.error(f"Error: {e}")

            if "last_notes" in st.session_state:
                if st.session_state.get("last_transcript"):
                    with st.expander("View Groq Whisper Audio Transcript"):
                        st.write(st.session_state["last_transcript"])

                st.markdown(st.session_state["last_notes"])

                st.write("")
                b1, b2 = st.columns([1, 3])
                with b1:
                    st.download_button(
                        "Download .md",
                        data=st.session_state["last_notes"],
                        file_name=f"{subject.lower().replace(' ', '_')}_notes.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                with b2:
                    if st.button("Clear Workspace"):
                        st.session_state.pop("last_notes", None)
                        st.session_state.pop("last_transcript", None)
                        st.rerun()
            else:
                st.markdown(
                    """
                    <div style="background:#FAFAFA; border:1px dashed #D1D5DB; border-radius:12px; padding:28px 24px; margin-top:6px;">
                        <div class="mono" style="font-size:11px; color:#6B7280; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px;">
                            Pipeline Ready
                        </div>
                        <div style="font-size:16px; font-weight:600; color:#111827; margin-bottom:18px;">
                            Turn raw lectures &amp; messy PDFs into exam-ready revision packs.
                        </div>
                        <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:12px;">
                            <div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:10px; padding:14px;">
                                <div class="mono" style="font-size:11px; color:#6B7280;">01 · INPUT</div>
                                <div style="font-size:13px; font-weight:600; color:#111827; margin-top:4px;">Typed + Photo PDFs</div>
                                <div style="font-size:12px; color:#6B7280; margin-top:4px;">PyMuPDF + RapidOCR extracts scanned pages &amp; filters by topic.</div>
                            </div>
                            <div style="background:#FFFBEB; border:1px solid #FDE68A; border-radius:10px; padding:14px;">
                                <div class="mono" style="font-size:11px; color:#92400E;">02 · SIGNALS</div>
                                <div style="font-size:13px; font-weight:600; color:#92400E; margin-top:4px;">Teacher Spotlight</div>
                                <div style="font-size:12px; color:#78350F; margin-top:4px;">Groq Whisper captures repeated derivations &amp; exam traps.</div>
                            </div>
                            <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:10px; padding:14px;">
                                <div class="mono" style="font-size:11px; color:#166534;">03 · OUTPUT</div>
                                <div style="font-size:13px; font-weight:600; color:#166534; margin-top:4px;">Revision + Recap</div>
                                <div style="font-size:12px; color:#166534; margin-top:4px;">Structured notes, formulas &amp; a 60-sec pre-exam summary.</div>
                            </div>
                        </div>
                        <div style="margin-top:18px; font-size:12px; color:#6B7280;">
                            Tip: Click <b>Load Sample</b> in the left panel, then click <b>Generate Smart Study Pack</b>.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )