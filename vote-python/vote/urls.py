from fastapi import APIRouter
from vote import vote_mng

__author__ = '吾延'
vote_router = APIRouter()


vote_router.include_router(vote_mng.router, prefix='/activity')

