import streamlit as st


st.markdown("""
<style>
body, html {
    direction: RTL;
    unicode-bidi: bidi-override;
    text-align: right;
}
p, div, input, label, h1, h2, h3, h4, h5, h6 {
    direction: RTL;
    unicode-bidi: bidi-override;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)


st.title("🎈 מחשבון פנסיה")
# st.write(#"Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."# )


class StreamlitHelper:
    @staticmethod
    def get_user_inputs():
        """
        Collect Pension details via Streamlit UI.
        Returns:
            dict: A dictionary containing user input values.
        """
        with st.form("חישוב פנסיה לשכיר"):
            salary = st.text_input(" *שכר חודשי (ברוטו)", placeholder=" לדוגמה: 15,000 ")
            current_balance = st.text_input(" *צבירה נוכחית", placeholder=" לדוגמה: 300,000 ")
            current_age = st.text_input(" *גיל", placeholder="לדוגמא:  30 ")
            retirement_age = st.text_input(" *גיל פרישה", placeholder=" נשים 64, גברים 67 ")
            employee_deposit = st.text_input("אחוז הפקדה של העובד",placeholder=" בדרך כלל 6% (אפשר ואפילו מומלץ להגדיל ל-7%) ")
            employer_deposit = st.text_input("אחוז הפקדה של המעסיק",placeholder=" בדרך כלל 6.5% ")
            submitted = st.form_submit_button("חשב פנסיה")

        if submitted:
            # Ensure required fields are filled
            if not salary or not current_balance:
                st.warning("יש למלא את כל הפרטים המסומנים בכוכבית לפני השליחה")
                return None
            
            try:
                # Convert input values and set defaults if necessary
                return {
                    "salary": float(salary.replace(',', '').strip()) if salary.strip() else 0.0,
                    "current_balance": float(current_balance.replace(',', '').strip()) if current_balance.strip() else 0.0,
                    "current_age": int(current_age.strip()) if current_age.strip() else None,
                    "retirement_age": int(retirement_age.strip()) if retirement_age.strip() else None,
                    "employee_deposit": float(employee_deposit.strip()) if employee_deposit.strip() else 6.0,
                    "employer_deposit": float(employer_deposit.strip()) if employer_deposit.strip() else 6.5,
                }
            except ValueError:
                st.error("נא לוודא שהזנתם מספרים תקינים")
                return None
        else:
            return None

# # Run the input form and store the results
# pension_data = StreamlitHelper.get_user_inputs()

# # Display the collected data
# if pension_data:
#     st.success("פרטי הפנסיה שהוזנו:")
#     st.write(pension_data)


def main():
    """
    """
    # Run the input form and store the results
    pension_data = StreamlitHelper.get_user_inputs()

    # Display the collected data
    if pension_data:
        st.success("פרטי הפנסיה שהוזנו:")
        st.write(pension_data)

if __name__ == "__main__":
    main()
