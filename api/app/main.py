from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List
from Bio import Entrez
import time
import pandas as pd

app = FastAPI(title="PubMed Data Fetcher")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# リクエストボディのモデル定義
class PubMedRequest(BaseModel):
    email: EmailStr
    pmids: List[str]

# PubMed記事を取得する関数
def fetch_pubmed_articles(email: str, pmids: List[str]):
    Entrez.email = email
    articles_data = []

    for pmid in pmids:
        try:
            record = Entrez.read(Entrez.efetch(db="pubmed", id=pmid, retmode="xml"))
            article = record['PubmedArticle'][0]['MedlineCitation']['Article']

            article_info = {
                'PMID': pmid,
                'Title': article['ArticleTitle'],
                'Journal': article['Journal']['Title'],
                'Year': article['Journal'].get('JournalIssue', {}).get('PubDate', {}).get('Year', ''),
                'Authors': '; '.join([
                    f"{author.get('LastName', '')} {author.get('ForeName', '')}"
                    for author in article.get('AuthorList', [])
                ]),
                'Abstract': article.get('Abstract', {}).get('AbstractText', [''])[0] if isinstance(
                    article.get('Abstract', {}).get('AbstractText', ['']), list
                ) else article.get('Abstract', {}).get('AbstractText', ''),
                'Keywords': '; '.join(
                    record['PubmedArticle'][0]['MedlineCitation'].get('KeywordList', [[]])[0]
                ) if record['PubmedArticle'][0]['MedlineCitation'].get('KeywordList') else ''
            }

            articles_data.append(article_info)
            time.sleep(1)

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error with PMID {pmid}: {str(e)}")

    return articles_data

@app.get("/")
async def root():
    return {"message": "PubMed Data Fetcher API is running"}

@app.post("/fetch-pubmed")
async def fetch_pubmed(request: PubMedRequest):
    try:
        articles = fetch_pubmed_articles(request.email, request.pmids)
        return {"status": "success", "data": articles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))