from fastapi import APIRouter, Request, Depends
from system.model import SysDepartment as Dept
from sqlalchemy.orm import Session
from system.form import DeptForm
from core import config
from db.db_base import DbHandleBase
from public.oppose_crawler import backstage
from public.get_data_by_cache import get_current_user, get_token_key
from public.data_utils import get_tree_data, orm_all_to_dict, sql_one_to_dict
import datetime
from fastapi.responses import JSONResponse

__author__ = '吾延'
router = APIRouter()


@router.get('/get-dept-list', dependencies=[Depends(backstage)], tags=[config.LOG_QUERY], name="获取部门列表")
async def get_dept_list(request: Request, dept_name: str = None):
    """
    获取部门列表
    """
    db: Session = request.state.db
    kwargs = {'state': 1}
    db_dept = db.query(Dept.id, Dept.parent_id, Dept.department_name, Dept.idx,
                       Dept.remarks, Dept.create_time).filter_by(**kwargs)
    if dept_name:
        db_dept = db_dept.filter(Dept.department_name.like('%' + dept_name + '%'))
    dept_tuple_list = db_dept.order_by("idx").all()
    dept_list = orm_all_to_dict(dept_tuple_list)
    paren_dept_list = []
    child_dept_list = []
    for dept in dept_list:
        # 第一层
        if not dept['parent_id']:
            paren_dept_list.append(dept)
        else:
            child_dept_list.append(dept)
    if not paren_dept_list and child_dept_list:
        tree_dept_list = child_dept_list
    else:
        # 递归获取子的层
        tree_dept_list = get_tree_data(paren_dept_list, child_dept_list)
    return JSONResponse({'code': config.HTTP_200, 'data': tree_dept_list})


@router.get('/get-dept-info', dependencies=[Depends(backstage)], tags=[config.LOG_QUERY], name="获取部门详情")
async def get_dept_detail(request: Request, dept_id: str):
    """
    获取部门详情
    """
    db: Session = request.state.db
    if not dept_id:
        return JSONResponse({'code': config.HTTP_404, 'message': '请选择部门'})
    db_dept = db.execute("select c.id, c.department_name, c.parent_id, c.idx, c.remarks, p.department_name "
                         "as parent_name from sys_department as c left join sys_department as p on "
                         "p.id=c.parent_id where c.state=1 and c.id=:cid;", params={'cid': dept_id})
    dept = db_dept.fetchone()
    if not dept:
        return JSONResponse({'code': config.HTTP_404, 'message': '没有找到该部门信息'})
    dept_info = sql_one_to_dict(dept)
    if not dept_info['parent_name']:
        dept_info['parent_name'] = '全部'
    return JSONResponse({'code': config.HTTP_200, 'data': dept_info})


@router.post('/save-dept', dependencies=[Depends(backstage)], tags=[config.LOG_SAVE], name="保存部门")
async def save_dept(request: Request, form: DeptForm):
    """
    保存部门
    """
    db: Session = request.state.db
    if form.id:
        # 判断是否存在
        if not db.query(Dept.id).filter(Dept.id == form.id, Dept.state == 1).scalar():
            return JSONResponse({'code': config.HTTP_404, 'message': '找不到该部门信息'})
        return JSONResponse({'code': config.HTTP_200, 'message': '修改成功，为不影响他人浏览，此操作将做不入库处理！'})
        user = get_current_user(request)
        update_dic = {
            'idx': form.idx,
            'department_name': form.department_name,
            'remarks': form.remarks,
            'change_by_id': user['id'],
            'last_change_time': datetime.datetime.now()
        }
        db.query(Dept).filter(Dept.id == form.id, Dept.state == 1).update(update_dic)
        db.commit()
        return JSONResponse({'code': config.HTTP_200, 'message': '修改部门成功'})
    return JSONResponse({'code': config.HTTP_200, 'message': '修改新增，为不影响他人浏览，此操作将做不入库处理！'})
    token_key = get_token_key(request)
    dept = Dept()
    dept.parent_id = form.parent_id
    dept.idx = form.idx
    dept.department_name = form.department_name
    dept.remarks = form.remarks
    handle_db = DbHandleBase()
    status_code, dept_obj = handle_db.create(db, token_key, dept)
    if status_code != 200:
        return JSONResponse({'code': config.HTTP_404, 'message': '创建部门失败'})
    return JSONResponse({'code': config.HTTP_200, 'message': '创建部门成功'})


@router.get('/del-dept', dependencies=[Depends(backstage)], tags=[config.LOG_DELETE], name="删除部门")
async def del_dept(request: Request, dept_id: str):
    """
    删除部门
    """
    if not dept_id:
        return JSONResponse({'code': config.HTTP_404, 'message': '请选择部门！'})
    db: Session = request.state.db
    if not db.query(Dept.id).filter(Dept.id == dept_id, Dept.state == 1).scalar():
        return JSONResponse({'code': config.HTTP_404, 'message': '找不到该部门信息或已删除'})
    return JSONResponse({'code': config.HTTP_200, 'message': '删除成功，为不影响他人浏览，此操作将做不入库处理！'})
    user = get_current_user(request)
    now_time = datetime.datetime.now()
    res = recursion_del_dept(db, dept_id, user['id'], now_time)
    if not res:
        return JSONResponse({'code': config.HTTP_404, 'message': '删除失败'})
    return JSONResponse({'code': config.HTTP_200, 'message': '删除成功'})


def recursion_del_dept(db, dept_id, user_id, now_time):
    """递归删除部门列表"""
    kwargs = {"deleted_time": now_time, 'deleted_by_id': user_id, 'state': 0}
    res = db.query(Dept).filter(Dept.id == dept_id).update(kwargs)
    db.commit()
    dept_child_id_list = db.query(Dept.id).filter(Dept.parent_id == dept_id).all()
    if dept_child_id_list:
        for dept_child_id in dept_child_id_list:
            recursion_del_dept(db, dept_child_id[0], user_id, now_time)

    return res




