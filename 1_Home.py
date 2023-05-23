import streamlit as st
import openai
from streamlit_agraph import agraph, Node, Edge, Config
import webbrowser
from urllib.parse import urlencode


def get_job_titles(content):
    openai.api_key = st.secrets["OPENAI_KEY"]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"{content}. Only give the specific points in new lines and no other text",
            }
        ],
    )

    chat_response = completion.choices[0].message.content
    print("1" + chat_response)
    job_titles = chat_response.split("\n")
    return job_titles


if (
    "stage" not in st.session_state
    and "job_titles" not in st.session_state
    and "roadmap" not in st.session_state
    and "courses" not in st.session_state
    and "certifications" not in st.session_state
    and "corporate_ladder" not in st.session_state
    and "salary" not in st.session_state
    and "interview_questions" not in st.session_state
    and "JobTitle" not in st.session_state
):
    st.session_state.stage = 0
    st.session_state.job_titles = []
    st.session_state.roadmap = []
    st.session_state.courses = ""
    st.session_state.certifications = ""
    st.session_state.corporate_ladder = ""
    st.session_state.salary = ""
    st.session_state.interview_questions = ""
    st.session_state.JobTitle = ""


def set_stage(stage):
    st.session_state.stage = stage


def set_stage_courses(stage):
    st.session_state.stage = stage
    content = f"Give the names of courses for the role of {st.session_state.JobTitle} with their websites"
    st.session_state.courses = get_job_titles(content)
    st.session_state.courses.insert(0, "")


def set_stage_certifications(stage):
    st.session_state.stage = stage
    content = (
        f"give the names of certifications for the role of {st.session_state.JobTitle}"
    )
    st.session_state.certifications = get_job_titles(content)
    st.session_state.certifications.insert(0, "")


def set_stage_corporate_ladder(stage):
    st.session_state.stage = stage
    content = f"give the corporate ladder job titles for the role of {st.session_state.JobTitle}"
    st.session_state.corporate_ladder = get_job_titles(content)
    st.session_state.corporate_ladder.insert(0, "")


def set_stage_salary(stage):
    st.session_state.stage = stage
    content = f"provide the salary range for the role of {st.session_state.JobTitle}"
    st.session_state.salary = get_job_titles(content)
    st.session_state.salary.insert(0, "")


def set_stage_interview_questions(stage):
    st.session_state.stage = stage
    content = (
        f"provide 10 interview questions for the role of {st.session_state.JobTitle}"
    )
    st.session_state.interview_questions = get_job_titles(content)
    st.session_state.interview_questions.insert(0, "")


def set_stage_Employeed(stage):
    st.session_state.stage = stage
    if (
        "EmpStatus" in st.session_state
        and EmpStatus == "Employed"
        or EmpStatus == "Searching For Jobs"
    ):
        if "Profession" in st.session_state and "Exp" in st.session_state:
            content = (
                f"I am a {st.session_state['Profession'].lower()} with {st.session_state['Exp']} years of experience. "
                f"Can you recommend some suitable jobs? "
            )
            st.session_state.job_titles = get_job_titles(content)
            st.session_state.job_titles.insert(0, "")
            # for i in st.session_state.job_titles:
            #    if len(i) < 5:
            #        st.session_state.job_titles.remove(i);


def set_stage_Student(stage):
    st.session_state.stage = stage
    if "EmpStatus" in st.session_state and EmpStatus == "Student":
        if "Discipline" in st.session_state:
            content = f"I am a {st.session_state['Discipline']} {st.session_state['EmpStatus'].lower()}. Can you recommend some suitable jobs?"
            st.session_state.job_titles = get_job_titles(content)
            st.session_state.job_titles.insert(0, "")
            # for i in st.session_state.job_titles:
            #    if len(i) < 5:
            #        st.session_state.job_titles.remove(i);


def set_stage_Roadmap(stage):
    st.session_state.stage = stage
    if "JobTitle" in st.session_state:
        content = f"Give steps to become a {st.session_state['JobTitle']}"
        st.session_state.roadmap = get_job_titles(content)
        for i in st.session_state.roadmap:
            if len(i) < 5:
                st.session_state.roadmap.remove(i)


def open_linkedin_job_listings(job_keywords, location):
    base_url = "https://www.linkedin.com/jobs/search/?"
    params = {"keywords": job_keywords, "location": location}
    url = base_url + urlencode(params)

    # Open the URL using the default web browser
    webbrowser.open(url)


def build_roadmap_student_employed(templist):
    nodes = []
    edges = []
    for i in range(len(templist)):
        nodes.append(
            Node(
                id=templist[i], size=25, shape="square", color="#3264a8", label=f"{i+1}"
            )
        )
        if i != len(templist) - 1:
            edges.append(Edge(source=templist[i], label="next", target=templist[i + 1]))
    config = Config(
        width=1500,
        height=1000,
        directed=True,
        physics=False,
        hierarchical=True,
    )

    return_value = agraph(nodes=nodes, edges=edges, config=config)
    set_stage(4)
    if st.session_state.stage > 3:
        st.markdown("<h4 style='color: #d66d22;'>Gain competitive edge by acheiving these certifications</h4>", unsafe_allow_html=True)
        st.write(
            "Click the button below to display recommended certifications for your selected job."
        )
        st.button(
            "Display Certifications", on_click=set_stage_certifications, args=(5,)
        )
        temp_courses = "\n".join(st.session_state.certifications)
        st.write(temp_courses)
        set_stage(5)
        if st.session_state.stage > 6:
            st.markdown("<h4 style='color: #d66d22;'>Discover your next level in the corporate ladder</h4>", unsafe_allow_html=True)
            st.write(
                "Click the button below to display the corporate ladder for your selected job."
            )
            st.button(
                "Display corporate Ladder",
                on_click=set_stage_corporate_ladder,
                args=(6,),
            )
            temp_courses = "\n".join(st.session_state.corporate_ladder)
            st.write(temp_courses)


def build_roadmap_searching_for_jobs(templist):
    nodes = []
    edges = []
    for i in range(len(templist)):
        nodes.append(
            Node(
                id=templist[i], size=25, shape="square", color="#3264a8", label=f"{i+1}"
            )
        )
        if i != len(templist) - 1:
            edges.append(Edge(source=templist[i], label="next", target=templist[i + 1]))
    config = Config(
        width=1500,
        height=1000,
        directed=True,
        physics=False,
        hierarchical=True,
    )

    return_value = agraph(nodes=nodes, edges=edges, config=config)
    set_stage(4)
    if st.session_state.stage > 3:
        st.markdown("<h4 style='color: #d66d22;'>Crack your next interview with these questions</h4>", unsafe_allow_html=True)
        st.write(
            "Click the button below to display possible interview questions for your selected job."
        )
        st.button(
            "Display Interview Question",
            on_click=set_stage_interview_questions,
            args=(5,),
        )
        temp_courses = "\n".join(st.session_state.interview_questions)
        st.write(temp_courses)
        set_stage(5)
        if st.session_state.stage > 4:
            st.markdown("<h4 style='color: #d66d22;'>Find out your next expected salary</h4>", unsafe_allow_html=True)
            st.write(
                "Click the button below to display recommended salary for your selected job."
            )
            st.button("Display salary", on_click=set_stage_salary, args=(6,))
            temp_courses = "\n".join(st.session_state.salary)
            st.write(temp_courses)
            set_stage(6)
            if st.session_state.stage > 5:
                st.markdown("<h4 style='color: #d66d22;'>View available jobs related to your expertise</h4>", unsafe_allow_html=True)
                job_keywords = st.text_input("Enter your job title")
                location = st.text_input("Enter your preferred stay of work")
                if location and job_keywords:
                    open_linkedin_job_listings(job_keywords, location)


def build_roadmap_student(templist):
    nodes = []
    edges = []
    for i in range(len(templist)):
        nodes.append(
            Node(
                id=templist[i], size=25, shape="square", color="#3264a8", label=f"{i+1}"
            )
        )
        if i != len(templist) - 1:
            edges.append(Edge(source=templist[i], label="next", target=templist[i + 1]))
    config = Config(
        width=1500,
        height=1000,
        directed=True,
        physics=False,
        hierarchical=True,
    )

    return_value = agraph(nodes=nodes, edges=edges, config=config)
    set_stage(4)
    if st.session_state.stage > 3:
        st.markdown("<h4 style='color: #d66d22;'>Learn in demand skills through these popular courses</h4>", unsafe_allow_html=True)
        st.write(
            "Click the button below to display recommended courses for your selected job."
        )
        st.button("Display Courses", on_click=set_stage_courses, args=(5,))
        temp_courses = "\n".join(st.session_state.courses)
        st.write(temp_courses)


st.set_page_config(page_title="CareerBoost", page_icon="🚀", layout="wide")
st.markdown("<h1 style='color: #d66d22;'>Career Advisor using OpenAI GPT-3</h1>", unsafe_allow_html=True)
st.sidebar.success("Select a page above.")

EmpStatus = st.radio(
    "What is your current employment status?",
    ("Employed", "Searching For Jobs", "Student"),
    on_change=set_stage,
    args=(1,),
    key="EmpStatus",
)

if st.session_state.stage > 0:
    if EmpStatus == "Employed":
        if st.slider("How many years of experience do you have", 0, 10, key="Exp"):
            st.text_input(
                "Enter your profession",
                key="Profession",
                on_change=set_stage_Employeed,
                args=(2,),
            )
            if st.session_state.stage > 1:
                st.selectbox(
                    "Select a job",
                    st.session_state.job_titles,
                    on_change=set_stage_Roadmap,
                    args=(3,),
                    key="JobTitle",
                )
                if st.session_state.stage > 2:
                    st.markdown("<h4 style='color: #d66d22;'>Roadmap</h4>", unsafe_allow_html=True)
                    build_roadmap_student_employed(st.session_state.roadmap)
                st.button("Reset", on_click=set_stage, args=(0,))
    elif EmpStatus == "Searching For Jobs":
        if st.slider("How many years of experience do you have", 0, 10, key="Exp"):
            st.text_input(
                "Enter your profession",
                key="Profession",
                on_change=set_stage_Employeed,
                args=(2,),
            )
            if st.session_state.stage > 1:
                st.selectbox(
                    "Select a job",
                    st.session_state.job_titles,
                    on_change=set_stage_Roadmap,
                    args=(3,),
                    key="JobTitle",
                )
                if st.session_state.stage > 2:
                    st.markdown("<h4 style='color: #d66d22;'>Roadmap</h4>", unsafe_allow_html=True)
                    build_roadmap_searching_for_jobs(st.session_state.roadmap)
                st.button("Reset", on_click=set_stage, args=(0,))
    elif EmpStatus == "Student":
        st.selectbox(
            "Which discipline do you study in?",
            ("", "CS", "EEE", "MECH", "BioTech", "Civil"),
            on_change=set_stage_Student,
            args=(2,),
            key="Discipline",
        )
        if st.session_state.stage > 1:
            st.selectbox(
                "Select a job",
                st.session_state.job_titles,
                on_change=set_stage_Roadmap,
                args=(3,),
                key="JobTitle",
            )
            if st.session_state.stage > 2:
                st.markdown("<h4 style='color: #d66d22;'>Roadmap</h4>", unsafe_allow_html=True)
                build_roadmap_student(st.session_state.roadmap)
            st.button("Reset", on_click=set_stage, args=(0,))
