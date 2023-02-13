from typing import List, Any, Union
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from .schema import {{ cookiecutter.pascal_name }}Create, {{ cookiecutter.pascal_name }}Info
from .model import {{ cookiecutter.pascal_name }}


router = APIRouter()


"""
接口：{{ cookiecutter.pascal_name }} 表增删改查

POST   /api/{{ cookiecutter.snake_name }}s            ->  create_{{ cookiecutter.snake_name }}  ->  创建 {{ cookiecutter.snake_name }}
GET    /api/{{ cookiecutter.snake_name }}s            ->  get_{{ cookiecutter.snake_name }}s    ->  获取所有 {{ cookiecutter.snake_name }}
GET    /api/{{ cookiecutter.snake_name }}s/{{'{'}}{{ cookiecutter.snake_name }}_id{{'}'}}   ->  get_{{ cookiecutter.snake_name }}     ->  获取单个 {{ cookiecutter.snake_name }}
PUT    /api/{{ cookiecutter.snake_name }}s/{{'{'}}{{ cookiecutter.snake_name }}_id{{'}'}}   ->  update_{{ cookiecutter.snake_name }}  ->  更新单个 {{ cookiecutter.snake_name }}
DELETE /api/{{ cookiecutter.snake_name }}s/{{'{'}}{{ cookiecutter.snake_name }}_id{{'}'}}   ->  delete_{{ cookiecutter.snake_name }}  ->  删除单个 {{ cookiecutter.snake_name }}
"""

# 新建 {{ cookiecutter.snake_name }}
@router.post("/", response_model={{ cookiecutter.pascal_name }}Info, name="新建 {{ cookiecutter.snake_name }}")
async def create_{{ cookiecutter.snake_name }}({{ cookiecutter.snake_name }}: {{ cookiecutter.pascal_name }}Create, db: Session = Depends(get_db)):
    return {{ cookiecutter.pascal_name }}.create(db)


# 获取所有 {{ cookiecutter.snake_name }}
@router.get("/", response_model=List[{{ cookiecutter.pascal_name }}Info], name="获取所有 {{ cookiecutter.snake_name }}")
async def get_{{ cookiecutter.snake_name }}s(db: Session = Depends(get_db)):
    return {{ cookiecutter.pascal_name }}.all(db)


# 通过id查询 {{ cookiecutter.snake_name }}
@router.get("/{{'{'}}{{ cookiecutter.snake_name }}_id{{'}'}}", response_model=Union[{{ cookiecutter.pascal_name }}Info, Any], name="查询 {{ cookiecutter.snake_name }} by {{ cookiecutter.snake_name }}_id")
async def get_{{ cookiecutter.snake_name }}({{ cookiecutter.snake_name }}_id: int, db: Session = Depends(get_db)):
    db_{{ cookiecutter.snake_name }} = {{ cookiecutter.pascal_name }}.get_or_404(db, id={{ cookiecutter.snake_name }}_id)
    if not db_{{ cookiecutter.snake_name }}:
        raise HTTPException(status_code=404, detail="{{ cookiecutter.pascal_name }} not found")
    return db_{{ cookiecutter.snake_name }}


# 通过id更改 {{ cookiecutter.snake_name }}
@router.put("/{{'{'}}{{ cookiecutter.snake_name }}_id{{'}'}}", name="更改 {{ cookiecutter.snake_name }} by {{ cookiecutter.snake_name }}_id")
async def update_{{ cookiecutter.snake_name }}({{ cookiecutter.snake_name }}_id: int, {{ cookiecutter.snake_name }}: {{ cookiecutter.pascal_name }}Create, db: Session = Depends(get_db)):
    return {{ cookiecutter.pascal_name }}.update_by(db, {{ cookiecutter.snake_name }}_id, {})


# 通过id删除 {{ cookiecutter.snake_name }}
@router.delete("/{{'{'}}{{ cookiecutter.snake_name }}_id{{'}'}}", name="删除 {{ cookiecutter.snake_name }} by {{ cookiecutter.snake_name }}_id")
async def delete_{{ cookiecutter.snake_name }}({{ cookiecutter.snake_name }}_id: int, db: Session = Depends(get_db)):
    {{ cookiecutter.pascal_name }}.remove_by(db, id={{ cookiecutter.snake_name }}_id)
    return 0
