from typing import Annotated

from fastapi import APIRouter, Query, Depends, Body, status

from model import User, Note, PublicNote, CreateNote, PaginatedResponse
from utils.dependencies import get_current_active_user, get_note

router = APIRouter(prefix="/note", tags=["note"])


@router.get(path="/",
            response_model=PaginatedResponse,
            status_code=status.HTTP_200_OK,
            summary="Get list of notes")
async def note_list(user: Annotated[User, Depends(get_current_active_user)],
                    size: int = 10,
                    offset: int = 0,
                    title: Annotated[str | None,
                    Query(title="Note title",
                          description="This parameter is used to find notes"),
                    ] = None):
    if title:
        result = Note.find({
            "user": str(user.id),
            "title": {'$regex': f".*{title}.*"}
        })
    else:
        result = Note.find(Note.user == str(user.id))

    return {
        "total": await result.count(),
        "results": await result.skip(offset).limit(size).to_list()
    }


@router.post(path="/",
             status_code=status.HTTP_201_CREATED,
             response_model=PublicNote,
             summary="Create a new note")
async def create_note(user: Annotated[User, Depends(get_current_active_user)],
                      new_note: CreateNote):
    data = new_note.dict()
    data['user'] = str(user.id)
    return await Note(**data).insert()


@router.get(path="/{note_id}/",
            status_code=status.HTTP_200_OK,
            response_model=PublicNote,
            summary="Get details of a note")
async def note_detail(note: Annotated[Note, Depends(get_note)]):
    return note


@router.delete(path="/{note_id}/",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a note")
async def delete_note(note: Annotated[Note, Depends(get_note)]):
    await note.delete()
    return {}


@router.patch(path="/{note_id}/",
              status_code=status.HTTP_200_OK,
              response_model=PublicNote,
              summary="Update an existing note")
async def update_note(note: Annotated[Note, Depends(get_note)],
                      new_note: Annotated[CreateNote, Body()]):
    note.title = new_note.title
    note.description = new_note.description
    note.save()
    return note
