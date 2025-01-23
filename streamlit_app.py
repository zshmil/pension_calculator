import streamlit as st

st.title("🎈 מחשבון פנסיה")
# st.write(
#     "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
# )

class StreamlitHelper:
    @staticmethod
    def get_user_inputs():
        """
        Collect Pension details via Streamlit UI.
        Returns:
            dict: A dictionary containing user input values.
        """
        # st.title("AppLovin Campaign Manager")
        with st.form("חישוב פנסיה לשכיר"):
            salary = st.text_input(" שכר חודשי (ברוטו) *", placeholder="לדוגמה: 15,000")
            current_balance = st.text_input("צבירה נוכחית *", placeholder="לדוגמה: 300,000")
            current_age = st.text_input("גיל", placeholder="לדוגמא: 30")
            retirement_age = st.text_input("גיל פרישה", placeholder='''נשים 64, גברים 67 (ניתן לפרוש בגיל מאוחר יותר, הפנסיה היא רק מגיל הפרישה כך שלא ניתן לקבל קצבה לפני גיל הפרישה)''') #input('When Are You Planning To Retire?: ').strip()
            employee_deposit = st.text_input("אחוז הפקדה של העובד", placeholder='''(אפשר ואפילו מומלץ להגדיל ל7%) בד"כ 6%''')
            employer_deposit = st.text_input("אחוז הפקדה של המעסיק", placeholder='''בד"כ 6.5%''')
            
            submitted = st.form_submit_button("Submit")
    
        if submitted and campaign_name:
            return {
                "salary": salary.strip(),
                "current_balance": float(current_balance.strip()),
                "current_age": int(current_age.strip() if creative_set_description.strip()) else None,
                "retirement_age": int(etirement_age.strip() if product_page.strip()) else None,
                "employee_deposit": float(employee_deposit.strip() if product_page.strip()) else 6.0,
                "employer_deposit": float(employer_deposit.strip() if product_page.strip()) else 6.5,
               
            }
        else:
            st.warning("יש למלא את כל הפרטים לפני השליחה")
            return None
