# --------------------------------------------------
# # VOICE
# # --------------------------------------------------

# elif st.session_state.step == 2:

#     voice_page()

#     col1, col2, col3 = st.columns([2, 4, 2])

#     with col1:
#         if st.button("⬅ Back"):
#             previous_step()
#             st.rerun()

#     with col3:
#         if st.button("Skip ➜"):
#             st.session_state.results["voice"] = "Skipped"
#             next_step()
#             st.rerun()

# # --------------------------------------------------
# # FINGER TAPPING
# # --------------------------------------------------

# elif st.session_state.step == 3:

#     fingertap_page()

#     col1, col2, col3 = st.columns([2, 4, 2])

#     with col1:
#         if st.button("⬅ Back"):
#             previous_step()
#             st.rerun()

#     with col3:
#         if st.button("Finish ➜"):
#             next_step()
#             st.rerun()

# # --------------------------------------------------
# # SUMMARY
# # --------------------------------------------------

# else:

#     summary_page()
