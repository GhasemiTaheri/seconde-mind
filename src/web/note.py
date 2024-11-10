from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Query, Path, Depends, HTTPException
from starlette import status

from model import User, PublicNote, CreateNote
from model.note import Note
from utils.dependencies import get_current_active_user

router = APIRouter(prefix="/note", tags=["note"])


@router.get(path="/",
            status_code=status.HTTP_200_OK,
            response_model=list[PublicNote],
            summary="Get list of notes")
async def note_list(
        user: Annotated[User, Depends(get_current_active_user)],
        title: Annotated[
            str | None,
            Query(
                title="Note title",
                description="This parameter is used to find notes"),
        ] = None):
    return await Note.user_note_list(user_id=str(user.id))


@router.post(path="/",
             status_code=status.HTTP_201_CREATED,
             response_model=PublicNote,
             summary="Create a new note")
async def create_note(user: Annotated[User, Depends(get_current_active_user)],
                      note_in: CreateNote):
    data = note_in.dict()
    data['user'] = str(user.id)
    return await Note(**data).insert()


@router.get(path="/{note_id}/",
            status_code=status.HTTP_200_OK,
            response_model=PublicNote,
            summary="Get details of a note")
async def note_detail(user: Annotated[User, Depends(get_current_active_user)],
                      note_id: Annotated[PydanticObjectId, Path(title="Note id")]):
    note = await Note.find_one(Note.id == note_id, Note.user == str(user.id))
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Does not exist",
        )

    return note


@router.delete(path="/{note_id}/",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a note")
async def delete_note(user: Annotated[User, Depends(get_current_active_user)],
                      note_id: Annotated[PydanticObjectId, Path(title="Note id")]):
    note = await Note.find_one(Note.id == note_id, Note.user == str(user.id))
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Does not exist",
        )
    await note.delete()
    return {}


@router.patch(path="/{note_id}/",
              status_code=status.HTTP_200_OK,
              response_model=PublicNote,
              summary="Update an existing note")
async def update_note(user: Annotated[User, Depends(get_current_active_user)],
                      note_id: Annotated[PydanticObjectId, Path(title="Note id")],
                      note_in: CreateNote):
    note = await Note.find_one(Note.id == note_id, Note.user == str(user.id))
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Does not exist",
        )
    note.title = note_in.title
    note.description = note_in.description
    note.save()
    return note
