# langchain code for the assistant
import os
import pinecone
from dbbase import SQLDatabase
from constants import prompt
from dbchain import SQLDatabaseChain 
from langchain.llms import OpenAI 
from langchain.chat_models import ChatOpenAI
from langchain.tools import HumanInputRun as human
from langchain.agents import AgentType, Tool, AgentExecutor , initialize_agent , OpenAIFunctionsAgent
from sqlalchemy import create_engine
# import summarization memory
from langchain.memory import ConversationSummaryBufferMemory


with open("openai_api_key.txt", "r") as f:
    api_key = f.read()
    

os.environ["OPENAI_API_KEY"] = api_key

llm = ChatOpenAI(
    temperature=0.4,
)

class Assistant:
    """
    The assistant is a class that is used to interact with the user and the agent. 
    It is the main interface for the user to interact with the agent."""
    def __init__(self):
        self.agent = None
        self.memory = ConversationSummaryBufferMemory(llm=llm)
        self.tools = None
        self.human = None
        self.sql = None
        self.calendly = None
        self.system_message = prompt
        self.prompt = OpenAIFunctionsAgent.create_prompt(
            system_message=self.system_message,
        )
    
    
    def initialize_human(self) -> None:
        """Initialize the human"""
        self.human = human()
        return None
    
    
    def sql_chain(self, query: str = None) -> str:
        """Initialize the sql database chain"""
        db = SQLDatabase.from_uri("sqlite:///lead_db.db")
        sql_db_chain = SQLDatabaseChain.from_llm(
        llm=llm,
        db=db,
        )
        return sql_db_chain.run(query)
        
    def intialize_tools(self):
        """Initialize the tools"""
        if self.tools is None:
            self.tools = [
                Tool(
                    name="human",
                    func=self.human,
                    description="The human tool is used to interact with the user and responds to all inputs of the user."
                ),
                Tool(
                    name="sql",
                    func=self.sql_chain,
                    description="useful to interact with database with CRUD operations (takes natural language input)."
                ),
            ]
        else :
            print("Tools already initialized")
            

            
    def initialize_agent(self, verbose: bool = False) -> None:
        """Initialize the agent"""
        # self.agent = initialize_agent(
        #     agent_type=AgentType.OPENAI_FUNCTIONS,
        #     llm=llm,
        #     tools=self.tools,
        #     verbose=verbose,
        # )
        self.agent = OpenAIFunctionsAgent(
            llm=llm,
            tools=self.tools,
            prompt=self.prompt,
        )
        agent_executor =AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=verbose,
            memory=self.memory,
        )
        return agent_executor
        
        
     
    def initialize(self) -> None:
        """Initialize the assistant"""
        # self.initialize_vectordb()
        self.initialize_human()
        self.intialize_tools()
        self.agent_executor = self.initialize_agent(verbose=True)
        return None
    
    def get_answer(self, question: str) -> str:
        """Get the answer from the agent"""
        return self.agent_executor.run(question)
