import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Student Career Compass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Career areas are scored from students' interests, preferred activities, and subjects.
CAREERS = {
    "Technology & Computing": {
        "description": "You may enjoy solving problems with computers, building digital products, or working with data.",
        "careers": ["Software developer", "Cybersecurity analyst", "Data analyst", "IT support specialist", "UX/UI designer"],
        "courses": ["Computer Science", "Software Engineering", "Information Technology", "Cybersecurity", "Data Science"],
        "subjects": ["Mathematics", "English Language", "Physics or other relevant science subjects"],
        "skills": ["Python or another programming language", "Logical problem-solving", "Digital safety", "Building small projects"],
        "interest": ["technology", "computers", "logic"],
    },
    "Medicine & Health": {
        "description": "You may be motivated by helping people, understanding the human body, and improving health.",
        "careers": ["Doctor", "Nurse", "Pharmacist", "Medical laboratory scientist", "Physiotherapist", "Public health professional"],
        "courses": ["Medicine and Surgery", "Nursing Science", "Pharmacy", "Medical Laboratory Science", "Physiotherapy", "Public Health"],
        "subjects": ["Biology", "Chemistry", "Physics", "English Language"],
        "skills": ["Communication and empathy", "Careful observation", "Basic first-aid awareness", "Consistent science study"],
        "interest": ["health", "helping"],
    },
    "Engineering & Building": {
        "description": "You may enjoy designing, repairing, constructing, or understanding how machines and systems work.",
        "careers": ["Civil engineer", "Electrical engineer", "Mechanical engineer", "Mechatronics engineer", "Architect", "Quantity surveyor"],
        "courses": ["Civil Engineering", "Electrical/Electronic Engineering", "Mechanical Engineering", "Mechatronics Engineering", "Architecture", "Quantity Surveying"],
        "subjects": ["Mathematics", "Physics", "Chemistry", "Technical Drawing where relevant"],
        "skills": ["Mathematical reasoning", "Design and drawing", "Practical experiments", "Building or repair projects"],
        "interest": ["building", "logic", "design"],
    },
    "Business, Finance & Entrepreneurship": {
        "description": "You may like organising resources, selling ideas, managing money, or starting projects.",
        "careers": ["Accountant", "Business analyst", "Entrepreneur", "Banking professional", "Marketing specialist", "Human resources officer"],
        "courses": ["Accounting", "Business Administration", "Economics", "Finance", "Marketing", "Entrepreneurship"],
        "subjects": ["Mathematics", "English Language", "Economics", "Commerce or Accounting where offered"],
        "skills": ["Budgeting", "Presentation", "Teamwork", "Customer research", "Spreadsheet skills"],
        "interest": ["business", "leadership", "numbers"],
    },
    "Law, Government & Public Service": {
        "description": "You may enjoy debating ideas, researching issues, understanding rules, and advocating for people.",
        "careers": ["Lawyer", "Policy analyst", "Diplomat", "Public administrator", "Human rights advocate", "Political researcher"],
        "courses": ["Law", "Political Science", "International Relations", "Public Administration", "Peace and Conflict Studies"],
        "subjects": ["English Language", "Government", "Literature in English", "History or other relevant humanities subjects"],
        "skills": ["Reading and writing", "Reasoned debate", "Research", "Public speaking"],
        "interest": ["law", "leadership", "writing"],
    },
    "Education & Communication": {
        "description": "You may enjoy explaining ideas, helping others learn, writing, speaking, or sharing information.",
        "careers": ["Teacher", "Lecturer (with further study)", "Journalist", "Public relations officer", "Editor", "Communication specialist"],
        "courses": ["Education", "English", "Mass Communication", "Linguistics", "Educational Technology"],
        "subjects": ["English Language", "Relevant teaching-subject combinations", "Literature or other related subjects"],
        "skills": ["Clear writing", "Speaking", "Explaining difficult ideas", "Listening"],
        "interest": ["teaching", "writing", "helping"],
    },
    "Creative Arts & Media": {
        "description": "You may enjoy creating visuals, telling stories, performing, making content, or designing experiences.",
        "careers": ["Graphic designer", "Animator", "Filmmaker", "Photographer", "Content creator", "Fashion designer"],
        "courses": ["Fine and Applied Arts", "Graphic Design", "Film and Multimedia Studies", "Theatre Arts", "Fashion Design", "Creative Arts"],
        "subjects": ["English Language", "Fine Art or relevant creative subjects where offered", "Other course-specific subjects"],
        "skills": ["Portfolio development", "Visual storytelling", "Editing tools", "Creative practice"],
        "interest": ["art", "design", "writing"],
    },
    "Science, Environment & Agriculture": {
        "description": "You may enjoy investigating nature, conducting experiments, protecting the environment, or improving food production.",
        "careers": ["Biologist", "Environmental scientist", "Agricultural scientist", "Food scientist", "Laboratory researcher", "Veterinarian"],
        "courses": ["Biology", "Microbiology", "Environmental Science", "Agriculture", "Food Science and Technology", "Veterinary Medicine"],
        "subjects": ["Biology", "Chemistry", "Mathematics", "Physics or other course-specific science subjects"],
        "skills": ["Observation", "Data collection", "Scientific writing", "Field or laboratory practice"],
        "interest": ["nature", "health", "logic"],
    },
    "Social Sciences & People": {
        "description": "You may enjoy understanding people, communities, behaviour, and how society works.",
        "careers": ["Psychologist (with required further training)", "Sociologist", "Social worker", "Human resources professional", "Community development officer"],
        "courses": ["Psychology", "Sociology", "Social Work", "Criminology", "Community Development"],
        "subjects": ["English Language", "Government", "Economics", "Biology or other course-specific subjects"],
        "skills": ["Listening", "Research", "Ethical judgement", "Communication"],
        "interest": ["helping", "people", "law"],
    },
}

# Each question contributes points to one or more career areas.
QUESTIONS = [
    {
        "key": "activities",
        "label": "Which activities would you most enjoy?",
        "help": "Choose up to 3.",
        "options": {
            "Writing code or solving computer problems": ["Technology & Computing"],
            "Helping sick people or learning about the body": ["Medicine & Health"],
            "Designing buildings, machines, or practical solutions": ["Engineering & Building"],
            "Running a business or managing money": ["Business, Finance & Entrepreneurship"],
            "Debating social issues or defending people's rights": ["Law, Government & Public Service"],
            "Explaining topics or telling stories": ["Education & Communication"],
            "Drawing, designing, filming, or performing": ["Creative Arts & Media"],
            "Studying plants, animals, food, or the environment": ["Science, Environment & Agriculture"],
            "Understanding people's behaviour and communities": ["Social Sciences & People"],
        },
    },
    {
        "key": "strengths",
        "label": "What are you naturally good at or willing to practise?",
        "help": "Choose up to 3.",
        "options": {
            "Logical thinking and solving puzzles": ["Technology & Computing", "Engineering & Building"],
            "Biology, health topics, and careful observation": ["Medicine & Health", "Science, Environment & Agriculture"],
            "Mathematics and working with numbers": ["Engineering & Building", "Business, Finance & Entrepreneurship", "Technology & Computing"],
            "Speaking, persuading, or leading a group": ["Law, Government & Public Service", "Business, Finance & Entrepreneurship"],
            "Writing, reading, and explaining ideas": ["Education & Communication", "Law, Government & Public Service"],
            "Drawing, imagining, and creating": ["Creative Arts & Media", "Engineering & Building"],
            "Listening and supporting other people": ["Social Sciences & People", "Medicine & Health", "Education & Communication"],
            "Practical work with nature or materials": ["Science, Environment & Agriculture", "Engineering & Building"],
        },
    },
    {
        "key": "subjects",
        "label": "Which school subjects do you enjoy most?",
        "help": "Choose up to 4. Select subjects you enjoy, not only subjects with high marks.",
        "options": {
            "Mathematics": ["Technology & Computing", "Engineering & Building", "Business, Finance & Entrepreneurship"],
            "Physics": ["Engineering & Building", "Technology & Computing"],
            "Chemistry": ["Medicine & Health", "Science, Environment & Agriculture", "Engineering & Building"],
            "Biology": ["Medicine & Health", "Science, Environment & Agriculture", "Social Sciences & People"],
            "English Language or Literature": ["Education & Communication", "Law, Government & Public Service", "Creative Arts & Media"],
            "Economics, Commerce, or Accounting": ["Business, Finance & Entrepreneurship"],
            "Government or History": ["Law, Government & Public Service", "Social Sciences & People", "Education & Communication"],
            "Art, Music, or other creative subjects": ["Creative Arts & Media"],
            "Agricultural Science or Geography": ["Science, Environment & Agriculture"],
            "Computer Studies": ["Technology & Computing"],
        },
    },
    {
        "key": "workstyle",
        "label": "What kind of work setting sounds best to you?",
        "help": "Choose one or two.",
        "options": {
            "Working with computers and digital tools": ["Technology & Computing"],
            "Working with patients or health teams": ["Medicine & Health"],
            "Building, testing, fixing, or designing things": ["Engineering & Building"],
            "Planning, selling, managing, or analysing business problems": ["Business, Finance & Entrepreneurship"],
            "Researching, writing, debating, or interpreting rules": ["Law, Government & Public Service"],
            "Teaching, presenting, interviewing, or communicating": ["Education & Communication"],
            "Making visual, audio, or performance-based work": ["Creative Arts & Media"],
            "Working outdoors, in a lab, or with the environment": ["Science, Environment & Agriculture"],
            "Supporting people or improving communities": ["Social Sciences & People"],
        },
    },
    {
        "key": "values",
        "label": "What matters most to you in a future career?",
        "help": "Choose up to 2.",
        "options": {
            "Making a difference to people's health": ["Medicine & Health", "Social Sciences & People"],
            "Inventing or solving difficult problems": ["Technology & Computing", "Engineering & Building", "Science, Environment & Agriculture"],
            "Running my own business or growing income": ["Business, Finance & Entrepreneurship"],
            "Speaking up for fairness and justice": ["Law, Government & Public Service"],
            "Sharing knowledge and helping others learn": ["Education & Communication"],
            "Expressing ideas and creating original work": ["Creative Arts & Media"],
            "Understanding people and improving society": ["Social Sciences & People", "Law, Government & Public Service"],
            "Improving food, land, or the natural world": ["Science, Environment & Agriculture"],
        },
    },
]

def score_answers(answers):
    scores = {area: 0 for area in CAREERS}
    for question in QUESTIONS:
        selected = answers.get(question["key"], [])
        for option in selected:
            for area in question["options"].get(option, []):
                scores[area] += 1
    return sorted(scores.items(), key=lambda item: (-item[1], item[0]))

def render_bullets(items):
    for item in items:
        st.markdown(f"- {item}")

st.title("🧭 Student Career Compass")
st.caption("A career-interest guide for SS3 / Year 12 students preparing for final examinations and life after secondary school.")
st.info(
    "This tool suggests career areas from your interests and preferences. It does not measure intelligence, "
    "guarantee success, or replace advice from a school counsellor. Course requirements vary by institution."
)

with st.sidebar:
    st.header("About this guide")
    st.write("Designed for students exploring university, polytechnic, college, vocational, and other training pathways.")
    st.write("**Tip:** Answer honestly. There are no right or wrong answers.")
    st.divider()
    st.write("Your answers are processed in this session and are not saved to a database by this app.")

st.header("1. Tell us about yourself")
col1, col2 = st.columns(2)
with col1:
    student_name = st.text_input("First name or nickname (optional)")
    school_level = st.selectbox("Current level", ["SS3 / Year 12", "SS2 / Year 11", "Other final-year secondary level", "Other"])
with col2:
    country = st.selectbox("Country where you plan to study", ["Nigeria", "Ghana", "Other / not sure"])
    next_step = st.selectbox(
        "What are you considering after secondary school?",
        ["University", "Polytechnic / college", "Vocational or technical training", "Work and further study", "Not sure yet"],
    )

st.header("2. Discover your interests")
st.write("Select the options that fit you best. You can leave a question unanswered if you are unsure.")
answers = {}
for question in QUESTIONS:
    st.subheader(question["label"])
    st.caption(question["help"])
    max_selections = {"activities": 3, "strengths": 3, "subjects": 4, "workstyle": 2, "values": 2}[question["key"]]
    answers[question["key"]] = st.multiselect(
        question["label"],
        list(question["options"].keys()),
        max_selections=max_selections,
        key=f"q_{question['key']}",
        label_visibility="collapsed",
    )

st.header("3. Your study and career priorities")
col1, col2 = st.columns(2)
with col1:
    favourite_subject_other = st.text_input("Any other favourite subject? (optional)")
    enjoy_practical = st.radio(
        "Do you prefer practical projects or mostly reading and theory?",
        ["Practical projects", "A mix of both", "Mostly reading and theory", "Not sure"],
    )
with col2:
    important_constraint = st.selectbox(
        "What should your next-step plan consider?",
        ["Course entry requirements", "Cost and scholarships", "Location", "Length of training", "Job opportunities", "All of these", "Not sure yet"],
    )
    exam_year = st.selectbox("When are you planning to take your final exams?", ["This academic year", "Next academic year", "Already completed", "Not sure"])

st.divider()
if st.button("✨ Generate my career guidance report", type="primary", use_container_width=True):
    if not any(answers.values()):
        st.warning("Please answer at least one interest question so the report can reflect your preferences.")
    else:
        ranked = score_answers(answers)
        top_score = ranked[0][1]
        top_areas = [area for area, score in ranked if score == top_score and score > 0]
        # Include the next strongest area where it has a meaningful score.
        second_areas = [
            area for area, score in ranked
            if score > 0 and area not in top_areas and score >= max(1, top_score - 1)
        ][:2]
        st.session_state["career_report"] = {
            "name": student_name.strip(),
            "level": school_level,
            "country": country,
            "next_step": next_step,
            "ranked": ranked,
            "top_areas": top_areas,
            "second_areas": second_areas,
            "favourite_subject_other": favourite_subject_other.strip(),
            "enjoy_practical": enjoy_practical,
            "important_constraint": important_constraint,
            "exam_year": exam_year,
        }

if "career_report" in st.session_state:
    report = st.session_state["career_report"]
    st.header("Your career guidance report")
    if report["name"]:
        st.markdown(f"### Hello, {report['name']}!")
    st.write(
        f"Based on your answers, your strongest match{'es are' if len(report['top_areas']) > 1 else ' is'} "
        + ", ".join(f"**{x}**" for x in report["top_areas"])
        + ". These are starting points for exploration, not fixed labels."
    )

    for idx, area in enumerate(report["top_areas"] + report["second_areas"]):
        info = CAREERS[area]
        st.subheader(f"{idx + 1}. {area}")
        st.write(info["description"])
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Possible careers**")
            render_bullets(info["careers"])
            st.markdown("**Related courses to investigate**")
            render_bullets(info["courses"])
        with c2:
            st.markdown("**Subjects to pay attention to**")
            render_bullets(info["subjects"])
            st.markdown("**Skills you can start building**")
            render_bullets(info["skills"])
        st.divider()

    st.subheader("Your next steps before final exams")
    steps = [
        "Choose your 2–3 favourite career areas and read about the everyday work involved.",
        "Check the official entry requirements for each course at the specific institutions you are considering.",
        "Compare required O'Level subjects and grades with your current subjects and study plan.",
        "Ask a teacher, parent/guardian, or career counsellor to discuss your strengths and options.",
        "Try a small project, club activity, job shadowing opportunity, or free beginner course related to your top career area.",
        "Keep a backup option that also interests you; your career can change as you learn more.",
    ]
    render_bullets(steps)

    st.subheader("Important course-entry reminder")
    if report["country"] == "Nigeria":
        st.write(
            "For Nigeria, verify current requirements using the official JAMB brochure and the admissions page of each institution. "
            "Requirements can differ by course and institution, and may include UTME subject combinations and O'Level credits. "
            "Do not rely on this app alone to decide your subject combination."
        )
        st.markdown("[JAMB official website](https://www.jamb.gov.ng/)")
    else:
        st.write(
            "Check the official admissions and qualification requirements for the country and institution where you intend to study. "
            "Requirements can vary by course, institution, and year."
        )

    st.markdown("**Your preferences**")
    st.write(f"- Preferred next step: {report['next_step']}")
    st.write(f"- Main planning priority: {report['important_constraint']}")
    st.write(f"- Exam timing: {report['exam_year']}")
    st.write(f"- Preferred learning style: {report['enjoy_practical']}")
    if report["favourite_subject_other"]:
        st.write(f"- Other favourite subject: {report['favourite_subject_other']}")

    summary_lines = [
        "STUDENT CAREER COMPASS — CAREER GUIDANCE REPORT",
        f"Name: {report['name'] or 'Not provided'}",
        f"Level: {report['level']}",
        f"Study country: {report['country']}",
        f"Next step: {report['next_step']}",
        "",
        "Career matches:",
    ]
    for area, score in report["ranked"]:
        if score > 0:
            summary_lines.append(f"- {area}: interest score {score}")
            if area in report["top_areas"] or area in report["second_areas"]:
                summary_lines.append(f"  Careers: {', '.join(CAREERS[area]['careers'])}")
                summary_lines.append(f"  Courses: {', '.join(CAREERS[area]['courses'])}")
    summary_lines += [
        "",
        "Reminder: This is an interest guide, not a guarantee or formal aptitude test.",
        "Verify all admission requirements with official institutions and relevant exam/admissions bodies.",
    ]
    st.download_button(
        "⬇️ Download report as a text file",
        data="\n".join(summary_lines),
        file_name="student_career_guidance_report.txt",
        mime="text/plain",
        use_container_width=True,
    )

st.divider()
st.caption("Student Career Compass • For educational guidance. Review career and course information with a qualified counsellor.")
