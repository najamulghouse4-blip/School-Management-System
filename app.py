"""
The Registrar's Desk — a school management system
Built on the original Student/Teacher OOP model, wrapped in a Streamlit UI.
"""

import json
from abc import ABC, abstractmethod
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

DATABASE = "school_data.json"

# ----------------------------------------------------------------------------
# Data layer
# ----------------------------------------------------------------------------

def load_data():
    if Path(DATABASE).exists():
        with open(DATABASE, "r") as f:
            content = f.read()
            if content:
                return json.loads(content)
    return {"students": [], "teachers": []}


def save_data(data):
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)


if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data


# ----------------------------------------------------------------------------
# OOP layer — same shape as the original console program, adapted so methods
# take arguments and return (ok, message) instead of calling input()/print()
# ----------------------------------------------------------------------------

class Persons(ABC):
    @abstractmethod
    def get_role(self):
        pass

    @abstractmethod
    def register(self, **kwargs):
        pass

    @abstractmethod
    def show_details(self, identifier):
        pass

    @staticmethod
    def validate_email(e_mail):
        return "@" in e_mail and "." in e_mail


class Student(Persons):
    def get_role(self):
        return "Student"

    def find(self, roll_no):
        for s in data["students"]:
            if s["roll_no"] == roll_no:
                return s
        return None

    def register(self, name, age, e_mail, roll_no):
        if not name or not roll_no:
            return False, "Name and roll number are required."
        if not Persons.validate_email(e_mail):
            return False, "That email address doesn't look right."
        if self.find(roll_no):
            return False, f"Roll No. {roll_no} is already on file."
        data["students"].append({
            "name": name, "age": age, "e_mail": e_mail,
            "roll_no": roll_no, "grades": {},
        })
        save_data(data)
        return True, f"{name} has been enrolled under Roll No. {roll_no}."

    def show_details(self, roll_no):
        return self.find(roll_no)

    def add_grade(self, roll_no, subject, marks):
        s = self.find(roll_no)
        if not s:
            return False, "No student found with that roll number."
        if not subject:
            return False, "Enter a subject."
        s["grades"][subject] = marks
        save_data(data)
        return True, f"Recorded {marks:g} for {subject}."


class Teacher(Persons):
    def get_role(self):
        return "Teacher"

    def find(self, emp_id):
        for t in data["teachers"]:
            if t["emp_id"] == emp_id:
                return t
        return None

    def register(self, name, age, subject, emp_id, e_mail):
        if not name or not emp_id:
            return False, "Name and employee ID are required."
        if not Persons.validate_email(e_mail):
            return False, "That email address doesn't look right."
        if self.find(emp_id):
            return False, f"Employee ID {emp_id} is already on file."
        data["teachers"].append({
            "name": name, "age": age, "subject": subject,
            "emp_id": emp_id, "e_mail": e_mail,
        })
        save_data(data)
        return True, f"{name} has joined the faculty."

    def show_details(self, emp_id):
        return self.find(emp_id)


stud = Student()
tech = Teacher()

# ----------------------------------------------------------------------------
# Page setup + theme
# ----------------------------------------------------------------------------

st.set_page_config(page_title="The Registrar's Desk", page_icon="🖋️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap');

:root {
  --ink: #1B2A45;
  --ink-2: #263B5F;
  --parchment: #FAF6EC;
  --card: #FFFFFF;
  --gold: #B8862E;
  --gold-soft: #E7D6AC;
  --rust: #A8432E;
  --forest: #2F6F4E;
  --slate: #5B6472;
  --line: #E4DCC8;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: var(--parchment); }

/* headings use the display serif */
h1, h2, h3, .ledger-title { font-family: 'Fraunces', serif; color: var(--ink); }

/* kill default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2.2rem; max-width: 1150px; }

/* ---------- sidebar: card-catalog look ---------- */
section[data-testid="stSidebar"] {
  background: var(--ink);
  border-right: 3px solid var(--gold);
}
section[data-testid="stSidebar"] * { color: #EDE7D6 !important; }
section[data-testid="stSidebar"] .stRadio > label { display: none; }
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
  border: 1px solid rgba(237,231,214,0.18);
  border-radius: 4px;
  padding: 10px 12px;
  margin-bottom: 6px;
  transition: all 0.15s ease;
}
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
  background: rgba(184,134,46,0.18);
  border-color: var(--gold);
}
.sidebar-brand {
  font-family: 'Fraunces', serif;
  font-size: 1.5rem;
  font-weight: 600;
  color: #F4EFE0 !important;
  letter-spacing: 0.02em;
  line-height: 1.15;
  margin-bottom: 0;
}
.sidebar-tag {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.72rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--gold-soft) !important;
  margin-bottom: 1.4rem;
  display: block;
}

/* ---------- cards ---------- */
.ledger-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 1.4rem 1.6rem;
  box-shadow: 0 1px 2px rgba(27,42,69,0.04);
  position: relative;
}
.ledger-card + .ledger-card { margin-top: 1rem; }

/* the registrar's stamp — signature element */
.stamp {
  display: inline-block;
  font-family: 'IBM Plex Mono', monospace;
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--rust);
  border: 2px solid var(--rust);
  border-radius: 3px;
  padding: 3px 10px;
  transform: rotate(-3deg);
  letter-spacing: 0.06em;
  opacity: 0.9;
  float: right;
  margin-left: 12px;
}

.eyebrow {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.72rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 0.2rem;
}

.stat-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-left: 4px solid var(--gold);
  border-radius: 6px;
  padding: 1rem 1.2rem;
}
.stat-num {
  font-family: 'Fraunces', serif;
  font-size: 2.1rem;
  font-weight: 600;
  color: var(--ink);
  line-height: 1;
}
.stat-label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.72rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--slate);
}

hr.divider { border: none; border-top: 1px solid var(--line); margin: 1.6rem 0; }

/* buttons */
.stButton > button, .stFormSubmitButton > button {
  background: var(--ink);
  color: #F4EFE0;
  border: none;
  border-radius: 4px;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  padding: 0.5rem 1.3rem;
  transition: background 0.15s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover { background: var(--gold); color: var(--ink); }

/* inputs */
.stTextInput input, .stNumberInput input, .stSelectbox [data-baseweb="select"] {
  border-radius: 4px !important;
  border: 1px solid var(--line) !important;
}

/* dataframe */
[data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 6px; }
</style>
""", unsafe_allow_html=True)


def stat_card(label, value):
    st.markdown(f"""
    <div class="stat-card">
      <div class="stat-num">{value}</div>
      <div class="stat-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def notice(ok, message):
    if ok:
        st.success(message)
    else:
        st.error(message)


# ----------------------------------------------------------------------------
# Sidebar navigation
# ----------------------------------------------------------------------------

with st.sidebar:
    st.markdown('<div class="sidebar-brand">The Registrar\'s<br>Desk</div>', unsafe_allow_html=True)
    st.markdown('<span class="sidebar-tag">Est. records office</span>', unsafe_allow_html=True)
    page = st.radio(
        "nav",
        [
            "📖  Overview",
            "🧑‍🎓  Enroll a Student",
            "🧑‍🏫  Add Faculty",
            "✒️  Record Grades",
            "🗂️  Student File",
            "🗂️  Faculty File",
        ],
        label_visibility="collapsed",
    )
    st.markdown('<hr class="divider" style="border-top-color:rgba(237,231,214,0.2);">', unsafe_allow_html=True)
    st.caption(f"{len(data['students'])} students · {len(data['teachers'])} faculty on file")


# ----------------------------------------------------------------------------
# Overview
# ----------------------------------------------------------------------------

if page.endswith("Overview"):
    st.markdown('<div class="eyebrow">Front desk</div>', unsafe_allow_html=True)
    st.markdown("## Good day, Registrar.")
    st.write("A running account of everyone enrolled and everything graded.")

    all_grades = [m for s in data["students"] for m in s["grades"].values()]
    avg_grade = f"{sum(all_grades)/len(all_grades):.1f}" if all_grades else "—"

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        stat_card("Students", len(data["students"]))
    with c2:
        stat_card("Faculty", len(data["teachers"]))
    with c3:
        stat_card("Grades logged", len(all_grades))
    with c4:
        stat_card("Cohort average", avg_grade)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    left, right = st.columns([1.3, 1])

    with left:
        st.markdown("#### Grade distribution")
        if all_grades:
            df = pd.DataFrame({"marks": all_grades})
            bins = alt.Chart(df).mark_bar(color="#B8862E", cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
                x=alt.X("marks:Q", bin=alt.Bin(maxbins=12), title="Marks"),
                y=alt.Y("count()", title="Students"),
                tooltip=[alt.Tooltip("count()", title="Count")],
            ).properties(height=260)
            st.altair_chart(bins, use_container_width=True)
        else:
            st.info("No grades recorded yet — visit **Record Grades** to log the first one.")

    with right:
        st.markdown("#### Latest enrollments")
        if data["students"]:
            for s in data["students"][-5:][::-1]:
                st.markdown(f"""
                <div class="ledger-card" style="padding:0.8rem 1.1rem; margin-bottom:0.5rem;">
                  <span class="stamp" style="font-size:0.75rem; padding:1px 7px;">№ {s['roll_no']}</span>
                  <strong>{s['name']}</strong><br>
                  <span style="color:var(--slate); font-size:0.85rem;">{s.get('e_mail','')}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("The roll is empty. Enroll your first student on the left.")


# ----------------------------------------------------------------------------
# Enroll a Student
# ----------------------------------------------------------------------------

elif page.endswith("Enroll a Student"):
    st.markdown('<div class="eyebrow">Admissions</div>', unsafe_allow_html=True)
    st.markdown("## Enroll a student")
    st.write("Add a new student to the roll.")

    with st.form("enroll_student", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full name")
            roll_no = st.text_input("Roll number")
        with col2:
            age = st.number_input("Age", min_value=3, max_value=100, step=1, value=15)
            email = st.text_input("Email")
        submitted = st.form_submit_button("Enroll student")

    if submitted:
        ok, msg = stud.register(name.strip(), int(age), email.strip(), roll_no.strip())
        notice(ok, msg)


# ----------------------------------------------------------------------------
# Add Faculty
# ----------------------------------------------------------------------------

elif page.endswith("Add Faculty"):
    st.markdown('<div class="eyebrow">Human resources</div>', unsafe_allow_html=True)
    st.markdown("## Add a faculty member")
    st.write("Add a new teacher to the staff record.")

    with st.form("add_teacher", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full name")
            subject = st.text_input("Subject taught")
        with col2:
            age = st.number_input("Age", min_value=18, max_value=100, step=1, value=30)
            emp_id = st.text_input("Employee ID")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Add to faculty")

    if submitted:
        ok, msg = tech.register(name.strip(), int(age), subject.strip(), emp_id.strip(), email.strip())
        notice(ok, msg)


# ----------------------------------------------------------------------------
# Record Grades
# ----------------------------------------------------------------------------

elif page.endswith("Record Grades"):
    st.markdown('<div class="eyebrow">Academic office</div>', unsafe_allow_html=True)
    st.markdown("## Record a grade")

    if not data["students"]:
        st.info("Enroll a student first — there's no one to grade yet.")
    else:
        options = {f"{s['name']}  ·  № {s['roll_no']}": s["roll_no"] for s in data["students"]}
        with st.form("add_grade"):
            choice = st.selectbox("Student", list(options.keys()))
            col1, col2 = st.columns(2)
            with col1:
                subject = st.text_input("Subject")
            with col2:
                marks = st.number_input("Marks", min_value=0.0, max_value=100.0, step=0.5, value=75.0)
            submitted = st.form_submit_button("Save grade")

        if submitted:
            ok, msg = stud.add_grade(options[choice], subject.strip(), float(marks))
            notice(ok, msg)


# ----------------------------------------------------------------------------
# Student File
# ----------------------------------------------------------------------------

elif page.endswith("Student File"):
    st.markdown('<div class="eyebrow">Records</div>', unsafe_allow_html=True)
    st.markdown("## Student file")

    if not data["students"]:
        st.info("No students on file yet.")
    else:
        options = {f"{s['name']}  ·  № {s['roll_no']}": s["roll_no"] for s in data["students"]}
        choice = st.selectbox("Look up a student", list(options.keys()))
        s = stud.show_details(options[choice])

        grades = s["grades"]
        avg = sum(grades.values()) / len(grades) if grades else 0

        st.markdown(f"""
        <div class="ledger-card">
          <span class="stamp">№ {s['roll_no']}</span>
          <div class="eyebrow">Student record</div>
          <h3 style="margin:0 0 0.2rem 0;">{s['name']}</h3>
          <div style="color:var(--slate);">{s.get('e_mail','')} &nbsp;·&nbsp; Age {s.get('age','—')}</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2])
        with col1:
            stat_card("Average", f"{avg:.1f}" if grades else "—")
        with col2:
            if grades:
                df = pd.DataFrame({"Subject": list(grades.keys()), "Marks": list(grades.values())})
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No grades recorded for this student yet.")


# ----------------------------------------------------------------------------
# Faculty File
# ----------------------------------------------------------------------------

elif page.endswith("Faculty File"):
    st.markdown('<div class="eyebrow">Records</div>', unsafe_allow_html=True)
    st.markdown("## Faculty file")

    if not data["teachers"]:
        st.info("No faculty on file yet.")
    else:
        options = {f"{t['name']}  ·  {t['emp_id']}": t["emp_id"] for t in data["teachers"]}
        choice = st.selectbox("Look up a teacher", list(options.keys()))
        t = tech.show_details(options[choice])

        st.markdown(f"""
        <div class="ledger-card">
          <span class="stamp">{t['emp_id']}</span>
          <div class="eyebrow">Faculty record</div>
          <h3 style="margin:0 0 0.2rem 0;">{t['name']}</h3>
          <div style="color:var(--slate);">{t.get('e_mail','')} &nbsp;·&nbsp; Age {t.get('age','—')}</div>
          <div style="margin-top:0.6rem;"><strong>Subject:</strong> {t.get('subject','—')}</div>
        </div>
        """, unsafe_allow_html=True)
