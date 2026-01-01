from langchain.tools import create_retriever_tool
from langchain_chroma import Chroma
import embedding # Your existing embedding file

# 1. Connect to the database you just created
vectorstore = Chroma(
    persist_directory="./knowledgebase",
    embedding_function= embedding.embed_model, 
    collection_name="sunbeam_data"
)

# 2. Create the Retriever (fetches top 3 relevant chunks)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 3. Create the Tool
# The 'description' is very important: it tells the AI what is inside the tool.
sunbeam_tool = create_retriever_tool(
    retriever,
    "sunbeam_course_advisor",
    "Use this tool to find information about Sunbeam's Internship programs, Modular courses, Pre-CAT, and Mastering MCQ courses. Use it for fees, durations, and syllabus questions."
)

tools = [sunbeam_tool]