from fastapi import APIRouter, Request, Depends
from system.model import SysMenu as Menu
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from system.form import MenuForm
from core import config
from db.db_base import DbHandleBase
from public.oppose_crawler import backstage
from public.get_data_by_cache import get_token_key, get_current_user
from public.data_utils import orm_one_to_dict, orm_all_to_dict, get_tree_data
import datetime

__author__ = '吾延'
router = APIRouter()


@router.get('/get-menu-list', dependencies=[Depends(backstage)], tags=[config.LOG_QUERY], name="菜单列表, 只获取第一层")
async def get_menu_list(request: Request, menu_name: str = None):
    """
    菜单列表, 只获取第一层
    """
    db: Session = request.state.db
    db_menu = db.query(Menu.id,  Menu.menu_name, Menu.idx, Menu.parent_id, Menu.menu_code,
                       Menu.menu_url, Menu.menu_icon, Menu.menu_type).filter(Menu.state == 1)
    if menu_name:
        db_menu = db_menu.filter(Menu.menu_name.like('%' + menu_name + '%'))
    menu_tuple_list = db_menu.order_by('idx').all()
    menu_list = orm_all_to_dict(menu_tuple_list)
    paren_menu_list = []
    child_menu_list = []
    for dept in menu_list:
        # 第一层
        if not dept['parent_id']:
            paren_menu_list.append(dept)
        else:
            child_menu_list.append(dept)
    if not paren_menu_list and child_menu_list:
        tree_dept_list = child_menu_list
    else:
        # 递归获取子的层
        tree_dept_list = get_tree_data(paren_menu_list, child_menu_list)

    return JSONResponse({'code': config.HTTP_200, 'data': tree_dept_list})


@router.post('/save-menu', dependencies=[Depends(backstage)], tags=[config.LOG_SAVE], name="菜单保存")
async def save_menu(request: Request, form: MenuForm):
    """
    菜单保存
    """
    db: Session = request.state.db
    if form.id:     # 修改
        # 判断是否存在
        if not db.query(Menu.id).filter(Menu.id == form.id, Menu.state == 1).scalar():
            return JSONResponse({'code': config.HTTP_404, 'message': '找不到该部门信息'})
        return JSONResponse({'code': config.HTTP_200, 'message': '修改成功，为不影响他人浏览，此操作将做不入库处理！'})
        user = get_current_user(request)
        update_dict = {'idx': form.idx, 'menu_type': form.menu_type, 'menu_icon': form.menu_icon, 'menu_name': form.menu_name,
                       'menu_code': form.menu_code, 'menu_url': form.menu_url, 'change_by_id': user['id'],
                       'last_change_time': datetime.datetime.now()}
        db.query(Menu).filter(Menu.id == form.id, Menu.state == 1).update(update_dict)
        db.commit()
        return JSONResponse({'code': config.HTTP_200, 'message': '修改菜单成功'})
    else:
        return JSONResponse({'code': config.HTTP_200, 'message': '新增成功，为不影响他人浏览，此操作将做不入库处理！'})
        new_menu = Menu()
        new_menu.parent_id = form.parent_id
        new_menu.menu_type = form.menu_type
        new_menu.menu_name = form.menu_name
        new_menu.idx = form.idx
        new_menu.menu_code = form.menu_code
        new_menu.menu_url = form.menu_url
        new_menu.menu_icon = form.menu_icon
        handle_db = DbHandleBase()
        status_code, dept_obj = handle_db.create(db, get_token_key(request), new_menu)
        if status_code != 200:
            return JSONResponse({'code': config.HTTP_404, 'message': '创建菜单失败'})
    return JSONResponse({'code': config.HTTP_200, 'message': '操作成功'})


@router.get('/get-menu-info', dependencies=[Depends(backstage)], tags=[config.LOG_QUERY], name="菜单详情")
async def get_menu_info(request: Request, menu_id: str):
    """
    菜单详情
    """
    db: Session = request.state.db
    if not menu_id:
        return JSONResponse({'code': config.HTTP_404, 'message': '请选择菜单！'})
    db_menu = db.query(Menu.id, Menu.menu_name, Menu.idx, Menu.menu_code, Menu.menu_url, Menu.parent_id,
                       Menu.menu_icon, Menu.menu_type).filter(Menu.state == 1, Menu.id == menu_id).first()
    if not db_menu:
        return JSONResponse({'code': config.HTTP_404, 'message': '没有找到该菜单信息！'})
    menu_info = orm_one_to_dict(db_menu)

    return JSONResponse({'code': config.HTTP_200, 'data': menu_info})


@router.get('/del-menu', dependencies=[Depends(backstage)], tags=[config.LOG_DELETE], name="删除菜单")
async def del_menu(request: Request, menu_id: str):
    """
    删除菜单
    """
    db: Session = request.state.db
    if not menu_id:
        return JSONResponse({'code': config.HTTP_404, 'message': '至少选择一个要删除的菜单！'})
    if not db.query(Menu.id).filter(Menu.id == menu_id, Menu.state == 1).scalar():
        return JSONResponse({'code': config.HTTP_404, 'message': '找不到该菜单信息或已删除'})
    return JSONResponse({'code': config.HTTP_200, 'message': '删除成功，为不影响他人浏览，此操作将做不入库处理！'})
    user = get_current_user(request)
    now_time = datetime.datetime.now()
    res = recursion_del_menu(db, menu_id, user['id'], now_time)
    if not res:
        return JSONResponse({'code': config.HTTP_404, 'message': '删除失败'})
    return JSONResponse({'code': config.HTTP_200, 'message': '删除成功'})


def recursion_del_menu(db, menu_id, user_id, now_time):
    """递归删除菜单列表"""
    kwargs = {"deleted_time": now_time, 'deleted_by_id': user_id, 'state': 0}
    res = db.query(Menu).filter(Menu.id == menu_id).update(kwargs)
    db.commit()
    menu_child_id_list = db.query(Menu.id).filter(Menu.parent_id == menu_id).all()
    if menu_child_id_list:
        for menu_child_id in menu_child_id_list:
            recursion_del_menu(db, menu_child_id[0], user_id, now_time)

    return res
