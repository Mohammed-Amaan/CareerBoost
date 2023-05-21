import docx2txt as docx2txt
import fitz
import streamlit as st
import openai
from streamlit_agraph import agraph, Node, Edge, Config
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import os


api_key = st.secrets["OPENAI_KEY"]
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_KEY"]

# Declaring variables and lists used in the code
resume_headers = [
    "WORK EXPERIENCE",
    "JOB EXPERIENCE",
    "DUTY EXPERIENCE",
    "EXPERIENCE",
    "PROFESSIONAL EXPERIENCE",
    "CAREER SUMMARY",
    "PROFESSION SUMMARY",
    "CAREER OBJECTIVE",
    "PROFESSION OBJECTIVE",
    "EDUCATION",
    "TRAINING",
    "SCHOOLING",
    "Relevant Courses",
    "Courses",
    "Appropriate Courses",
    "SKILLS",
    "TOP SKILLS",
    "TECHNICAL SKILLS",
    "EXPERTISE",
    "CERTIFICATIONS",
    "UNIVERSITY PROJECTS",
    "CERTIFICATES",
    "PROJECTS",
    "ASSIGNMENTS",
    "OTHER",
    "ADDITIONAL",
    "ADDITIONAL INFORMATION",
    "CONTACT",
    "HONORS-AWARDS",
    "LANGUAGES",
]


# Add text between start and end of two headers onto lists
def add_val(strList, mainList, s, e):
    s1 = s + 1
    while s1 < e:
        if mainList[s1] != "":
            strList.append(mainList[s1])
        s1 += 1


# Reading contents of resume according to file type
def read_resume():
    #   st.markdown("<h4 style='color: White;'>Enter your details</h4>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload Your Resume",
        type=["txt", "docx", "pdf"],
        on_change=set_stage,
        args=(1,),
    )
    # if st.button("Display Skills", on_click=set_stage, args=(1,)):
    if uploaded_file is not None:
        # File Details
        if uploaded_file.type == "text/plain":
            maintext = str(uploaded_file.read(), "utf-8")
            create_resume_dict(maintext, resume_headers)
        elif uploaded_file.type == "application/pdf":
            # os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_KEY"]
            # Using LLM model to get skills and experience of candidate (Applied only to PDF)
            try:
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                text = ""
                for page in doc:
                    text += page.get_text("text")
                raw_text = text.split("\n")

                text_splitter = CharacterTextSplitter(
                    separator="\n",
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len,
                )
                texts = raw_text

                # Download embeddings from OpenAI
                embeddings = OpenAIEmbeddings()

                docsearch = FAISS.from_texts(texts, embeddings)

                chain = load_qa_chain(OpenAI(), chain_type="stuff")

                query = "Give the technical skills in the provided resume"
                docs = docsearch.similarity_search(query)
                st.session_state.skills = chain.run(
                    input_documents=docs, question=query
                )
                query = "Give the number of years of experience with the field of work in the provided resume"
                docs = docsearch.similarity_search(query)
                st.session_state.experience = chain.run(
                    input_documents=docs, question=query
                )
                result()
            except Exception as e:
                print(e)
        elif (
            uploaded_file.type
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            text = docx2txt.process(uploaded_file)
            x = text.split("\n")
            templist = []
            for i in x:
                templist.append(i.replace(":", ""))
            maintext = [i for i in templist if i != ""]
            create_resume_dict(maintext, resume_headers)


# Create dictionary based on position of headers in resume
def create_resume_dict(x, resume_headers):
    dict = []
    length = len(x)
    for i in range(length):
        for j in resume_headers:
            doc = x[i].split()
            if len(doc) >= 2:
                if (str(doc[0]) + " " + str(doc[1])).lower() == j.lower():
                    temp_dict = {"text": j, "pos": i}
                    dict.append(temp_dict)
            elif x[i].lower() == j.lower():
                temp_dict = {"text": j, "pos": i}
                dict.append(temp_dict)
            if i <= length - 2:
                if (x[i] + " " + x[i + 1]).lower() == j.lower():
                    temp_dict = {"text": j, "pos": i + 2}
                    dict.append(temp_dict)
    add_resume_val_to_list(dict, x)


# Add text under a header onto list and then on Excel - RESUME
def add_resume_val_to_list(dict, x):
    WE = []
    CS = []
    E = []
    S = []
    C = []
    P = []
    RC = []
    O = []
    length = len(dict)
    for k in range(length):
        if k != length - 1:
            s = dict[k]["pos"]
            e = dict[k + 1]["pos"]
        else:
            s = dict[k]["pos"]
            e = len(x) - 1
        header_name = dict[k]["text"]

        if (
            header_name == "WORK EXPERIENCE"
            or header_name == "JOB EXPERIENCE"
            or header_name == "DUTY EXPERIENCE"
            or header_name == "EXPERIENCE"
            or header_name == "PROFESSIONAL EXPERIENCE"
        ):
            add_val(WE, x, s, e)
        elif (
            header_name == "CAREER SUMMARY"
            or header_name == "PROFESSION SUMMARY"
            or header_name == "CAREER OBJECTIVE"
            or header_name == "PROFESSION OBJECTIVE"
        ):
            add_val(CS, x, s, e)
        elif (
            header_name == "EDUCATION"
            or header_name == "TRAINING"
            or header_name == "SCHOOLING"
        ):
            add_val(E, x, s, e)
        elif (
            header_name == "SKILLS"
            or header_name == "EXPERTISE"
            or header_name == "TECHNICAL SKILLS"
            or header_name == "TOP SKILLS"
        ):
            add_val(S, x, s, e)
        elif header_name == "CERTIFICATIONS" or header_name == "CERTIFICATES":
            add_val(C, x, s, e)
        elif (
            header_name == "PROJECTS"
            or header_name == "ASSIGNMENTS"
            or header_name == "UNIVERSITY PROJECTS"
        ):
            add_val(P, x, s, e)
        elif (
            header_name == "Courses"
            or header_name == "Relevant Courses"
            or header_name == "Appropriate Courses"
        ):
            add_val(RC, x, s, e)
        elif (
            header_name == "OTHER"
            or header_name == "ADDITIONAL"
            or header_name == "ADDITIONAL INFORMATION"
            or header_name == "CONTACT"
            or header_name == "HONOR-AWARDS"
            or header_name == "LANGUAGES"
        ):
            add_val(O, x, s, e)

    st.session_state.skills = ", ".join(S)
    # st.write(st.session_state.skills)
    if st.session_state.skills:
        if st.session_state.stage > 0:
            st.button("Display Jobs", on_click=set_stage_Resume_docx, args=(2,))
            if st.session_state.stage > 1:
                st.selectbox(
                    "Select a job?",
                    st.session_state.job_titles,
                    on_change=set_stage_Roadmap,
                    args=(3,),
                    key="JobTitle",
                )
                if st.session_state.stage > 2:
                    st.header("Roadmap")
                    build_roadmap(st.session_state.roadmap)
                st.button("Reset", on_click=set_stage, args=(0,))
    else:
        st.write("Skills not found !!!")
        st.write("Please make sure you have a separate section for Skills")


def result():
    if st.session_state.stage > 0:
        st.button("Display Jobs", on_click=set_stage_Resume_pdf, args=(2,))
        if st.session_state.stage > 1:
            st.selectbox(
                "Select a job?",
                st.session_state.job_titles,
                on_change=set_stage_Roadmap_pdf,
                args=(3,),
                key="JobTitle",
            )
            if st.session_state.stage > 2:
                st.header("Roadmap")
                build_roadmap(st.session_state.roadmap)
            st.button("Reset", on_click=set_stage, args=(0,))


def get_job_titles(content):
    

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"{content}. Give the points in new lines"}
        ],
    )

    chat_response = completion.choices[0].message.content
    print("1" + chat_response)
    job_titles = chat_response.split("\n")
    return job_titles


if (
    "stage" not in st.session_state
    and "skills" not in st.session_state
    and "job_titles" not in st.session_state
    and "roadmap" not in st.session_state
    and "experience" not in st.session_state
):
    st.session_state.stage = 0
    st.session_state.skills = ""
    st.session_state.job_titles = []
    st.session_state.roadmap = []
    st.session_state.experience = ""


def set_stage(stage):
    st.session_state.stage = stage


def set_stage_Resume_docx(stage):
    st.session_state.stage = stage
    if "skills" in st.session_state:
        content = f"Recommend suitable jobs for someone with skills in {st.session_state.skills}"
        st.session_state.job_titles = get_job_titles(content)
        st.session_state.job_titles.insert(0, "")


def set_stage_Resume_pdf(stage):
    st.session_state.stage = stage
    if "skills" in st.session_state:
        content = f"Recommend suitable jobs for someone with skills {st.session_state.skills} and experience as {st.session_state.experience} "
        st.session_state.job_titles = get_job_titles(content)
        st.session_state.job_titles.insert(0, "")


def set_stage_Roadmap(stage):
    st.session_state.stage = stage
    if "JobTitle" in st.session_state:
        content = f"Give steps to become a {st.session_state['JobTitle']}"
        st.session_state.roadmap = get_job_titles(content)


def set_stage_Roadmap_pdf(stage):
    st.session_state.stage = stage
    if "JobTitle" in st.session_state:
        content = f"Give steps to become a {st.session_state['JobTitle']} with {st.session_state.experience}"
        st.session_state.roadmap = get_job_titles(content)


def build_roadmap(templist):
    nodes = []
    edges = []
    temp = []
    for i in range(len(templist)):
        if templist[i] not in temp:
            temp.append(templist[i])
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


st.set_page_config(page_title="CareerBoost", page_icon="🚀", layout="wide")

st.title("Career Advisor using OpenAI GPT-3.5-turbo")
st.sidebar.success("Select a page above.")

read_resume()
