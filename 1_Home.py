import streamlit as st
import openai
from streamlit_agraph import agraph, Node, Edge, Config


def get_job_titles(content):
    openai.api_key = st.secrets["OPENAI_KEY"]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f'{content}. Only give the specific points in new lines and no other text'}
        ]
    )

    chat_response = completion.choices[0].message.content
    print("1" + chat_response)
    job_titles = chat_response.split("\n")
    return job_titles


if 'stage' not in st.session_state and 'job_titles' not in st.session_state and 'roadmap' not in st.session_state:
    st.session_state.stage = 0
    st.session_state.job_titles = []
    st.session_state.roadmap = []


def set_stage(stage):
    st.session_state.stage = stage


def set_stage_Employeed(stage):
    st.session_state.stage = stage
    if 'EmpStatus' in st.session_state and EmpStatus == 'Employed' or EmpStatus == 'Searching For Jobs':
        if 'Profession' in st.session_state and 'Exp' in st.session_state:
            content = f"I am a {st.session_state['Profession'].lower()} with {st.session_state['Exp']} years of experience. " \
                      f"Can you recommend some suitable jobs? "
            st.session_state.job_titles = get_job_titles(content)
            st.session_state.job_titles.insert(0, '')


def set_stage_Student(stage):
    st.session_state.stage = stage
    if 'EmpStatus' in st.session_state and EmpStatus == 'Student':
        if 'Discipline' in st.session_state:
            content = f"I am a {st.session_state['Discipline']} {st.session_state['EmpStatus'].lower()}. Can you recommend some suitable jobs?"
            st.session_state.job_titles = get_job_titles(content)
            st.session_state.job_titles.insert(0, '')


def set_stage_Roadmap(stage):
    st.session_state.stage = stage
    if 'JobTitle' in st.session_state:
        content = f"Give steps to become a {st.session_state['JobTitle']}"
        st.session_state.roadmap = get_job_titles(content)



def build_roadmap(templist):
    nodes = []
    edges = []
    for i in range(len(templist)):
        nodes.append(Node(id=templist[i], size=25, shape="square", color='#3264a8', label= f'{i+1}'))
        if i != len(templist) - 1:
            edges.append(Edge(source=templist[i], label='next', target=templist[i + 1]))
    config = Config(width=2000,
                    height=2000,
                    directed=True,
                    physics=False,
                    hierarchical=True,
                    )

    return_value = agraph(nodes=nodes,
                          edges=edges,
                          config=config)


st.set_page_config(
    page_title="CareerBoost",
    page_icon="🚀",
)

st.title("Career Advisor using OpenAI GPT-3")
st.sidebar.success("Select a page above.")

EmpStatus = st.radio(
    "What is your current employment status?",
    ('Employed', 'Searching For Jobs', 'Student'), on_change=set_stage, args=(1,), key='EmpStatus')

if st.session_state.stage > 0:
    if EmpStatus == 'Employed' or EmpStatus == 'Searching For Jobs':
        if st.slider('How many years of experience do you have', 0, 10, key='Exp'):
            st.text_input("Enter your profession", key="Profession", on_change=set_stage_Employeed, args=(2,))
            if st.session_state.stage > 1:
                st.selectbox(
                    'Select a job?',
                    st.session_state.job_titles, on_change=set_stage_Roadmap, args=(3,), key='JobTitle',
                )
                if st.session_state.stage > 2:
                    build_roadmap(st.session_state.roadmap)
                st.button('Reset', on_click=set_stage, args=(0,))
    elif EmpStatus == 'Student':
        st.selectbox('Which discipline do you study in?',
                     ('', 'CS', 'EEE', 'MECH', 'BioTech', 'Civil'), on_change=set_stage_Student, args=(2,),
                     key='Discipline')
        if st.session_state.stage > 1:
            st.selectbox(
                'Select a job?',
                st.session_state.job_titles, on_change=set_stage_Roadmap, args=(3,), key='JobTitle',
            )
            if st.session_state.stage > 2:
                build_roadmap(st.session_state.roadmap)
            st.button('Reset', on_click=set_stage, args=(0,))
