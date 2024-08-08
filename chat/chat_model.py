from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from typing import List, Dict
load_dotenv()
class NewsBot():
    llm: ChatOpenAI = ChatOpenAI(model_name='gpt-4o', temperature=1)
    chains: Dict[str, Dict[str, any]] = dict()

    def __init__(self):
        self.create_chain()

    def create_chain(self):

        prompt = hub.pull("everyshare/newsreader-summarize-prompt")
        self.chain = prompt | self.llm | StrOutputParser()

    def summarize_content(self, content: str) -> str:
        return self.chain.invoke({"article": content})
    def summarize_contents(self, contents: List[Dict[str, str]]) -> List[str]:

        return self.chain.batch(contents)



news_bot = NewsBot()

