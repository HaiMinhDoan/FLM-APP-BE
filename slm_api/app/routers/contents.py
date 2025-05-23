import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.model.model import get_db, Content, ContentCategory, MediaContent
from app.repository.model_repo import ContentRepository, ContentCategoryRepository, MediaContentRepository
from app.model.dto import ContentCreateDTO, MediaContentCreateDTO, ContentCategoryCreateDTO

from typing import List
import traceback

router = APIRouter()

@router.get("/content_category", response_model=List[dict])
def get_content_categories(db: Session = Depends(get_db)):
    """Lấy danh sách Content Category."""
    content_categories = ContentCategoryRepository.get_all_content_categories(db)
    content_categories_dict = []
    for content_category in content_categories:
        content_category_dict = content_category.__dict__.copy()
        content_category_dict.pop("_sa_instance_state", None)
        content_categories_dict.append(content_category_dict)
    return content_categories_dict

@router.post("/content_category", response_model=dict)
def create_content_category(content_category_data: ContentCategoryCreateDTO, db: Session = Depends(get_db)):
    """Tạo Content Category mới."""
    newContentCategory = ContentCategoryRepository.create_content_category(db, content_category_data={"name": content_category_data.name,
                                                                                                        "code": content_category_data.code,
                                                                                                        "description": content_category_data.description})
    if not newContentCategory:
        raise HTTPException(status_code=404, detail="Create content category failed")
    return {"message": "Content category created successfully"}

@router.get("/content", response_model=List[dict])
def get_contents(db: Session = Depends(get_db)):
    """Lấy danh sách Content."""
    contents = ContentRepository.get_all_contents(db)
    contents_dict = []
    for content in contents:
        content_dict = content.__dict__.copy()
        content_dict["category"] = content.category.__dict__.copy()
        content_dict["category"].pop("_sa_instance_state", None)
        content_dict["media_contents"] = []
        for media_content in content.media_contents:
            media_content_dict = media_content.__dict__.copy()
            media_content_dict.pop("_sa_instance_state", None)
            content_dict["media_contents"].append(media_content_dict)
        content_dict.pop("_sa_instance_state", None)
        contents_dict.append(content_dict)
    return contents_dict

@router.post("/content", response_model=dict)
def create_content(content_data: ContentCreateDTO, db: Session = Depends(get_db)):
    """Tạo Content mới."""
    try:
        # Bắt đầu giao dịch
        with db.begin():
            # Tạo Content
            newContent = ContentRepository.create_content(db, content_data={
                "title": content_data.title,
                "content": content_data.content,
                "hashtag": content_data.hashtag,
                "category_id": content_data.content_category_id
            })
            if not newContent:
                raise HTTPException(status_code=404, detail="Create content failed")

            # Tạo MediaContent liên quan
            for media_content in content_data.media_contents:
                MediaContentRepository.create_media_content(db, media_content_data={
                    "content_id": newContent.id,
                    "kind": media_content.kind,
                    "link": media_content.link,
                    "title": media_content.title
                })

        # Nếu không có lỗi, trả về kết quả thành công
        return {"message": "Content created successfully"}
    except Exception as e:
        # Rollback sẽ tự động được thực hiện bởi `with db.begin()` nếu có lỗi
        print("Error occurred while creating content:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error creating content: {str(e)}")