from typing import Annotated

from fastapi import APIRouter, Query, Path, Depends
from starlette import status

from model.note import Note
from utils.dependencies import get_current_active_user

router = APIRouter(prefix="/note", tags=["note"], dependencies=[Depends(get_current_active_user)])


@router.get(path="/",
            status_code=status.HTTP_200_OK,
            response_model=list[Note],
            summary="Get list of notes")
def note_list(
        title: Annotated[
            str | None,
            Query(
                title="Note title",
                description="This parameter is used to find notes"),
        ] = None):
    pass


@router.post(path="/",
             status_code=status.HTTP_201_CREATED,
             response_model=Note,
             summary="Create a new note")
def create_note(note: Note):
    pass


@router.get(path="/{note_id}/",
            status_code=status.HTTP_200_OK,
            response_model=Note,
            summary="Get details of a note")
def note_detail(
        note_id: Annotated[
            int,
            Path(
                title="Note id",
                ge=1)
        ]):
    pass


@router.delete(path="/{note_id}/",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a note")
def delete_note(
        note_id: Annotated[
            int,
            Path(
                title="Note id",
                ge=1)
        ]):
    pass


@router.patch(path="/{note_id}/",
              status_code=status.HTTP_200_OK,
              response_model=Note,
              summary="Update an existing note")
def update_note(note_id: int, note: Note):
    pass
