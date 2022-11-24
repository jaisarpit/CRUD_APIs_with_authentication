from fastapi import Body, FastAPI, Response , status, HTTPException , Depends , APIRouter
from .. import schemas,models, oauth2, database, utils
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags= ["vote"]
)

@router.get("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db : Session= Depends(database.get_db), current_user: int =Depends(oauth2.get_current_user)):
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if(vote.dir ==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail= f"user {current_user.id} already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "New vote added"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote doesn't exist")
        vote_query.delete()
        db.commit()
        return {"message": "successfully deleted vote"}
